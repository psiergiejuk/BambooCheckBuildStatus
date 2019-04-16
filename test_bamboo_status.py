#!/usr/bin/env python
#! -*- coding:utf-8 -*-

"""
Test of bamboo_status
"""

import pytest
import configparser
from mockito import when, mock, unstub, verify, patch
from bamboo_status import BambooStatus, NetException

__author__ = "Paweł Siergiejuk"
__date__ = "16/04/2019"
__version__ = "v0.0"
__email__ = "pawelsiergiejuk@gmail.com"
__status__ = "Development"

DATA = {BambooStatus.URL: "localhost",
        BambooStatus.PORT: 9887,
        BambooStatus.USER: "test",
        BambooStatus.PASSWD: "test1",
        }
CONFIG = configparser.ConfigParser()
CONFIG[BambooStatus.SETUP] = DATA
TEXT = "OK"
URL = "test.test"

def test_set_url_port():
    """Check method that read data from config"""
    bamboo = BambooStatus(CONFIG)
    assert bamboo.url == DATA[BambooStatus.URL]
    assert bamboo.port == DATA[BambooStatus.PORT]
    assert bamboo.user == DATA[BambooStatus.USER]
    assert bamboo.passwd == DATA[BambooStatus.PASSWD]

def test_auth_on_session():
    """Check do we setup auth on seesion"""
    bamboo = BambooStatus(CONFIG)
    assert bamboo.session.auth == (DATA[BambooStatus.USER], DATA[BambooStatus.PASSWD])

def test_get_data_from_url():
    """Check do method __get_data_from_url__"""
    bamboo = BambooStatus(CONFIG)
    session = mock()
    response = mock({'status_code': 200, 'text': TEXT})
    when(session).get(...).thenReturn(response)
    bamboo.session = session
    text = bamboo.__get_data_from_url__(URL)
    verify(session).get(URL, headers=bamboo.HEADERS)
    assert text == TEXT
    #clean up
    unstub()

def test_get_data_from_url_error():
    """Check method __get_data_from_url__ error handling"""
    bamboo = BambooStatus(CONFIG)
    session = mock()
    response = mock({'status_code': 404, 'reason': TEXT})
    when(session).get(...).thenReturn(response)
    bamboo.session = session
    with pytest.raises(NetException):
        text = bamboo.__get_data_from_url__(URL)
    #clean up
    unstub()
    
def test_get_build_result():
    """Check get_build_result method"""
    test_json = "{'results': ['1', '2'], 'size':2}"
    bamboo = BambooStatus(CONFIG)
    session = mock()
    response = mock({'status_code': 200, 'text': test_json})
    when(session).get(...).thenReturn(response)
    bamboo.session = session
    data = bamboo.get_build_result("TEST")
    assert data == ['1', '2']
    verify(session).get("http://localhost:9887/rest/api/latest/result/TEST")

def test_get_url():
    """Check get_url method"""
    bamboo = BambooStatus(CONFIG)
    assert bamboo.get_url("test") == "http://localhost:9887/test"
    
    
