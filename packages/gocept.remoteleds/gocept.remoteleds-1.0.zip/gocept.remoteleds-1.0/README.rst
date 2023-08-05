=================
gocept.remoteleds
=================

Preparing a developer machine
-----------------------------

>>> hg clone https://bitbucket.org/gocept/gocept.remoteleds
>>> cd gocept.remoteleds
>>> virtualenv .
>>> bin/pip install -e .[test]

Running tests is than as easy as:

>>> bin/py.test