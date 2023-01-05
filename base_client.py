#!/usr/bin/env python3
import requests as r  # import installed requests module
from requests.exceptions import HTTPError  # import requests exceptions
from requests.compat import urljoin  # could be usefull to create url…
import json


class Client:
    def __init__(self, baseUrl, defaultProtocol="http"):
        self.__baseUrl__ = baseUrl  # nom de domaine / Domain name
        self.__defaultProtocol__ = defaultProtocol  # Request protocol if not specified
        self.__r__ = None  # Server response
        self.__error__ = None  # errors

    # Changes the base url
    def set_baseurl(self, baseUrl):
        self.__baseUrl__ = baseUrl

    # Creates a url out of a Client object, a route and a protocol
    def make_url(self, route, protocol=None):
        if protocol == None:
            protocol = self.__defaultProtocol__
        baseurl = protocol + "://" + self.__baseUrl__
        url = urljoin(baseurl, route)
        return url  # Change in question 3

    # issues an http get request
    def get(self, route, payload={}, protocol=None):
        res = True
        try:
            # Stores in __r__ the response to the query
            self.__r__ = r.get(self.make_url(route, protocol), params=payload)
            print(self.__r__.url)
            # Deletes the last error (if an error is raised this is not executed)
            self.__error__ = None
        # possible errors
        except HTTPError as http_err:
            self.__error__ = f'HTTP error occurred: {http_err}'
            self.__r__ = None
            res = False
        except Exception as err:
            self.__error__ = f'Other error occurred: {err}'
            self.__r__ = None
            res = False
        return res

    # issues an http post request
    def post(self, route, data=None, protocol=None):
        res = True
        try:
            # Stores in __r__ the response to the query
            if data == None:
                self.__r__ = r.post(self.make_url(route, protocol))
            else:
                self.__r__ = r.post(self.make_url(
                    route, protocol), json=json.dumps(data))
            # Deletes the last error (if an error is raised this is not executed)
            self.__error__ = None
        # possible errors
        except HTTPError as http_err:
            self.__error__ = f'HTTP error occurred: {http_err}'
            self.__r__ = None
            res = False
        except Exception as err:
            self.__error__ = f'Other error occurred: {err}'
            self.__r__ = None
            res = False
        return res

    # issues an http delete request
    def delete(self, route, protocol=None):
        res = True
        try:
            # Stores in __r__ the response to the query
            self.__r__ = r.delete(self.make_url(route, protocol))
            # Deletes the last error (if an error is raised this is not executed)
            self.__error__ = None
        # possible errors
        except HTTPError as http_err:
            self.__error__ = f'HTTP error occurred: {http_err}'
            self.__r__ = None
            res = False
        except Exception as err:
            self.__error__ = f'Other error occurred: {err}'
            self.__r__ = None
            res = False
        return res

    # returns the last response to a succesful query
    def lr(self):
        return self.__r__

    # returns the last error raised by a query
    def lr_error(self):
        return self.__error__

    def lr_status_code(self):
        res = None
        if self.__r__ != None:
            res = self.__r__.status_code  # Change in question 4
        return res

    def lr_headers(self):
        res = None
        if self.__r__ != None:
            res = self.__r__.headers  # Change in question 5
        return res

    def lr_response(self, json=False):
        res = None
        if self.__r__ != None:
            res = self.__r__  # Change in question 7
            if json:
                res = self.__r__.json()
        return res
