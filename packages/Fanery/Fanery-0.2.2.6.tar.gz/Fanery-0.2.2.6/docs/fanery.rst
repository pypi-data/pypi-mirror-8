Fanery Framework
================

An opinionated application development framework.

Project Goals
-------------

- Strong security by default.
- Focus on being developer-oriented.
- Promote funcional pythonic style.
- Promote continuous testing+profiling.

Install
-------

1. First make sure to install successfully the following C libraries::

    pip install PyNaCl
    pip install cxor
    pip install ujson
    pip install scrypt
    pip install bjoern
    pip install bsdiff4
    pip install ciso8601
    pip install python-libuuid
    pip install msgpack-python
    pip install linesman objgraph

2. Then install Fanery and run test files::

    pip install Fanery
    python tests/test_term.py
    python tests/test_service.py

Contribute
----------

- Issue Tracker: https://bitbucket.org/mcaramma/fanery/issues
- Source Code: https://bitbucket.org/mcaramma/fanery/src

License
-------

The project is licensed under the ISC license.
