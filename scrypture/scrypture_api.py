# script_utils_api.py

import requests
import json
import logging
import urlparse

try:
    from scrypture import app
    API_BASE_URL = app.config['API_BASE_URL']
except:
    API_BASE_URL = 'http://localhost:5000/'

logging.basicConfig(level=logging.DEBUG)

class ScryptureAPI():
    def __init__(self,
                 base_url=API_BASE_URL,
                 username=None,
                 password=None,
                 interactive_password=False,
                 pass_auth=False):
        self.password = password
        self.username = username
        if interactive_password:
            import getpass
            self.password = getpass.getpass()
        if pass_auth != False:
            self.auth = pass_auth
        else:
            self.auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        self.BASE_URL = urlparse.urljoin(base_url, '/api/v2/')
        self.api_doc = self.get_api_docs()
        self.uris = {}
        self.api_funcs = {}
        for module, info in self.api_doc.items():
            self.uris[module] = urlparse.urljoin(self.BASE_URL, module)

            def make_api_func(module):
                def api_func(**kwargs):
                    json_kwargs = {kw : json.dumps(arg)
                                  for kw,arg in kwargs.items()}
                    uri = self.uris[module]
                    output = self.post_parse(uri, data=kwargs)
                    return  output
                return api_func

            api_func = make_api_func(module)
            api_func.__name__ = str(module)
            api_func.func_name = str(module)
            api_func.__doc__ = str(info['__doc__'])
            self.api_funcs[module] = api_func
            setattr(self, module, api_func)

    def _generate_uri(self, script_name, **kwargs):
        return self.uris[script_name].format(**kwargs)

    def get_api_docs(self):
        # first, request latest version number, instead of hardcoding v1
        api_doc_url = urlparse.urljoin(self.BASE_URL, '/api/v2/docs')
        return self.get_parse(api_doc_url)

    def get(self, uri, params={}):
        '''A generic method to make GET requests'''
        logging.debug("Requesting URL: "+str(urlparse.urljoin(self.BASE_URL, uri)))
        return requests.get(urlparse.urljoin(self.BASE_URL, uri),
            params=params, verify=False,
            auth=self.auth)

    def post(self, uri, params={}, data={}):
        '''A generic method to make POST requests on the given URI.'''
        return requests.post(
            urlparse.urljoin(self.BASE_URL, uri),
            params=params, data=json.dumps(data), verify=False,
            auth=self.auth, headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})

    def _request_parse(self, method, *args):
        r = method(*args)
        r.raise_for_status()
        return r.json()

    def get_parse(self, uri, params={}):
        '''Convenience method to call get() on an arbitrary URI and parse the response into a JSON object. Raises an error on non-200 response status.
        '''
        return self._request_parse(self.get, uri, params)

    def post_parse(self, uri, params={}, data={}):
        '''Convenience method to call post() on an arbitrary URI and parse the response
        into a JSON object. Raises an error on non-200 response status.
        '''
        return self._request_parse(self.post, uri, params, data)



if __name__ == '__main__':
    foo = ScryptureAPI()
