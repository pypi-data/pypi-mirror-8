import time

def application(environ, start_response):
    status = '200 OK'

    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    line = (78*'X')+'\n'

    yield line
    yield line
    yield line
    yield line
    yield line

    print('pause')

    time.sleep(30.0)

    print('resume')

    for i in range(10000000):
        yield line

    print('done')
