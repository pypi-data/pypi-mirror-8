# coding:utf8

"""
Created on 2014-08-26

@author: tufei
@description:
         
Copyright (c) 2014 infohold inc. All rights reserved.
"""
import base64
import urllib
import json
from dhkit import log
from dhkit.error import Error
from tornado.httpclient import HTTPRequest, HTTPClient, HTTPError


class ApiError(Error):
    """
    """

    cls_code = -9999

    def __init__(self, msg=None, code=-1000, httpcode=None):
        super(ApiError, self).__init__(msg, code)
        self.httpcode = httpcode


class Api(object):

    _api_url = "http://localhost:9099"
    _client_key = "test"
    _client_secret = "ji9acGmkMe4u3lXteDPpo5Xti4QmM9"

    _access_token = None

    def __init__(self, api_url=None, timeout=30, use_gzip=True):
        self.api_url = api_url
        self.timeout = timeout
        self.use_gzip = use_gzip
        self.api_url = api_url or self._api_url

    def get(self, api_path, **kwargs):
        headers = {
            'Accept': "application/json",
            'Connection': 'Keep-Alive',
        }
        if self._access_token:
            headers['Authorization'] = "Bearer %s" % self._access_token
        if kwargs:
            url = "%s?%s" % (self.part_url(api_path), urllib.urlencode(kwargs))
        else:
            url = self.part_url(api_path)
        request = HTTPRequest(url, method="GET", headers=headers, connect_timeout=self.timeout,
                              request_timeout=self.timeout, use_gzip=True, validate_cert=False)
        return self.fetch(request)

    def post(self, api_path, **kwargs):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': "application/json",
            'Connection': 'Keep-Alive',
        }
        if self._access_token:
            headers['Authorization'] = "Bearer %s" % self._access_token
        url = self.part_url(api_path)
        body = kwargs and urllib.urlencode(kwargs) or None
        request = HTTPRequest(url, method="POST", headers=headers, body=body, connect_timeout=self.timeout,
                              request_timeout=self.timeout, use_gzip=True, validate_cert=False)
        return self.fetch(request)

        def fetch(self, request):
            http_client = HTTPClient()
            try:
                response = http_client.fetch(request)
                log.debug("Response code:[%d] body:[%s]" % (response.code, response.body))
                body = json.loads(response.body)
                if (not isinstance(body, dict)) and (not isinstance(body, list)):
                    raise TypeError("json.loads() result expected dict type or list type.")
                return body
            except HTTPError, e:
                log.exception("Fetch REST api http error")
                try:
                    body = json.loads(e.response.body)
                    if not isinstance(body, dict):
                        body = dict()
                except TypeError:
                    body = dict()
                raise ApiError(msg=body.get('return_message'), code=body.get('return_code'), httpcode=e.code)
            except TypeError, e:
                log.exception("Server return body is not json string")
                raise ApiError(msg="Server return body is not json string: %s" % e.message)

    def authorize(self, username, password):
        authorize_path = '/oauth/authorize'
        auth_header_value = "Bearer " + base64.b64encode("%s:%s" % (self._client_key, self._client_secret))
        headers = {
            "Authorization": auth_header_value,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Connection": "Keep-Alive",
        }
        url = self.part_url(authorize_path)
        body = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        body = urllib.urlencode(body)
        request = HTTPRequest(url, method="POST", headers=headers, body=body, connect_timeout=self.timeout,
                              request_timeout=self.timeout, use_gzip=True, validate_cert=False)
        auth_data = self.fetch(request)
        Api._access_token = auth_data.get("access_token")
        return auth_data

    def part_url(self, api_path):
        api_url = self.api_url[:-1] if self.api_url.endswith("/") else self.api_url
        return "%s%s" % (api_url, api_path)
