"""
Small utilities for writing Vumi Go APIs.
"""

from functools import wraps

from twisted.internet.defer import Deferred, maybeDeferred


def defer_async(value, reactor=None):
    """
    Return a deferred that fires with the given value, but only after the
    reactor has a chance to run.

    Useful when writing functions that need to mimic asynchronous behaviour
    (usually for use in unit tests).
    """
    if reactor is None:
        from twisted.internet import reactor
    d = Deferred()
    reactor.callLater(0, lambda: d.callback(value))
    return d


def simulate_async(f, reactor=None):
    """
    Decorator to use on synchronous methods to convert their
    result to an asynchronous deferred that fires after the
    reactor has been given a chance to run.

    Synchronous methods might return a deferred that has
    already fired. :func:`simulate_async` supports that case
    by returning a new deferred that will only fire after the
    reactor has run.
    """
    if reactor is None:
        from twisted.internet import reactor

    @wraps(f)
    def async_f(*args, **kw):
        d = maybeDeferred(f, *args, **kw)
        async_d = Deferred()
        reactor.callLater(0, lambda: d.chainDeferred(async_d))
        return async_d

    return async_f
