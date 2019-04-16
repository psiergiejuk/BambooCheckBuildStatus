#!/usr/bin/env python
#! -*- coding:utf-8 -*-

"""
TODO: Short description

TODO: Details description
"""

#TODO: all import block
import sys
import requests

__author__ = "Paweł Siergiejuk"
__date__ = "16/04/2019"
__version__ = "v0.0"
__email__ = "pawelsiergiejuk@gmail.com"
__status__ = "Development"

class NetException(Exception):
    def __init__(self, value): 
        self.value = value 
  
    def __str__(self): 
        return(repr(self.value)) 


class BambooStatus:
    SETUP = "setup"
    PORT = "port"
    URL = "url"
    USER = "user"
    PASSWD = "passwd"
    HEADERS = {'Accept': 'application/json'}
    
    def __init__(self, config):
        self.url = config.get(self.SETUP, self.URL)
        self.port = config.getint(self.SETUP, self.PORT)
        self.user = config.get(self.SETUP, self.USER)
        self.passwd = config.get(self.SETUP, self.PASSWD)
        self.session = requests.Session()
        self.session.auth = (self.user, self.passwd)

    def __get_data_from_url__(self, url):
        """Method that get data from url"""
        request = self.session.get(url, headers=self.HEADERS)
        if request.status_code != 200:
            raise NetException(request.reason)
        return request.text

if __name__ == "__main__":
    sys.exit()


