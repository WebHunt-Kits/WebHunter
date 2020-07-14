from flask import request
from flask_mico.error import HTTPStatus
from flask_mico.log import logger


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
