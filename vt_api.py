""" VirusTotal API Module

This module provides API access to https://www.virustotal.com/vtapi/v2/.

"""

__author__ = "Charlie Aiken (charles.aiken@verizon.com)"
__version__ = "0.1.0"
__copyright__ = "Copyleft 2016 Charlie Aiken"
__license__ = "Free as in beer"

import os
import requests
import json
import time
import pprint

#requests.packages.urllib3.disable_warnings()

class RequestHandler():
    """ Method for making HTTP GET and POST requests using requests
    python module.
    """
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "TricksterBot/Wisakedjak 1.0"
    }
    epoch = None
    tokens = 4

    def __init__( self, proxy_user=None, proxy_pass=None, proxy_host=None,
        proxy_port=None, proxy_https=False ):
        """ Set up RequestHandler, including proxy settings.
        @param proxy_user: the proxy username, if required
        @param proxy_pass: the proxy password, if required
        @param proxy_host: required, if using a proxy
        @param proxy_port: the proxy port number, if required
        @param proxy_https: flag to specify an HTTPS connection to the
        proxy
        """
        self.epoch = time.time()
        self.proxy_url = None
        self.proxies = None
        if proxy_host is not None:
            if proxy_port is not None:
                proxy_setting = proxy_host + str(proxy_port)
            else:
                proxy_setting = proxy_host
            if proxy_user is not None and proxy_pass is not None:
                proxy_setting = (proxy_user + ':' + proxy_pass + '@'
                    + proxy_setting)
            if proxy_https:
                self.proxy_url = 'https://' + proxy_setting
            else:
                self.proxy_url = 'http://' + proxy_setting

            self.proxies = { 'http': self.proxy_url, 'https': self.proxy_url }

    @staticmethod
    def RateLimit( seconds ):
        if(time.time() - seconds) < 60:
            return True
        else:
            return False

    def getToken( self ):
        if self.tokens > 0:
            self.tokens = self.tokens - 1
        else:
            while self.RateLimit(self.epoch):
                time.sleep(5)
            self.tokens = 4
            self.epoch = time.time()

    def getRaw( self, url ):
        self.getToken()
        if self.proxies is not None:
            response = requests.get(url, proxies=self.proxies).text()
        else:
            response = requests.get(url).text()
        return response

    def get( self, url, kwargs ):
        self.getToken()
        if self.proxies is not None:
            response = json.loads(requests.get(url, params=kwargs,
                proxies=self.proxies).text)
        else:
            response = json.loads(requests.get(url, params=kwargs))
        return response

    def postFile( self, url, path, kwargs):
        self.getToken()
        if path is not None:
            files = { 'files': (
                os.path.basename(path),
                open(path, 'rb')
            )}
        if self.proxies is not None:
            response = requests.post(url, files=files, data=kwargs,
                proxies=self.proxies)
        else:
            response = requests.post(url, files=files, data=kwargs)

    def post( self, url, kwargs ):
        self.getToken()
        if self.proxies is not None:
            response = json.loads(requests.post(url, headers=self.headers,
                params=kwargs, proxies=self.proxies).text)
        else:
            response = json.loads(requests.post(url, headers=self.headers,
                params=kwargs).text)
        return response

class VirusTotal_API:
    """ Wrapper for VirusTotal API """
    host = 'https://www.virustotal.com'
    api_key = None

    def __init__( self, api_key=None, proxy_host=None, proxy_port=None,
        proxy_user=None, proxy_pass=None, proxy_https=False):
        """ Setup VirusTotal Object with API key and RequestHandler
        @param api_key: personal VirusTotal API key
        @param proxy_user: the proxy username, if required
        @param proxy_pass: the proxy password, if required
        @param proxy_host: required, if using a proxy
        @param proxy_port: the proxy port number, if required
        @param proxy_https: flag to specify an HTTPS connection to the
        proxy
        """
        self.api_key = api_key
        self.request_handler = RequestHandler(proxy_host=proxy_host,
            proxy_port=proxy_port, proxy_user=proxy_user, proxy_pass=proxy_pass,
            proxy_https=proxy_https)

    def bulkReport(self, url=None, query=[], step=None):
        start = 0
        end = step
        response = []
        while start < len(query):
            resource = ",".join(query[start:end]) if "file" in url \
                else "\n".join(query[start:end])
            params = {
                'apikey': self.api_key,
                'resource': resource
            }
            r = self.request_handler.post(url, params)
            if isinstance(r, list):
                [ response.append(report) for report in r ]
            else:
                response.append(r)
            start += step
            end += step
        return response


    def urlReport(self, query):
        url = "%s/vtapi/v2/url/report" % (self.host)
        if isinstance(query, list):
            response = self.bulkReport(url=url, query=query, step=4)
            return response
        params = {'apikey': self.api_key, 'resource': query}
        response = self.request_handler.post(url, params)
        return response

    def urlReportHits(self, query):
        json_data = self.urlReport(query)
        if isinstance(json_data, list):
            results = { r['url']: r['positives'] for r in json_data }
        else:
            results = json_data['positives']
        return results

    def urlReportVendors(self, query):
        json_data = self.urlReport(query)
        results = dict()
        urls = { r['url']: r['scans'] for r in json_data if r['positives'] > 0 }
        for url,scans in urls.iteritems():
            results[url] = [ vendor for vendor,res in scans.iteritems()
                if res['detected']  ]
        return results

    def urlReportFiles(self, query):
        json_data = self.urlReport(query)
        if isinstance(json_data, list):
            results = [ r['filescan_id'] for r in json_data
                if r['filescan_id'] is not None ]
        else:
            results = json_data['filescan_id']
        return results

    def fileReport(self, query):
        url = "%s/vtapi/v2/file/report" % (self.host)
        if isinstance(query, list):
            response = self.bulkReport(url=url, query=query, step=4)
            return response
        params = {'apikey': self.api_key, 'resource': query}
        response = self.request_handler.post(url, params)
        return response

    def fileReportHits(self, query):
        json_data = self.fileReport(query)
        if isinstance(json_data, list):
            results = { r['sha256']: r['positives'] for r in json_data }
        else:
            results = json_data['positives']
        return results

    def fileReportVendors(self, query):
        json_data = self.fileReport(query)
        results = dict()
        files = { r['sha256']: r['scans'] for r in json_data if r['positives'] > 0 }
        for file,scans in files.iteritems():
            results[file] = [ vendor for vendor,res in scans.iteritems()
                if res['detected']  ]
        return results
