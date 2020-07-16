import time
from typing import Iterable

from flask import g, request
from flask_mico.error import (AuthenticationRequiredError, HTTPStatus,
                              InvalidParameterError)
from flask_mico.log import logger

from core.common.utils import plain2md5
from core.models.user import User


class Cors:
    def __init__(self):
        self.headers = {
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Max-Age": 24 * 3600
        }

    def process_request(self):
        if request.method == 'OPTIONS':
            logger.debug("Cors process 'OPTIONS' request")
            raise HTTPStatus(body='\n', status=200, headers=self.headers)

    def process_response(self, resp):
        resp.headers.update(self.headers)
        return resp


class IgnorePathsMidMixin:
    def set_ignore_paths(self, paths: Iterable[str]):
        self._ignore_paths = paths

    def isignore(self, req_path) -> bool:
        for path in self._ignore_paths:
            if path in req_path:
                return True
        return False


class Authentication(IgnorePathsMidMixin):
    def __init__(self) -> None:
        self.set_ignore_paths(("/v1/login", "/v1/components"))

    def process_request(self):
        logger.debug("Authentication - %s", repr(request.method))
        if self.isignore(request.path):
            return
        username = request.cookies.get("username", None)
        if username is None:
            raise AuthenticationRequiredError()
        user = User.get_user(username)
        if not user:
            raise AuthenticationRequiredError()
        g.user = username


class VerifyApiSign(IgnorePathsMidMixin):
    def __init__(self) -> None:
        self.expired = 5 * 60  # second
        self.set_ignore_paths(("/v1/login",))

    def process_request(self):
        logger.debug("VerifySign - %s", repr(request.method))
        if self.isignore(request.path):
            return
        if request.method == "GET":
            sign = request.args.get("sign", None)
            ts = request.args.get("ts", None)
            req_data = request.args
        else:
            sign = g.data.get("sign", None)
            ts = g.data.get("ts", None)
            req_data = g.data

        if (not sign) or (not ts):
            raise InvalidParameterError("接口签名参数缺省")
        # verify ts
        if (time.time() - int(ts)) > self.expired:
            raise InvalidParameterError("接口超时")
        # verify sign
        sorted_data = ""
        for key in sorted(req_data.keys()):
            if key == "sign":
                continue
            sorted_data += (key + str(req_data[key]))
        sign_ = plain2md5(sorted_data).upper()
        if sign != sign_:
            raise InvalidParameterError("签名验证失败")
