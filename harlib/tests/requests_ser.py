#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# harlib
# Copyright (c) 2014, Andrew Robbins, All rights reserved.
# 
# This library ("it") is free software; it is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License ("LGPLv3") <https://www.gnu.org/licenses/lgpl.html>.
'''
harlib - HTTP Archive (HAR) format library
'''
from __future__ import absolute_import

import json
import requests
import unittest
import harlib.api
import six

try:
    import urllib3
except:
    from requests.packages import urllib3

from harlib.tests.utils import TestUtils


def response_from_exception(err):
    resp = err.response \
        if hasattr(err, 'response') \
        and err.response != None \
        else requests.models.Response()
    resp.request = err.request \
        if hasattr(err, 'request') \
        and err.request != None else None
    resp._error = err
    return resp


class TestRequestsResponse2(TestUtils):

    def setUp(self):
        try:
            self.resp = requests.post('http://httpbin.org/post',
                                      data={'username': 'bob', 'password': 'yes'},
                                      headers={'X-File': 'requests'})
        except requests.exceptions.RequestException as err:
            self.resp = response_from_exception(err)

    def tearDown(self):
        pass

    def test_1_from_requests(self):
        
        with open('./temp.har', 'wb') as writer:
            codec = harlib.codecs.requests.RequestsCodec()
            codec.serialize(writer, self.resp, harlib.HarEntry)
            
        with open('./temp.har', 'rb') as reader:
            har_entry = harlib.api.load(reader)

        har_resp = har_entry.response
        self.assertEqual(har_resp.status, self.resp.status_code)
        self.assertEqual(har_resp.status, self.resp.status_code)
        self.assertEqual(har_resp.statusText, self.resp.reason)
        self.assertEqual(har_resp.httpVersion, "HTTP/1.1")
        self.assertEqual(har_resp.get_header("Content-Type"), "application/json")
        self.assertEqual(har_resp.content.mimeType, "application/json")
        
        json_resp = json.loads(har_resp.content.text)
        #print(har_resp.content.text)
        #self.assertEqual(json_resp["headers"]["Connection"], "keep-alive")
        self.assertEqual(json_resp["url"], "http://httpbin.org/post")
        self.assertEqual(json_resp["headers"]["Host"], "httpbin.org")
        self.assertEqual(json_resp["headers"]["X-File"], "requests")
        self.assertEqual(json_resp["headers"]["Content-Type"], 
                         "application/x-www-form-urlencoded")
        self.assertTrue(json_resp["headers"]["User-Agent"]
                        .startswith("python-requests"))

    #def test_2_to_requests(self):
    #    har_resp = harlib.HarEntry(self.resp)
    #    to_resp = har_resp.encode(requests.Response)
    #    self.assertEqualResponse(to_resp, self.resp)


#class TestRequestsSession(unittest.TestCase):
#
#    def setUp(self):
#        pass
#
#    def tearDown(self):
#        pass
#
#    def testNone(self):
#        self.assertTrue(True)
#
#
#
#    def test_1_from_requests():
#
#    def test_1_to_json
#    def test_1_from_json
#    def test_1_to_urllib3
#    def test_1_from_urllib3
#    def test_1_to_django
#    def test_1_from_django

if __name__ == '__main__':
    unittest.main(verbosity=2)