import binascii
import copy
import hmac
import json
import sys
import time
from datetime import datetime
from hashlib import sha256

import requests

from . import logger, InvokeError


if sys.version_info.major < 3:
    from urllib import quote, unquote

    def hmacsha256(keyByte, message):
        return hmac.new(keyByte, message, digestmod=sha256).digest()

    # Create a "String to Sign".
    def StringToSign(canonicalRequest, t):
        string = HexEncodeSHA256Hash(canonicalRequest)
        return "%s\n%s\n%s" % (Algorithm, datetime.strftime(t, BasicDateFormat), string)
else:
    from urllib.parse import quote, unquote

    def hmacsha256(keyByte, message):
        return hmac.new(keyByte.encode('utf-8'), message.encode('utf-8'), digestmod=sha256).digest()

    # Create a "String to Sign".
    def StringToSign(canonicalRequest, t):
        string = HexEncodeSHA256Hash(canonicalRequest.encode('utf-8'))
        return "%s\n%s\n%s" % (Algorithm, datetime.strftime(t, BasicDateFormat), string)


def urlencode(s):
    return quote(s, safe='~')


def findHeader(r, header):
    for k in r.headers:
        if k.lower() == header.lower():
            return r.headers[k]
    return None


# HexEncodeSHA256Hash returns hexcode of sha256
def HexEncodeSHA256Hash(data):
    sha256hash = sha256()
    sha256hash.update(data)
    return sha256hash.hexdigest()


# HWS API Gateway Signature
class HttpRequest:
    def __init__(self, method="", url="", headers=None, body=None):
        body = body or ""
        self.method = method
        spl = url.split("://", 1)
        scheme = 'http'
        if len(spl) > 1:
            scheme = spl[0]
            url = spl[1]
        query = {}
        spl = url.split('?', 1)
        url = spl[0]
        if len(spl) > 1:
            for kv in spl[1].split("&"):
                spl = kv.split("=", 1)
                key = spl[0]
                value = ""
                if len(spl) > 1:
                    value = spl[1]
                if key != '':
                    key = unquote(key)
                    value = unquote(value)
                    if key in query:
                        query[key].append(value)
                    else:
                        query[key] = [value]
        spl = url.split('/', 1)
        host = spl[0]
        if len(spl) > 1:
            url = '/' + spl[1]
        else:
            url = '/'

        self.scheme = scheme
        self.host = host
        self.uri = url
        self.query = query
        if headers is None:
            self.headers = {}
        else:
            self.headers = copy.deepcopy(headers)
        if sys.version_info.major < 3:
            self.body = body
        else:
            self.body = body.encode("utf-8")


BasicDateFormat = "%Y%m%dT%H%M%SZ"
Algorithm = "SDK-HMAC-SHA256"
HeaderXDate = "X-Sdk-Date"
HeaderHost = "host"
HeaderAuthorization = "Authorization"
HeaderContentSha256 = "x-sdk-content-sha256"


# Build a CanonicalRequest from a regular request string
#
# CanonicalRequest =
#  HTTPRequestMethod + '\n' +
#  CanonicalURI + '\n' +
#  CanonicalQueryString + '\n' +
#  CanonicalHeaders + '\n' +
#  SignedHeaders + '\n' +
#  HexEncode(Hash(RequestPayload))
def CanonicalRequest(r, signedHeaders):
    canonicalHeaders = CanonicalHeaders(r, signedHeaders)
    hexencode = findHeader(r, HeaderContentSha256)
    if hexencode is None:
        hexencode = HexEncodeSHA256Hash(r.body)
    return "%s\n%s\n%s\n%s\n%s\n%s" % (r.method.upper(), CanonicalURI(r), CanonicalQueryString(r),
                                       canonicalHeaders, ";".join(signedHeaders), hexencode)


def CanonicalURI(r):
    pattens = unquote(r.uri).split('/')
    uri = []
    for v in pattens:
        uri.append(urlencode(v))
    urlpath = "/".join(uri)
    if urlpath[-1] != '/':
        urlpath = urlpath + "/"  # always end with /
    # r.uri = urlpath
    return urlpath


def CanonicalQueryString(r):
    keys = []
    for key in r.query:
        keys.append(key)
    keys.sort()
    a = []
    for key in keys:
        k = urlencode(key)
        value = r.query[key]
        if type(value) is list:
            value.sort()
            for v in value:
                kv = k + "=" + urlencode(str(v))
                a.append(kv)
        else:
            kv = k + "=" + urlencode(str(value))
            a.append(kv)
    return '&'.join(a)


def CanonicalHeaders(r, signedHeaders):
    a = []
    __headers = {}
    for key in r.headers:
        keyEncoded = key.lower()
        value = r.headers[key]
        valueEncoded = value.strip()
        __headers[keyEncoded] = valueEncoded
        if sys.version_info.major == 3:
            r.headers[key] = valueEncoded.encode("utf-8").decode('iso-8859-1')
    for key in signedHeaders:
        a.append(key + ":" + __headers[key])
    return '\n'.join(a) + "\n"


def SignedHeaders(r):
    a = []
    for key in r.headers:
        a.append(key.lower())
    a.sort()
    return a


