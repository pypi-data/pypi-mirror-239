import binascii
import hashlib
import hmac
import json
import sys
from datetime import datetime

import requests

from . import logger, InvokeError


if sys.version_info.major < 3:
    from urllib import quote

    def hmacsha256(keyByte, message):
        return hmac.new(keyByte, message, digestmod=hashlib.sha256).digest()

else:
    from urllib.parse import quote

    def hmacsha256(keyByte, message):
        return hmac.new(keyByte.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()


def get_canonical_query_string(query):
    if query is None or len(query) <= 0:
        return ''
    canon_keys = []
    for k, v in query.items():
        if v is not None:
            canon_keys.append(k)

    canon_keys.sort()
    query_string = ''
    for key in canon_keys:
        value = quote(query[key], safe='~', encoding='utf-8')
        if value is None:
            s = f'{key}&'
        else:
            s = f'{key}={value}&'
        query_string += s
    return query_string[:-1]


def to_str(val):
    if val is None:
        return val

    if isinstance(val, bytes):
        return str(val, encoding='utf-8')
    else:
        return str(val)


def get_canonicalized_headers(headers):
    canon_keys = []
    tmp_headers = {}
    for k, v in headers.items():
        if v is not None:
            if k.lower() not in canon_keys:
                canon_keys.append(k.lower())
                tmp_headers[k.lower()] = [to_str(v).strip()]
            else:
                tmp_headers[k.lower()].append(to_str(v).strip())

    canon_keys.sort()
    canonical_headers = ''
    for key in canon_keys:
        header_entry = ','.join(sorted(tmp_headers[key]))
        s = f'{key}:{header_entry}\n'
        canonical_headers += s
    return canonical_headers, ';'.join(canon_keys)


def hex_encode(raw):
    return binascii.b2a_hex(raw).decode('utf-8')


def sha256hash(raw):
    if not isinstance(raw, (bytes, str)):
        raw = json.dumps(raw)
    if not isinstance(raw, bytes):
        raw = raw.encode("utf-8")
    return hex_encode(hashlib.sha256(raw).digest())


class Signer(object):
    def __init__(self, ak, sk):
        self.Key = ak
        self.Secret = sk

    # SignRequest set Authorization header
    def Sign(self, method, params, payload, headers):
        sign_type = "ACS3-HMAC-SHA256"
        canonical_uri = '/'
        canonicalized_query = get_canonical_query_string(params)
        canonicalized_headers, signed_headers = get_canonicalized_headers(headers)

        canonical_request = f'{method.upper()}\n' \
                            f'{canonical_uri}\n' \
                            f'{canonicalized_query}\n' \
                            f'{canonicalized_headers}\n' \
                            f'{signed_headers}\n' \
                            f'{payload}'
        str_to_sign = f'{sign_type}\n{sha256hash(canonical_request)}'
        signature = hex_encode(hmacsha256(self.Secret, str_to_sign))
        auth = f'{sign_type} Credential={self.Key},SignedHeaders={signed_headers},Signature={signature}'
        return auth


class AliHttpRequest:
    def __init__(self, ak, sk):
        self.sig = Signer(ak, sk)

    def request(self, method, host, params=None, payload=None, headers=None, **kwargs):
        headers = headers or {}
        payload = sha256hash(payload or '')
        headers["accept"] = "application/json"
        headers["x-acs-date"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        headers["x-acs-content-sha256"] = payload
        headers["host"] = host
        headers["Authorization"] = self.sig.Sign(method, params, payload, headers)
        response = requests.request(method, "https://" + host, params=params, headers=headers, **kwargs)
        return self.handle_response(response)

    def handle_response(self, response):
        status_code = response.status_code
        if status_code >= 200 and status_code < 300:
            logger.info(f"response status code: {status_code}")
            if response.content:
                return json.loads(response.content.decode())
        else:
            logger.error(f"response status code: {status_code}, detail error message: {response.text}")
            raise InvokeError(f"response status code: {status_code}, error message: {response.text}")


def invoke(ak, sk, method, host, params=None, data=None, headers=None, **kwargs):
    ali_request = AliHttpRequest(ak, sk)
    response = ali_request.request(method, host, params, data, headers, **kwargs)
    logger.info(f"alicloud api response: {response}")
    return response
