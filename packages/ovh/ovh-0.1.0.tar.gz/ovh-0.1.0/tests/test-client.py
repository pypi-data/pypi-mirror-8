# -*- encoding: utf-8 -*-
#
# Copyright (c) 2013-2014, OVH SAS.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of OVH SAS nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY OVH SAS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL OVH SAS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
import requests
import mock
import json

from ovh.client import Client
from ovh.exceptions import (
    APIError, NetworkError, InvalidResponse, InvalidRegion, ReadOnlyError,
    ResourceNotFoundError, BadParametersError, ResourceConflictError, HTTPError,
    InvalidKey,
)

APPLICATION_KEY = 'fake application key'
APPLICATION_SECRET = 'fake application secret'
CONSUMER_KEY = 'fake consumer key'
ENDPOINT = 'ovh-eu'
ENDPOINT_BAD = 'laponie'
BASE_URL = 'https://eu.api.ovh.com/1.0'
FAKE_URL = 'http://gopher.ovh.net/'
FAKE_TIME = 1404395889.467238

FAKE_METHOD = 'MeThOd'
FAKE_PATH = '/unit/test'

class testClient(unittest.TestCase):
    def setUp(self):
        self.time_patch = mock.patch('time.time', return_value=FAKE_TIME)
        self.time_patch.start()

    def tearDown(self):
        self.time_patch.stop()

    ## test helpers

    def test_init(self):
        # nominal
        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, CONSUMER_KEY)
        self.assertEqual(APPLICATION_KEY, api._application_key)
        self.assertEqual(APPLICATION_SECRET, api._application_secret)
        self.assertEqual(CONSUMER_KEY, api._consumer_key)
        self.assertIsNone(api._time_delta)

        # invalid region
        self.assertRaises(InvalidRegion, Client, ENDPOINT_BAD, '', '', '')

    @mock.patch.object(Client, 'call')
    def test_time_delta(self, m_call):
        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, CONSUMER_KEY)
        m_call.return_value = 1404395895
        api._time_delta = None

        # nominal
        time_delta = api.time_delta
        m_call.assert_called_once_with('GET', '/auth/time', None, False)
        self.assertEqual(time_delta, 6)
        self.assertEqual(api._time_delta, 6)

        # ensure cache
        m_call.return_value = 0
        m_call.reset_mock()
        self.assertEqual(api.time_delta, 6)
        self.assertFalse(m_call.called)

    @mock.patch.object(Client, 'call')
    def test_request_consumerkey(self, m_call):
        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, CONSUMER_KEY)

        # nominal
        FAKE_RULES = object()
        FAKE_CK = object()
        RET = {'consumerKey': FAKE_CK}
        m_call.return_value = RET

        ret = api.request_consumerkey(FAKE_RULES, FAKE_URL)

        self.assertEqual(RET, ret)
        m_call.assert_called_once_with('POST', '/auth/credential', {
            'redirection': FAKE_URL,
            'accessRules': FAKE_RULES,
        }, False)

    ## test wrappers

    @mock.patch.object(Client, 'call')
    def test_get(self, m_call):
        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, CONSUMER_KEY)
        self.assertEqual(m_call.return_value, api.get(FAKE_URL))
        m_call.assert_called_once_with('GET', FAKE_URL, None, True)

    @mock.patch.object(Client, 'call')
    def test_delete(self, m_call):
        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, CONSUMER_KEY)
        self.assertEqual(m_call.return_value, api.delete(FAKE_URL))
        m_call.assert_called_once_with('DELETE', FAKE_URL, None, True)

    @mock.patch.object(Client, 'call')
    def test_post(self, m_call):
        PAYLOAD = {
            'arg1': object(),
            'arg2': object(),
            'arg3': object(),
        }

        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, CONSUMER_KEY)
        self.assertEqual(m_call.return_value, api.post(FAKE_URL, **PAYLOAD))
        m_call.assert_called_once_with('POST', FAKE_URL, PAYLOAD, True)

    @mock.patch.object(Client, 'call')
    def test_put(self, m_call):
        PAYLOAD = {
            'arg1': object(),
            'arg2': object(),
            'arg3': object(),
        }

        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, CONSUMER_KEY)
        self.assertEqual(m_call.return_value, api.put(FAKE_URL, **PAYLOAD))
        m_call.assert_called_once_with('PUT', FAKE_URL, PAYLOAD, True)

    ## test core function

    @mock.patch('ovh.client.request')
    def test_call_no_sign(self, m_req):
        m_res = m_req.return_value
        m_json = m_res.json.return_value

        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET)

        # nominal
        m_res.status_code = 200
        self.assertEqual(m_json, api.call(FAKE_METHOD, FAKE_PATH, None, False))
        m_req.assert_called_once_with(
            FAKE_METHOD, BASE_URL+'/unit/test',
            headers={'X-Ovh-Application': APPLICATION_KEY}, data=''
        )
        m_req.reset_mock()

        # data, nominal
        m_res.status_code = 200
        data = {'key': 'value'}
        j_data = json.dumps(data)
        self.assertEqual(m_json, api.call(FAKE_METHOD, FAKE_PATH, data, False))
        m_req.assert_called_once_with(
            FAKE_METHOD, BASE_URL+'/unit/test',
            headers={
                'X-Ovh-Application': APPLICATION_KEY,
                'Content-type': 'application/json',
            }, data=j_data
        )
        m_req.reset_mock()

        # request fails, somehow
        m_req.side_effect = requests.RequestException
        self.assertRaises(HTTPError, api.call, FAKE_METHOD, FAKE_PATH, None, False)
        m_req.side_effect = None

        # response decoding fails
        m_res.json.side_effect = ValueError
        self.assertRaises(InvalidResponse, api.call, FAKE_METHOD, FAKE_PATH, None, False)
        m_res.json.side_effect = None

        # HTTP errors
        m_res.status_code = 404
        self.assertRaises(ResourceNotFoundError, api.call, FAKE_METHOD, FAKE_PATH, None, False)
        m_res.status_code = 400
        self.assertRaises(BadParametersError, api.call, FAKE_METHOD, FAKE_PATH, None, False)
        m_res.status_code = 409
        self.assertRaises(ResourceConflictError, api.call, FAKE_METHOD, FAKE_PATH, None, False)
        m_res.status_code = 0
        self.assertRaises(NetworkError, api.call, FAKE_METHOD, FAKE_PATH, None, False)
        m_res.status_code = 99
        self.assertRaises(APIError, api.call, FAKE_METHOD, FAKE_PATH, None, False)
        m_res.status_code = 306
        self.assertRaises(APIError, api.call, FAKE_METHOD, FAKE_PATH, None, False)

    @mock.patch('ovh.client.request')
    @mock.patch('ovh.client.Client.time_delta', new_callable=mock.PropertyMock)
    def test_call_signature(self, m_time_delta, m_req):
        m_res = m_req.return_value
        m_json = m_res.json.return_value
        m_time_delta.return_value = 42

        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, CONSUMER_KEY)

        # nominal
        m_res.status_code = 200
        self.assertEqual(m_json, api.call(FAKE_METHOD, FAKE_PATH, None, True))
        m_time_delta.assert_called_once_with()
        m_req.assert_called_once_with(
            FAKE_METHOD, BASE_URL+'/unit/test',
            headers={
                'X-Ovh-Consumer': CONSUMER_KEY,
                'X-Ovh-Application': APPLICATION_KEY,
                'X-Ovh-Signature': '$1$16ae5ba8c63841b1951575be905867991d5f49dc',
                'X-Ovh-Timestamp': '1404395931',
            }, data=''
        )
        m_time_delta.reset_mock()
        m_req.reset_mock()


        # data, nominal
        data = data={'some': 'random', 'data': 42}
        m_res.status_code = 200
        self.assertEqual(m_json, api.call(FAKE_METHOD, FAKE_PATH, data, True))
        m_time_delta.assert_called_once_with()
        m_req.assert_called_once_with(
            FAKE_METHOD, BASE_URL+'/unit/test',
            headers={
                'X-Ovh-Consumer': CONSUMER_KEY,
                'X-Ovh-Application': APPLICATION_KEY,
                'Content-type': 'application/json',
                'X-Ovh-Timestamp': '1404395931',
                'X-Ovh-Signature': '$1$70e04549d8b9e3d7f499274090710206f8c87a78',
                }, data=json.dumps(data)
        )
        m_time_delta.reset_mock()
        m_req.reset_mock()

        # errors
        api = Client(ENDPOINT, APPLICATION_KEY, None, CONSUMER_KEY)
        self.assertRaises(InvalidKey, api.call, FAKE_METHOD, FAKE_PATH, None, True)
        api = Client(ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, None)
        self.assertRaises(InvalidKey, api.call, FAKE_METHOD, FAKE_PATH, None, True)

