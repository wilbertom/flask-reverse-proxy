

class FlaskReverseProxied(object):

    def __init__(self, app=None):
        self.app = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.wsgi_app = ReverseProxied(self.app.wsgi_app)

        return self


class ReverseProxied(object):
    """
    Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:

    location /prefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /prefix;
        }

    :param app: the WSGI application
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ.get('PATH_INFO', '')
            if path_info and path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        server = environ.get('HTTP_X_FORWARDED_SERVER_CUSTOM', 
                             environ.get('HTTP_X_FORWARDED_SERVER', ''))
        if server:
            environ['HTTP_HOST'] = server

        scheme = environ.get('HTTP_X_SCHEME', '')

        if scheme:
            environ['wsgi.url_scheme'] = scheme

        return self.app(environ, start_response)
