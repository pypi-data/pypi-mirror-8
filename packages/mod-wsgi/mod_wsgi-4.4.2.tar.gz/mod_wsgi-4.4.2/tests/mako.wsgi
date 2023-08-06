from __future__ import print_function

import os
import cgi

from threading import Lock

from mako.lookup import TemplateLookup
from mako import exceptions

_template_lock = Lock()
_template_loaders = {}

def application(environ, start_response):
    # We want to use a mako template loader in order to load the actual
    # target file which the URL mapped to. This is so that it can handle
    # in memory caching as well as code caching between requests and
    # across processes. We want to tie the actual template loader to the
    # document root directory and any additional template directories
    # which we are being told to search for templates. We therefore need
    # to lazily create the template loader and then cache it for use in
    # subsequent requests.

    document_root = environ.get('DOCUMENT_ROOT')
    template_path = environ.get('mako.template_path', '')

    # Be optimistic first and see if it already exists with grabbing a
    # lock on the loaders cache.

    key = os.path.pathsep.join([document_root, template_path])

    loader = _template_loaders.get(key)

    if loader is None:
        # No loader exists already so we potentially need to
        # create one. This time we grab the lock for the loaders
        # cache.

        with _template_lock:
            # In case there was a race condition, we look up the cache
            # again for the loader.

            loader = _template_loaders.get(key)

            if loader is None:
                # We definitely need to create the loader the first time.
                # We setup the directories for the loader to search to be
                # the document root directory where target files will be,
                # plus any additional user defined directories.

                directories = [document_root]

                if template_path:
                    directories.extend(template_path.split(os.path.pathsep))

                # Optionally can setup a directory to store generated
                # Python code corresponding to a template for reuse across
                # processes. Also allow the internal memory cache size to
                # be specified.

                module_directory = environ.get('mako.module_directory')
                collection_size = int(environ.get('mako.cache_size', '100'))

                input_encoding = environ.get('mako.input_encoding')

            # Create the loader and store it back in the loader cache.

            loader = TemplateLookup(directories=directories,
                    module_directory=module_directory,
                    collection_size=collection_size,
                    input_encoding=input_encoding, output_encoding='utf-8')

            _template_loaders[key] = loader

    try:
        # Retrieve the the template object from the template loader
        # and render the template to get the response. Any request
        # params are passed in when rendering the template so they
        # are available.

        template = loader.get_template(environ['SCRIPT_NAME'])

        raw_params = cgi.FieldStorage(fp=environ['wsgi.input'],
                environ=environ, keep_blank_values=True)

        def getfield(f):
            if isinstance(f, list):
                return [getfield(x) for x in f]
            else:
                return f.value

        params = dict([(k, getfield(raw_params[k])) for k in raw_params])

        output = template.render(**params)

        status = '200 OK'
        response_headers = [
                ('Content-Type', 'text/html; charset="utf-8"'),
                ('Content-Length', str(len(output)))]

        start_response(status, response_headers)

        return [output]

    except exceptions.TopLevelLookupException:
        # This could only happen due to a race condition where the file
        # was remove in the split second when the request was being
        # handled as Apache will only pass the request off to us if the
        # file existed in the first place.

        output = b'Not Found'

        status = '404 Not Found'
        response_headers = [('Content-Type', 'text/plain'),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)

        return [output]

    except Exception:
        # Always log the details to the error log file.

        print('Error rendering file: %r' % environ['SCRIPT_FILENAME'])
        print(exceptions.text_error_template().render().strip())

        # If debug level is non zero then we also render and error
        # page back to the browser with the error details.

        debug_level = int(environ.get('mako.debug_level', '0'))

        if debug_level > 0:
            output = exceptions.html_error_template().render()
            output = output.encode('UTF-8')

            status = '500 Internal Server Error'
            response_headers = [
                    ('Content-Type', 'text/html; charset="utf-8"'),
                    ('Content-Length', str(len(output)))]

            start_response(status, response_headers)

            return [output]

        else:
            output = b'Internal Server Error'

            status = '500 Internal Server Error'
            response_headers = [
                    ('Content-Type', 'text/plain'),
                    ('Content-Length', str(len(output)))]

            start_response(status, response_headers)

            return [output]
