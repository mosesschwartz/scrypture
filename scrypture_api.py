# script_utils_api.py

import requests
import json
import logging
import urlparse

logging.basicConfig(level=logging.DEBUG)

class ScryptureAPI():
    def __init__(self,
             base_url='http://localhost:5000',
             username=None,
             password=None,
             interactive_password=False):
        self.password = password
        self.username = username
        if interactive_password:
            import getpass
            self.password = getpass.getpass()
        self.BASE_URL = base_url
        self.api_doc = self.get_api_docs()
        self.uris = {}
        self.api_funcs = {}
        for module, info in self.api_doc.items():
            self.uris[module] = urlparse.urljoin(self.BASE_URL, module)
            self.uris[module] += '?' + '&'.join([arg[0]+'={'+arg[0]+'}' for arg in info['args']])

            def make_api_func(module):
                def api_func(**kwargs):
                    json_kwargs = {kw : json.dumps(arg)
                                  for kw,arg in kwargs.items()}
                    uri = self._generate_uri(module, **json_kwargs)
                    return self.get_parse(uri)
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
        api_doc_url = urlparse.urljoin(self.BASE_URL, '/api/v1/docs')
        return self.get_parse(api_doc_url)

    def get(self, uri, params={}):
        '''A generic method to make GET requests'''
        logging.debug("Requesting URL: "+str(urlparse.urljoin(self.BASE_URL, uri)))
        return requests.get(urlparse.urljoin(self.BASE_URL, uri),
            params=params, verify=False,
            auth=requests.auth.HTTPBasicAuth(self.username, self.password))

    def post(self, uri, params={}, data={}):
        '''A generic method to make POST requests on the given URI.'''
        return requests.post(
            urlparse.urljoin(UmbrellaAPI.BASE_URL, uri),
            params=params, data=data, headers=self._auth_header, verify=False,
            auth=requests.auth.HTTPBasicAuth(self.username, self.password))

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

