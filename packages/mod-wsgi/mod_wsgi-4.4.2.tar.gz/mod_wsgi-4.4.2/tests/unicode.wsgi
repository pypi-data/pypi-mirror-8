#!/usr/bin/python
# coding: utf-8

import os

filename = u"/tmp/äöü.gif"

def minimal_application(environ, start_response):
    start_response('200 OK', [('content-type', 'text/plain')])
    os.stat(filename)
    return (filename, )

application = minimal_application