# Create the HWS Signature.
def SignStringToSign(stringToSign, signingKey):
    hm = hmacsha256(signingKey, stringToSign)
    return binascii.hexlify(hm).decode()


# Get the finalized value for the "Authorization" header.  The signature
# parameter is the output from SignStringToSign
def AuthHeaderValue(signature, AppKey, signedHeaders):
    return "%s Access=%s, SignedHeaders=%s, Signature=%s" % (
        Algorithm, AppKey, ";".join(signedHeaders), signature)


class Signer:
    def __init__(self):
        self.Key = ""
        self.Secret = ""

    def Verify(self, r, authorization):
        if sys.version_info.major == 3 and isinstance(r.body, str):
            r.body = r.body.encode('utf-8')
        headerTime = findHeader(r, HeaderXDate)
        if headerTime is None:
            return False
        else:
            t = datetime.strptime(headerTime, BasicDateFormat)

        signedHeaders = SignedHeaders(r)
        canonicalRequest = CanonicalRequest(r, signedHeaders)
        stringToSign = StringToSign(canonicalRequest, t)
        return authorization == SignStringToSign(stringToSign, self.Secret)

    # SignRequest set Authorization header
    def Sign(self, r):
        if sys.version_info.major == 3 and isinstance(r.body, str):
            r.body = r.body.encode('utf-8')
        headerTime = findHeader(r, HeaderXDate)
        if headerTime is None:
            t = datetime.utcnow()
            r.headers[HeaderXDate] = datetime.strftime(t, BasicDateFormat)
        else:
            t = datetime.strptime(headerTime, BasicDateFormat)

        haveHost = False
        for key in r.headers:
            if key.lower() == 'host':
                haveHost = True
                break
        if not haveHost:
            r.headers["host"] = r.host
        signedHeaders = SignedHeaders(r)
        canonicalRequest = CanonicalRequest(r, signedHeaders)
        stringToSign = StringToSign(canonicalRequest, t)
        signature = SignStringToSign(stringToSign, self.Secret)
        authValue = AuthHeaderValue(signature, self.Key, signedHeaders)
        r.headers[HeaderAuthorization] = authValue
        r.headers["content-length"] = str(len(r.body))
        queryString = CanonicalQueryString(r)
        if queryString != "":
            r.uri = r.uri + "?" + queryString


class HuaWeiHttpRequest:
    headers = {"content-type": "application/json"}

    def __init__(self, ak, sk):
        sig = Signer()
        sig.Key = ak
        sig.Secret = sk
        self.sig = sig

    def get(self, url, data=None, headers=None):
        headers = headers or self.headers
        data = data or {}
        query = "&".join([f"{key}={value}" for key, value in data.items()])
        if query:
            url += "?" + query
        return HttpRequest("GET", url, headers, body="")

    def post(self, url, data=None, headers=None):
        headers = headers or self.headers
        if isinstance(data, dict):
            data = json.dumps(data)
        return HttpRequest("POST", url, headers, body=data)

    def put(self, url, data, headers=None):
        if not data:
            raise ValueError("`data` must be a dict, and not null")
        if isinstance(data, dict):
            data = json.dumps(data)
        headers = headers or self.headers
        return HttpRequest("PUT", url, headers, body=data)

    def delete(self, url, _, headers=None):
        headers = headers or self.headers
        return HttpRequest("DELETE", url, headers)

    def request(self, method, url, data=None, headers=None):
        if not hasattr(self, method.lower()):
            raise ValueError(f"Unsupported method: {method}")
        r = getattr(self, method.lower())(url, data, headers)
        self.sig.Sign(r)
        response = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
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


def invoke(ak, sk, method, url, data=None, headers=None):
    hw_request = HuaWeiHttpRequest(ak, sk)
    response = hw_request.request(method, url, data, headers)
    logger.info(f"huawei api response: {response}")
    return response


def loop_invoke_check_condition(ak, sk, method, url, condition, data=None, headers=None):
    if not (("==" in condition) ^ ("!=" in condition)):
        raise ValueError("Conditions can contain only one of them ==, !=")
    symbol = "==" if "==" in condition else "!="
    field, value = condition.split(symbol)
    keys = field.split(".")
    times = 1
    while True:
        response = invoke(ak, sk, method, url, data, headers)
        tmp_resp = copy.deepcopy(response)
        for key in keys:
            if not (key and tmp_resp):
                raise ValueError(f"{key} not in response or not exists")
            if isinstance(tmp_resp, list) and key.isdigit():
                key = int(key)
                if key >= len(tmp_resp):
                    raise ValueError(f"{key} is out of range")
                tmp_resp = tmp_resp[key]
            else:
                tmp_resp = tmp_resp.get(key)
        if ((symbol == "==") and (tmp_resp == value)) or ((symbol == "!=") and (tmp_resp != value)):
            logger.warning(f"第{times}次请求结果, 判断条件: {tmp_resp}{symbol}{value}成立, 退出循环")
            del tmp_resp
            break
        logger.info(f"第{times}次请求结果, 判断条件: {tmp_resp}{symbol}{value}不成立, 等待下次请求...")
        time.sleep(10)
        times += 1
    return response
