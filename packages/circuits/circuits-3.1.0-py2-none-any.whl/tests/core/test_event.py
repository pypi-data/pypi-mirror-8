# Module:   test_event
# Date:     12th April 2010
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""Event Tests"""

import py

from circuits import Event, Component


class test(Event):
    """test Event"""


class App(Component):

    def test(self):
        return "Hello World!"


def test_repr():
    app = App()
    while app:
        app.flush()

    e = test()

    s = repr(e)
    assert s == "<test[] ( )>"

    app.fire(e)

    s = repr(e)
    assert s == "<test[*] ( )>"


def test_create():
    app = App()
    while app:
        app.flush()

    e = Event.create("test")

    s = repr(e)
    assert s == "<test[] ( )>"

    app.fire(e)

    s = repr(e)
    assert s == "<test[*] ( )>"


def test_getitem():
    app = App()
    while app:
        app.flush()

    e = test(1, 2, 3, foo="bar")

    assert e[0] == 1
    assert e["foo"] == "bar"

    def f(e, k):
        return e[k]

    py.test.raises(TypeError, f, e, None)


def test_setitem():
    app = App()
    while app:
        app.flush()

    e = test(1, 2, 3, foo="bar")

    assert e[0] == 1
    assert e["foo"] == "bar"

    e[0] = 0
    e["foo"] = "Hello"

    def f(e, k, v):
        e[k] = v

    py.test.raises(TypeError, f, e, None, None)

    assert e[0] == 0
    assert e["foo"] == "Hello"


def test_subclass_looses_properties():
    class hello(Event):
        success = True
    e = hello().child('success')
    assert e.success is False
