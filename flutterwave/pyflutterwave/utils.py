import requests
import json


def validate_post(res):
    if res.status_code == requests.codes.created:
        return res.json()
    else:
        res.raise_for_status()


def validate_get(res):
    if res.status_code == requests.codes.ok:
        return res.json()
    else:
        res.raise_for_status()


def build_params(**kwargs):
    params = {}
    for kw in kwargs:
        if kwargs[kw]:
            if kw.lower() == 'amount':
                params[kw] = kwargs[kw]
            elif isinstance(kwargs[kw], dict):
                params[kw] = build_params(**kwargs[kw])
            else:
                params[kw] = str(kwargs[kw], 'UTF-8') if isinstance(kwargs[kw], bytes) else kwargs[kw]

    return params
