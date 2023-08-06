"""
Tests for go_api utility functions.
"""

from twisted.internet.defer import Deferred, inlineCallbacks, succeed
from twisted.internet.task import Clock
from twisted.trial.unittest import TestCase

from go_api.utils import defer_async, simulate_async


class DummyError(Exception):
    """
    Exception for use in tests.
    """


class TestDeferAsync(TestCase):
    def test_returns_deferred(self):
        d = defer_async('foo', reactor=Clock())
        self.assertTrue(isinstance(d, Deferred))

    def test_fires_only_after_reactor_runs(self):
        clock = Clock()
        d = defer_async('foo', reactor=clock)
        self.assertEqual(d.called, False)
        clock.advance(0)
        self.assertEqual(d.called, True)
        self.assertEqual(d.result, 'foo')


class TestSimulateAsync(TestCase):
    def test_wraps(self):
        def simple():
            """doc"""

        f = simulate_async(simple)
        self.assertEqual(f.__name__, "simple")
        self.assertEqual(f.__doc__, "doc")
        self.assertEqual(f.__module__, __name__)

    @inlineCallbacks
    def test_handles_successful_return(self):
        def simple():
            return 'foo'
        f = simulate_async(simple)
        d = f()
        self.assertTrue(isinstance(d, Deferred))
        v = yield d
        self.assertEqual(v, 'foo')

    @inlineCallbacks
    def test_handler_deferred_return(self):
        def simple_deferred():
            return succeed('foo')
        f = simulate_async(simple_deferred)
        d = f()
        self.assertTrue(isinstance(d, Deferred))
        v = yield d
        self.assertEqual(v, 'foo')

    @inlineCallbacks
    def test_handles_exceptions(self):
        def error():
            raise DummyError()
        f = simulate_async(error)
        d = f()
        self.assertTrue(isinstance(d, Deferred))
        yield self.failUnlessFailure(d, DummyError)

    def test_fires_only_after_reactor_runs(self):
        def simple():
            return 'foo'
        clock = Clock()
        f = simulate_async(simple, reactor=clock)
        d = f()
        self.assertEqual(d.called, False)
        clock.advance(0)
        self.assertEqual(d.called, True)
        self.assertEqual(d.result, 'foo')

    @inlineCallbacks
    def test_complex_arguments(self):
        def simple(*args, **kw):
            return (args, kw)
        f = simulate_async(simple)
        result = yield f("foo", "bar", baz=3, boop="barp")
        self.assertEqual(result, (
            ("foo", "bar"),
            {"baz": 3, "boop": "barp"},
        ))
