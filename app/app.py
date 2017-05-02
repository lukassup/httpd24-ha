#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import random
import os

from flask import Flask, jsonify, request


app = Flask(__name__)
random = random.SystemRandom()


class UnexpectedError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super(self.__class__, self).__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(UnexpectedError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def chaos_monkey():
    num = random.gauss(1, 1)
    if num > 3:
        raise UnexpectedError('Oops!', 500)
    elif -num > 3:
        raise UnexpectedError('Sorry!', 400)
    return "{} -> {}".format(socket.gethostname(), request.remote_addr)


if __name__ == '__main__':
    app.run(
        host=os.environ.get('APP_HOST', '0.0.0.0'),
        port=os.environ.get('APP_PORT', 8888)
    )
