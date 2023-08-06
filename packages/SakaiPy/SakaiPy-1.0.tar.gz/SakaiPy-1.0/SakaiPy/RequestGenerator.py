#!/usr/bin/python
# -*- coding: utf-8 -*-
import mechanize
import cookielib
import requests

try:
    import simplejson as json
except ImportError:
    import json

br = mechanize.Browser()

cj = cookielib.LWPCookieJar()

baseURL=""


class RequestGenerator(object):
    """This class will handle generating the neccasary requests and cookie generation"""

    # Browser

    br.set_cookiejar(cj)

    def __init__(self, connectionInfo):
        wPage = br.open(connectionInfo['loginURL'])
        self.baseURL=connectionInfo['baseURL']

        html = wPage.read()
        br.select_form(nr=0)

        br.form['username'] = connectionInfo['username']
        br.form['password'] = connectionInfo['password']
        br.submit()

    def executeRequest(self, url):
        """Returns the JSON response from the specified URL."""

        response = requests.get(self.baseURL+url, cookies=cj)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return 'SHIT BROKE'



			