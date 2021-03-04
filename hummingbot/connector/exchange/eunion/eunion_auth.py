import base64
import logging
import urllib
from datetime import datetime
import hashlib
import hmac
from typing import (
    Any,
    Dict
)
from urllib.parse import urlencode
from collections import OrderedDict

from hummingbot.logger import HummingbotLogger

EUNION_HOST_NAME = "api.eunion.pro"
hm_logger = None


class EunionAuth:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key: str = api_key
        self.hostname: str = EUNION_HOST_NAME
        self.secret_key: str = secret_key

    @classmethod
    def logger(cls) -> HummingbotLogger:
        global hm_logger
        if hm_logger is None:
            hm_logger = logging.getLogger(__name__)
        return hm_logger

    @staticmethod
    def keysort(dictionary: Dict[str, str]) -> Dict[str, str]:
        return OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))

    def add_auth_to_params(self,
                           method: str,
                           path_url: str,
                           args: Dict[str, Any] = None,
                           is_ws: bool = False) -> Dict[str, Any]:
        timestamp: str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        param_str: str = urllib.parse.urlencode(args)
        check_sum_str = "api_id=" + self.api_key + "&" + param_str + "&secret_key=" + self.secret_key
        if is_ws:
            params = {
                "accessKey": self.api_key,
                "signatureMethod": "HmacSHA256",
                "signatureVersion": "2.1",
                "timestamp": timestamp
            }
        else:
            params = {
                "api_id": self.api_key,
                "sign": hashlib.sha1(check_sum_str.encode('utf-8')).hexdigest()
            }
        if args is not None:
            params.update(args)

        return params

    def format_get_param_url(self, url: str, params: Dict[str, any]) -> str:

        param_str = urllib.parse.urlencode(params)
        self.logger().error("LOG" + param_str)

        return f"{url}?{param_str}"

    def generate_signature(self,
                           method: str,
                           path_url: str,
                           params: Dict[str, Any],
                           is_ws: bool = False) -> str:

        query_endpoint = f"/v1{path_url}" if not is_ws else path_url
        encoded_params_str = urlencode(params)
        payload = "\n".join([method.upper(), self.hostname, query_endpoint, encoded_params_str])
        signature = hmac.new(self.secret_key.encode("utf8"), payload.encode("utf8"), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode("utf8")

        return signature_b64
