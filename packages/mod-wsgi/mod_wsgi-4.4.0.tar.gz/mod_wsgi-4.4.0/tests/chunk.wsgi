def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!\n'

    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    for i in range(120):
        import time
        time.sleep(1.0)
        if i == 30:
            xxx
        yield output
