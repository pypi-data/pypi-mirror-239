import requests
import urllib3
import logging
from requests.exceptions import ProxyError


from json.decoder import JSONDecodeError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
"""
A restful client that returns a response for any json type rest API
"""
class RestClient(object):

    def __init__(self, host, port=None, base_uri='/', use_ssl=True, auth=None, verify=True):

        if type(verify) is not bool:
            raise ValueError("Verify SSL must be of type bool")

        if type(port) is not int:
            raise ValueError("Port must be of type int")

        self.host = host
        
        if not port and use_ssl:
            self.port = 443
        elif not port and not use_ssl:
            self.port = 80
        else:
            self.port = port
        
        self.base_uri = base_uri
        self.auth = auth

        self.ssl_verify = verify
        self.use_ssl = use_ssl

        
        self.base_url = '%s:%s%s' % (self.host, self.port, self.base_uri)

        if use_ssl:
            self.base_url = 'https://%s' % self.base_url
        else:
            self.base_url = 'http://%s' % self.base_url

        self.session = None
        self.session = self._getSession()

    def _getSession(self):
        """ Create a session using basic auth

        :return:
            - :class:`requests.Session` object
        """
        if not self.session:
            s = requests.session()

            if self.auth != None:
                s.auth = self.auth
        else:
            s = self.session

        return s

    def endpoint(self, endpoint):
        """ Creates a new endpoint
        :param api_path: Path to the API 
        :return:
            - :class:`Endpoint` object
        
        """
        return Endpoint(self.base_url, endpoint, self.session, verify=self.ssl_verify)


"""
API JSON Repsonse
"""


class JSONResponse(object):

    def __init__(self, status_code, content):
        self._current_item = 0
        self._status_code = status_code
        self._itemlist = []
        if isinstance(content, list):
            content = {'results': content}

        self.raw = content
        if isinstance(content, dict):
            self._parse_result(content)
            #logging.info(self._itemlist)

    @property
    def status_code(self) -> int:
        '''Returns the status code of the request for the endpoint
           :param content: JSON response from the API Call
           :return:
              - :int: Returns the status code of the api call
        '''
        return self._status_code

    def __iter__(self):
        for i in dict(self._itemlist):
            c = getattr(self, i)
            if isinstance(c, JSONResponse):
                yield i, dict(c)

            elif isinstance(c, list) and all(
                isinstance(i, JSONDecodeError) for i in c
            ):
                yield i, [ dict(x) for x in c ]
            else:
                yield i, c


    def _parse_result(self, content):
        '''Parses the json respnse of the rest client and builds a class object for each time'''
        try:
            if isinstance(content, dict):
                for k, v in content.items():
                    if isinstance(v,dict):
                        v = JSONResponse(self._status_code, v)

                        self._itemlist.append((k, v))
                    elif isinstance(v, list):
                        v = [ JSONResponse(self.status_code, x) for x in v ]
                        self._itemlist.append((k,list(v)))
                    else:
                        self._itemlist.append((k, v))
                        
                    setattr(self, k, v)
        except JSONDecodeError:
            pass

"""
Class that represents an API endpoint response.

"""
class Endpoint(object):
    def __init__(self, base_url, endpoint_path, session, verify=True, **kwargs):
        self.base_url = base_url
        self.endpoint_path = endpoint_path
        self.session = session

        self.endpoint = '%s%s' % (self.base_url, self.endpoint_path)
        self.verify = verify
        self.kwargs = kwargs
        self._response = None

    @property
    def path(self):
        return '%s' % self.base_url

    def _request(self,output, headers=None):
        logging.debug('getting endpoint: {}'.format(self.endpoint))
        try:
            if headers and not type(headers) is dict:
                headers = {}
            self._response = self.session.get(self.endpoint, verify=self.verify, headers=headers)
        except ProxyError as pe:
            logging.debug('Proxy Error: %r' % pe.__dict__.keys())
            logging.debug('Proxy Error response: %r' % pe.response)
            self._response = pe.response

        if not self._response:
            return JSONResponse(503, {})

        logging.debug('Json Response: {}'.format(self._response.__dict__.get('json', None)))
        if output == 'json':
            try: 
                logging.debug('Building JSON Response')
                return JSONResponse(self._response.status_code, self._response.json())
            except ValueError:
                return self._response
        else:
            logging.debug('Returning Response')
            return self._response

        return None

    def get(self, output='json', headers=None):
        return self._request(output, headers=headers)
