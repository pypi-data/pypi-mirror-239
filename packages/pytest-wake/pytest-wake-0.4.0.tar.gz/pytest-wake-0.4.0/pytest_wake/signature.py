#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import hashlib
import hmac
import json
import time

from .exception import UnImplementedMethodError, UnSupportVersionError
from .utils import url_split


class SignatureImpl:
    def __init__(self, api_key: str, api_secret: str, recv_window: int = 50000) -> None:
        if not api_key or not api_secret:
            raise PermissionError("Authenticated endpoints require keys.")
        self.api_key = api_key
        self.api_secret = bytes(api_secret, encoding="utf8")
        self.recv_window = recv_window

    def generate(self, method: str, url: str, params_or_body: dict, timestamp: int = None) -> str:
        self.now_timestamp = self.get_now_timestamp()

        if "/v3" in url or "/v5" in url:
            if method == "get":
                if params_or_body:
                    params = params_or_body
                else:
                    _, params = url_split(url)
                query = ""
                for k, v in params.items():
                    tmp = f"&{k}={v}"
                    query += tmp
                query = query[1:]
                sign_str = str(self.now_timestamp) + self.api_key + str(self.recv_window) + query
            elif method == "post":
                sign_str = str(self.now_timestamp) + str(self.api_key) + str(self.recv_window) + json.dumps(params_or_body)
            else:
                raise UnImplementedMethodError(f"Unimplemented request method yet: {method}")
            signature = hmac.new(self.api_secret, sign_str.encode("utf-8"), hashlib.sha256).hexdigest()
            return signature
        else:
            raise UnSupportVersionError(f"Unrecognized request url: {url}")

    def get_now_timestamp(self) -> int:
        """
        Return a millisecond integer timestamp.
        """
        return int(time.time() * 10**3)

    def get_auth_headers(self, sign) -> dict:
        headers = {
            "Content-Type": "application/json",
            "X-BAPI-SIGN": sign,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-TIMESTAMP": str(self.now_timestamp) if hasattr(self, "now_timestamp") else None,
            "X-BAPI-RECV-WINDOW": str(self.recv_window),
        }
        return headers
