"""
Pip.Services Net
----------------------

Pip.Services is an open-source library of basic microservices.
pip_services4_messaging provides messaging components.

Links
`````

* `website <http://github.com/pip-services-python/pip-services-python-messaging>`_
* `development version <http://github.com/pip-services4/pip-services4-python/tree/main/pip-services4-messaging-python>`

"""

from setuptools import find_packages
from setuptools import setup

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='pip_services4_messaging',
    version='0.0.1',
    url='http://github.com/pip-services4/pip-services4-python/tree/main/pip-services4-messaging-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='Messaging components for Pip.Services in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'pip-services4-commons >= 0.0.1, < 4.0',
        'pip-services4-components >= 0.0.1, < 4.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
