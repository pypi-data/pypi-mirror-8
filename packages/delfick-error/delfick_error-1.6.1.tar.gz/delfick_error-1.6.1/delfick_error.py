from __future__ import print_function

from total_ordering import total_ordering
from contextlib import contextmanager
import unittest
import hashlib
import sys
import six
import re

if hasattr(unittest, "util"):
    safe_repr = unittest.util.safe_repr
else:
    _MAX_LENGTH = 80
    def safe_repr(obj, short=False):
        try:
            result = repr(obj)
        except Exception:
            result = object.__repr__(obj)
        if not short or len(result) < _MAX_LENGTH:
            return result
        return result[:_MAX_LENGTH] + ' [truncated]...'

@total_ordering
class DelfickError(Exception):
    """Helpful class for creating custom exceptions"""
    desc = ""

    def __init__(self, message="", **kwargs):
        self.kwargs = kwargs
        self.errors = kwargs.get("_errors", [])
        if "_errors" in kwargs:
            del kwargs["_errors"]
        self.message = message
        super(DelfickError, self).__init__(message)

    def __str__(self):
        message = self.oneline()
        if self.errors:
            message = "{0}\nerrors:\n=======\n\n\t{1}".format(message, "\n\t".join("{0}\n-------".format('\n\t'.join(str(error).split('\n'))) for error in self.errors))
        return message

    def __unicode__(self):
        return str(self).decode("utf-8")

    def __repr__(self):
        return "{0}({1}, {2}, _errors={3})".format(self.__class__.__name__, self.message, ', '.join("{0}={1}".format(k, v) for k, v in self.kwargs.items()), self.errors)

    def __hash__(self):
        return hash(self.as_tuple())

    def oneline(self):
        """Get back the error as a oneliner"""
        desc = self.desc
        message = self.message

        info = ["{0}={1}".format(k, self.formatted_val(k, v)) for k, v in sorted(self.kwargs.items())]
        info = '\t'.join(info)
        if info and (message or desc):
            info = "\t{0}".format(info)

        if desc:
            if message:
                message = ". {0}".format(message)
            return '"{0}{1}"{2}'.format(desc, message, info)
        else:
            if message:
                return '"{0}"{1}'.format(message, info)
            else:
                return "{0}".format(info)

    def formatted_val(self, key, val):
        """Format a value for display in error message"""
        if not hasattr(val, "delfick_error_format"):
            return val
        else:
            try:
                return val.delfick_error_format(key)
            except Exception as error:
                return "<|Failed to format val for exception: val={0}, error={1}|>".format(val, error)

    def __eq__(self, error):
        """Say whether this error is like the other error"""
        return error.__class__ == self.__class__ and error.message == self.message and error.kwargs == self.kwargs and sorted(self.errors) == sorted(error.errors)

    def __lt__(self, error):
        return self.as_tuple() < error.as_tuple()

    def as_tuple(self):
        return (self.__class__.__name__, self.message, tuple(sorted(self.kwargs.items())), tuple(self.errors))

class ProgrammerError(Exception):
    """For when the programmer should have prevented something happening"""

class NotSpecified(object):
    """Used to tell the difference between None and Empty"""

class DelfickErrorTestMixin:
    @contextmanager
    def fuzzyAssertRaisesError(self, expected_kls, expected_msg_regex=NotSpecified, **values):
        """
        Assert that something raises a particular type of error.

        The error raised must be a subclass of the expected_kls
        Have a message that matches the specified regex.

        And have atleast the values specified in it's kwargs.
        """
        try:
            yield
        except Exception as error:
            try:
                assert issubclass(error.__class__, expected_kls), "Expected {0}, got {1}".format(expected_kls, error.__class__)

                if not issubclass(error.__class__, DelfickError):
                    # For normal exceptions we just regex against the string of the whole exception
                    if expected_msg_regex is not NotSpecified:
                        self.assertMatchingRegex(str(error), expected_msg_regex)
                else:
                    # For special DelfickError exceptions, we compare against error.message, error.kwargs and error._errors
                    if expected_msg_regex is not NotSpecified:
                        self.assertMatchingRegex(error.message, expected_msg_regex)

                    errors = values.get("_errors")
                    if "_errors" in values:
                        del values["_errors"]

                    self.assertDictContains(values, error.kwargs)
                    if errors:
                        self.assertEqual(sorted(error.errors), sorted(errors))
            except AssertionError:
                exc_info = sys.exc_info()
                try:
                    print("!" * 20)
                    print("Got error: {0}".format(error))
                    msg = "Expected: {0}".format(expected_kls)
                    if expected_msg_regex is not NotSpecified:
                        msg = "{0}: {1}".format(msg, expected_msg_regex)
                    if values:
                        msg = "{0}: {1}".format(msg, values)
                    print(msg)
                    print("!" * 20)
                finally:
                    six.reraise(exc_info[0], exc_info[1], exc_info[2])
        else:
            assert False, "Expected an exception to be raised\n\texpected_kls: {0}\n\texpected_msg_regex: {1}\n\thave_atleast: {2}".format(
                expected_kls, expected_msg_regex, values
            )

    def assertDictContains(self, expected, actual, msg=None):
        """Checks whether actual is a superset of expected."""
        missing = []
        mismatched = []
        for key, value in expected.items():
            if key not in actual:
                missing.append(safe_repr(key))
            elif value != actual[key]:
                nxt = "{{{0}: expected={1}, got={2}}}".format(safe_repr(key), safe_repr(value), safe_repr(actual[key]))
                mismatched.append(nxt)

        if not (missing or mismatched):
            return

        error = []
        if missing:
            error.append("Missing: {0}".format(', '.join(sorted(missing))))

        if mismatched:
            error.append("Mismatched: {0}".format(', '.join(sorted(mismatched))))

        if hasattr(self, "_formatMessage"):
            self.fail(self._formatMessage(msg, '; '.join(error)))
        else:
            self.fail(msg or '; '.join(error))

    def assertMatchingRegex(self, text, expected_regex, msg=None):
        """Fail the test unless the text matches the regular expression."""
        if isinstance(expected_regex, (str, bytes)):
            assert expected_regex, "expected_regex must not be empty."
            expected_regex = re.compile(expected_regex)
        if not expected_regex.search(text):
            msg = msg or "Regex didn't match"
            msg = '%s: %r not found in %r' % (msg, expected_regex.pattern, text)
            raise self.failureException(msg)

    def assertIs(self, expr1, expr2, msg=None):
        """For Python2.6 compatibility"""
        spr = None
        if type(DelfickErrorTestMixin) is type:
            spr = super(DelfickErrorTestMixin, self)

        if spr and hasattr(spr, "assertIs"):
            return spr.assertIs(self, expr1, expr2, msg)
        else:
            if expr1 is not expr2:
                standardMsg = '%s is not %s' % (safe_repr(expr1), safe_repr(expr2))
                if hasattr(self, "_formatMessage"):
                    self.fail(self._formatMessage(msg, standardMsg))
                else:
                    self.fail(msg or standardMsg)

