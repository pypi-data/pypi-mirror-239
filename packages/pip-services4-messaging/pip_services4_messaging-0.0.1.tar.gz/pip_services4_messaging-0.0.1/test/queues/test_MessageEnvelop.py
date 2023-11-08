# -*- coding: utf-8 -*-
import json

from pip_services4_components.context import Context

from pip_services4_messaging.queues import MessageEnvelope


class TestMessageEnvelop:
    def test_from_to_json(self):
        message = MessageEnvelope(Context.from_trace_id("123"), "Test", "This is a test message")
        jsoon = json.dumps(message.to_json())

        message2 = MessageEnvelope.from_json(jsoon)
        assert message.message_id == message2.message_id
        assert message.trace_id == message2.trace_id
        assert message.message_type == message2.message_type
        assert message.message.decode('utf-8') == message2.message.decode('utf-8')
