import time

def application(environ, start_response):
    status = '200 OK'

    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    line = '01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    yield line
    yield line
    yield line
    yield line
    yield line

    print('pause')

    #time.sleep(30.0)

    print('resume')

    for i in xrange(100000000):
        yield line

    print('done')
