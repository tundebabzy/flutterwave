from os import environ


class Keys(object):
    """
    This represents a Flutterwave account's keys.

    By default, `Keys` will look for the following environment variables to
    set its arguments if you do not supply any arguments when instantiating
    it:
    -	`secret_key`: `FLUTTERWAVE_SECRET_KEY`
    -	`public_key`: `FLUTTERWAVE_PUBLIC_KEY`
    -	`callback_url`: `FLUTTERWAVE_CALLBACK_URL`

    If you have the same information saved in an environment variable with a
    different name from what `Keys` is looking for, you can supply your
    environment variable name as the argument. e.g
    >>> Keys(secret_key='MY_OWN_ENVIRONMENT_VARIABLE_NAME', public_key='OTHER_ENVIRONMENT_VARIABLE')
    >>>

    Finally, you can just manually enter your Paystack keys. e.g
    >>> Keys(secret_key='sc_domain_topSEKrit', public_key='pk_domain_Ud0NtKNo')
    >>>
    """

    def __init__(self, secret_key='', public_key='', callback_url=''):
        """
        By default, the parameters are set as follows:
        -	`secret_key`: `FLUTTERWAVE_SECRET_KEY`
        -	`public_key`: `FLUTTERWAVE_PUBLIC_KEY`
        -	`callback_url`: `FLUTTERWAVE_CALLBACK_URL`

        You can supply your own matching environment variable names of just
        matching key.

        :param secret_key: String environment variable name containing FLutterwave
        secret key or Flutterwave secret key
        :param public_key: String environment variable name containing Flutterwave
        public key or Flutterwave public key
        :param callback_url: String environment variable name containing
        Flutterwave callback url or Flutterwave callback url
        """
        self._secret_key = environ.get(secret_key, secret_key)
        self._public_key = environ.get(public_key, public_key)
        self._callback_url = environ.get(callback_url, callback_url)

    @property
    def secret_key(self):
        return self._secret_key

    @property
    def public_key(self):
        return self._public_key

    @property
    def callback_url(self):
        return self._callback_url
