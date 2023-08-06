"""
If you want to catch any exception that might be raised,
catch :class:`mohawk.exc.HawkFail`.
"""


class HawkFail(Exception):
    """
    All Mohawk exceptions derive from this base.
    """


class InvalidCredentials(HawkFail):
    """
    The specified Hawk credentials are invalid.

    For example, the dict could be formatted incorrectly.
    """


class CredentialsLookupError(HawkFail):
    """
    A :class:`mohawk.Receiver` could not look up the
    credentials for an incoming request.
    """


class BadHeaderValue(HawkFail):
    """
    There was an error with an attribute or value when parsing
    or creating a Hawk header.
    """


class MacMismatch(HawkFail):
    """
    The locally calculated MAC did not match the MAC that was sent.
    """


class MisComputedContentHash(HawkFail):
    """
    The signature of the content did not match the actual content.
    """


class TokenExpired(HawkFail):
    """
    The timestamp on a message received has expired.

    .. important::

        The `Hawk`_ spec mentions how you can synchronize
        your sender's time with the receiver in the case
        of unexpected expiration. It is okay to expose the
        server timestamp in the clear (in the absence of TLS)
        so long as it is accompanied by a ts mac calculated
        using the client's credentials and the client verifies
        the mac prior to applying the offset.
        See the Hawk Node lib for an example of HMAC'ing the
        timestamp to send to clients.

    .. _`Hawk`: https://github.com/hueniverse/hawk
    """
    #: Current local time in seconds that was used to compare timestamps.
    localtime_in_seconds = None
    www_authenticate = None

    def __init__(self, *args, **kw):
        self.localtime_in_seconds = kw.pop('localtime_in_seconds')
        self.www_authenticate = kw.pop('www_authenticate')
        super(HawkFail, self).__init__(*args, **kw)


class AlreadyProcessed(HawkFail):
    """
    The message has already been processed and cannot be re-processed.

    See :ref:`nonce` for details.
    """
