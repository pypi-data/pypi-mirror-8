def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

class C(object):
    pass

class Pool(object):
    def __init__(self):
        self.myimport = __import__
    def __del__(self):
        mod_wsgi = self.myimport('mod_wsgi')
        print('del in %r' % mod_wsgi.application_group)
        list()

import mod_wsgi
print('init %r' % mod_wsgi.application_group)

C.pool = Pool()
