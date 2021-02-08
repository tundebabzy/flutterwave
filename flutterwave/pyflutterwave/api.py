from .request import FlutterWaveRequest
from .utils import build_params

class AccountVerification(object):
    def __init__(self, **kwargs):
        self.__base = FlutterWaveRequest(**kwargs)
        self.__url = 'https://api.flutterwave.com/v3/accounts/resolve'


    @property
    def ctx(self):
        return self.__base

    @property
    def url(self):
        return self.__url

    def verify(self, account_number, account_bank):
        params = build_params(**{'account_number': account_number, 'account_bank': account_bank})
        self.ctx.post(self.url, json=params)


"""
Use this to initiate a Flutterwave Payment.
"""
class Payment(object):
    def __init__(self, **kwargs):
        self.__base = FlutterWaveRequest(**kwargs)
        self.__url = 'https://api.flutterwave.com/v3/payments'
        self.__payment_url = ''
        self.__callback_url = ''

    @property
    def ctx(self):
        return self.__base

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    @property
    def callback_url(self):
        return self.__payment_url

    @callback_url.setter
    def payment_url(self, value):
        self.__payment_url = value

    @property
    def payment_url(self):
        return self.__payment_url

    @payment_url.setter
    def payment_url(self, value):
        self.__payment_url = value

    @property
    def request_code(self):
        return self.ctx.data.get('request_code')

    def __getattr__(self, item):
        return getattr(self.__base, item)

    def initiate(self, tx_ref, amount, payment_options, redirect_url,
                       customer, customizations, currency='NGN',
                       integrity_hash=None, payment_plan=None, subaccounts=None,
                       meta=None):

        # Note that `invoice_number` has to be an integer else it won't have
        # effect
        params = build_params(**{
            'tx_ref': tx_ref, 'amount': amount, 'payment_options': payment_options,
            'redirect_url': redirect_url, 'customer': customer, 'customizations': customizations,
            'currency': currency, 'integrity_hash': integrity_hash,
            'payment_plan': payment_plan, 'subaccounts': subaccounts,
            'meta': meta
        })

        self.ctx.post(self.url, json=params)

    def list_invoices(self, customer=None, paid=None, status=None, currency=None, include_archive=None):
        params = build_params(
            customer=customer, paid=paid, status=status, currency=currency, include_archive=include_archive)
        self.ctx.get(self.url, payload=params)


class TransactionVerification(object):
    def __init__(self, **kwargs):
        self.__base = FlutterWaveRequest(**kwargs)
        self.__url_prefix = 'https://api.flutterwave.com/v3/transactions'
        self.__url = ''

    @property
    def ctx(self):
        return self.__base

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = self.__url_prefix + '/{0}/verify'.format(value)

    def verify(self, tx_id):
        self.url = tx_id
        self.ctx.get(self.url)
