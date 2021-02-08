from .keys import Keys


class BearerTokenAuth(object):
    """
    This is a custom authentication class for `requests`. It adds bearer token
    to request headers for authentication.

    It requires a class that has a `secret_key` attribute representing the
    token to be used for authorization. By default, we use `Keys`
    """
    def __init__(self, key_cls=Keys, **kwargs):
        self._keys = key_cls(**kwargs)

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {token}'.format(token=self._keys.secret_key)
        return r
