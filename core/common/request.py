"""
requests patch
"""
import ssl

import requests
from urllib3 import disable_warnings


def remove_ssl_verify():
    ssl._create_default_https_context = ssl._create_unverified_context


def requests_patch(remove_ssl):
    if remove_ssl:
        remove_ssl_verify()
    disable_warnings()


requests_patch(True)
