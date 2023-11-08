# -*- coding: utf-8 -*-
import threading
import time
from abc import abstractmethod
from typing import List, Optional

from pip_services4_components.config import ConfigParams
from pip_services4_components.context import IContext
from pip_services4_components.run import ICleanable

from .IMessageReceiver import IMessageReceiver
from .MessageEnvelope import MessageEnvelope
from .MessageQueue import MessageQueue
from .MessagingCapabilities import MessagingCapabilities


class CachedMessageQueue(MessageQueue, ICleanable):
    """
    Message queue that caches received messages in memory to allow peek operations
    that may not be supported by the undelying queue.

    This queue is users as a base implementation for other queues
    """

    def __init__(self, name: str = None, capabilities: MessagingCapabilities = None):
        """
        Creates a new instance of the persistence component.

        :param name: (optional) a queue name
        :param capabilities: (optional) a capabilities of this message queue
        """
        super().__init__(name, capabilities)
        self._auto_subscribe: bool = None
        self._messages: List[MessageEnvelope] = []
        self._receiver: IMessageReceiver = None
        self._lock = threading.Lock()
        self._event = threading.Event()

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        super().configure(config)

        self._auto_subscribe = config.get_as_boolean_with_default("options.autosubscribe", self._auto_subscribe)

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.is_open():
            return

        try:
            if self._auto_subscribe:
                self._subscribe(context)

            self._logger.debug(context, "Opened queue " + self.get_name())

        except Exception as err:
            self.close(context)

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if not self.is_open():
            return

        try:
            # Unsubscribe from the broker
            self._unsubscribe(context)
        finally:
            with self._lock:
                self._messages = []
                self._receiver = None

    @abstractmethod
    def _subscribe(self, context: Optional[IContext]):
        """
        Subscribes to the message broker.

        :param context: (optional) transaction id to trace execution through call chain.
        """

    @abstractmethod
    def _unsubscribe(self, context: Optional[IContext]):
        """
        Unsubscribes from the message broker.

        :param context: (optional) transaction id to trace execution through call chain.
        """

    def clear(self, context: Optional[IContext]):
        """
        Clears component state.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        with self._lock:
            self._messages = []

    def read_message_count(self) -> int:
        """
        Reads the current number of messages in the queue to be delivered.

        :return: a number of messages in the queue.
        """
        with self._lock:
            return len(self._messages)

    def peek(self, context: Optional[IContext]) -> MessageEnvelope:
        """
        Peeks a single incoming message from the queue without removing it.
        If there are no messages available in the queue it returns None.

        :param context: (optional) transaction id to trace execution through call chain.
        :return: a peeked message or <code>null</code>.
        """
        self._check_open(context)

        # Subscribe to topic if needed
        self._subscribe(context)

        # Peek a message from the top
        message: MessageEnvelope = None

        with self._lock:
            if len(self._messages) > 0:
                message = self._messages[0]

        if message is not None:
            self._logger.trace(message.trace_id, "Peeked message %s on %s", message, self.get_name())

        return message

    def peek_batch(self, context: Optional[IContext], message_count: int) -> List[MessageEnvelope]:
        """
        Peeks multiple incoming messages from the queue without removing them.
        If there are no messages available in the queue it returns an empty list.

        Important: This method is not supported by MQTT.

        :param context: (optional) transaction id to trace execution through call chain.
        :param message_count: a maximum number of messages to peek.
        :return: a list with peeked messages.
        """
        self._check_open(context)

        # Subscribe to topic if needed
        self._subscribe(context)

        # Peek a batch of messages
        with self._lock:
            messages = self._messages[:message_count]

        self._logger.trace(context, "Peeked %d messages on %s", len(messages), self.get_name())

        return messages

    def receive(self, context: Optional[IContext], wait_timeout: int) -> MessageEnvelope:
        """
        Receives an incoming message and removes it from the queue.

        :param context: (optional) transaction id to trace execution through call chain.
        :param wait_timeout: a timeout in milliseconds to wait for a message to come.
        :return: a received message or `None`.
        """
        self._check_open(context)

        # Subscribe to topic if needed
        self._subscribe(context)

        check_interval_ms = 100
        elapsed_time = 0

        # Get message the the queue
        with self._lock:
            message = None if len(self._messages) < 0 else self._messages.pop(0)

        while elapsed_time < wait_timeout and message is None:
            # Wait for a while
            time.sleep(wait_timeout / 1000)
            elapsed_time += check_interval_ms

            # Get message the the queue
            with self._lock:
                message = self._messages.pop(0)

        return message

    def _send_message_to_receiver(self, receiver: IMessageReceiver, message: MessageEnvelope):
        """
        TODO add description

        :param receiver:
        :param message:
        :return:
        """
        trace_id = None if message is None else message.trace_id
        if message is None or receiver is None:
            self._logger.warn(trace_id, "Message was skipped.")
            return
        try:
            self._receiver.receive_message(message, self)
        except Exception as ex:
            self._logger.error(trace_id, ex, "Failed to process the message")

    def listen(self, context: Optional[IContext], receiver: IMessageReceiver):
        """
        Listens for incoming messages and blocks the current thread until queue is closed.

        :param context: (optional) transaction id to trace execution through call chain.
        :param receiver: a receiver to receive incoming messages.
        """
        if not self.is_open():
            return

        self._subscribe(context)

        self._logger.trace(None, "Started listening messages at %s", self.get_name())

        # Resend collected messages to receiver
        while self.is_open() and len(self._messages) > 0:
            with self._lock:
                message = self._messages.pop(0)

                if message is not None:
                    self._send_message_to_receiver(receiver, message)

        # Set the receiver
        if self.is_open():
            self._receiver = receiver

    def end_listen(self, context: Optional[IContext]):
        """
        Ends listening for incoming messages.
        When this method is call **listen** unblocks the thread and execution continues.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        self._receiver = None
