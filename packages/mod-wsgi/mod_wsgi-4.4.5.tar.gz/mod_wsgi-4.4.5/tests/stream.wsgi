import time

def application(environ, start_response):
    status = '200 OK'

    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    for i in xrange(100):
        time.sleep(1.0)
        yield 'hello\n'
