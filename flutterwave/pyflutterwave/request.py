from .auth import BearerTokenAuth
import requests

class FlutterWaveRequest:
    def __init__(self, **kwargs):
        self.req_headers = kwargs.get(
            'req_headers',
            {'Content-Type': 'application/json'}
        )
        self.__auth = kwargs.get('request_auth_cls', BearerTokenAuth)(**kwargs)
        self.__message = ''
        self.__status = ''
        self.__data = {}

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def auth(self):
        return self.__auth

    @property
    def headers(self):
        return self.req_headers

    def get(self, url, payload=None, **kwargs):
        """
        Send a GET request to Flutterwave's server
        :param url: Flutterwave's API URL ('https://api.flutterwave.com/v3/')
        :param payload: JSON Payload to add to request

        """
        timeout = kwargs.get('timeout', 5)

        res = requests.get(
            url=url, params=payload, timeout=timeout, headers=self.headers,
            auth=self.auth
        )

        self.save_response(res)

        return res.json()

    def post(self, url, json, **kwargs):
        """
        Send a POST request to Flutterwave's server
        :param url: Flutterwave's API URL ('https://api.flutterwave.com/v3/')
        :param payload: JSON Payload to add to request

        """
        timeout = kwargs.get('timeout', 5)

        res = requests.post(
            url=url, json=json, timeout=timeout, headers=self.req_headers,
            auth=self.auth
        )

        self.save_response(res)
        return res.json

    @staticmethod
    def put(url, data, **kwargs):
        timeout = kwargs.get('timeout', 0.001)
        r = requests.put(url=url, data=data, timeout=timeout)
        return r

    def save_response(self, res):
        data = res.json()
        self.status = data.get('status', '')
        self.message = data.get('message', '')
        self.data = data.get('data', {})
