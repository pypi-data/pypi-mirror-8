# By: Carlos Eduardo Moreira dos Santos, 2014.
# Based on: Kelcey Damage, 2012 & Kraig Amador, 2012
# Changes:
#   - ported to python3
#   - support for config.ini (url, key, secret)
#   - method calls work with no parameters
#   - pep8 compliance
#   - documentation

from expyrimenter import Config
from urllib.parse import quote_plus
from urllib.request import urlopen
from urllib.error import HTTPError
import base64
import hashlib
import hmac
import json
import logging
import string
import urllib


class SignedAPICall():
    def __init__(self, api_url, api_key, api_secret):
        self.url = api_url
        self.key = api_key
        self.secret = api_secret
        self._logger = logging.getLogger('cloudstack.api')

    def request(self, args):
        args['apiKey'] = self.key

        self.params = []
        self._sort_request(args)
        self._create_signature()
        self._build_post_request()

    def _sort_request(self, args):
        keys = sorted(args.keys())

        for key in keys:
            self.params.append(key + '=' + self._quote(args[key]))

    def _quote(self, value):
        if value is True:
            quoted = 'true'
        elif value is False:
            quoted = 'false'
        else:
            quoted = quote_plus(value)

        return quoted

    def _create_signature(self):
        self.query = '&'.join(self.params)
        digest = hmac.new(self.secret.encode(),
                          msg=self.query.lower().encode(),
                          digestmod=hashlib.sha1).digest()

        self.signature = base64.b64encode(digest)

    def _build_post_request(self):
        self.query += '&signature=' + quote_plus(self.signature)
        self.value = self.url + '?' + self.query


class API(SignedAPICall):
    def __init__(self):
        cfg = Config('api')
        super().__init__(cfg.get('url'), cfg.get('key'), cfg.get('secret'))

    def __getattr__(self, name):
        def handlerFunction(*args, **kwargs):
            if kwargs:
                return self._make_request(name, kwargs)
            if len(args) == 0:
                args = [{}]
            return self._make_request(name, args[0])
        return handlerFunction

    def _http_get(self, url):
        try:
            response = urlopen(url)
        except HTTPError:
            self._logger.error('Error getting "%s"' % url)
            raise

        return response.read()

    def _make_request(self, command, args):
        args['response'] = 'json'
        args['command'] = command
        self.request(args)
        data = self._http_get(self.value).decode()
        # The response is of the format {commandresponse: actual-data}
        key = command.lower() + "response"
        return json.loads(data)[key]
