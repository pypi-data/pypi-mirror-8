#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
Copyright (c) 2003-2011 Ralph Meijer
Copyright (c) 2012, 2013 Jérôme Poisson


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
--

This program is based on Idavoll (http://idavoll.ik.nu/),
originaly written by Ralph Meijer (http://ralphm.net/blog/)
It is sublicensed under AGPL v3 (or any later version) as allowed by the original
license.

--

Here is a copy of the original license:

Copyright (c) 2003-2011 Ralph Meijer

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

"""
Tests for L{idavoll.gateway}.

Note that some tests are functional tests that require a running idavoll
service.
"""

from twisted.internet import defer
from twisted.trial import unittest
from twisted.web import error
from twisted.words.xish import domish

from sat_pubsub import gateway

AGENT = "Idavoll Test Script"
NS_ATOM = "http://www.w3.org/2005/Atom"

TEST_ENTRY = domish.Element((NS_ATOM, 'entry'))
TEST_ENTRY.addElement("id",
                      content="urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a")
TEST_ENTRY.addElement("title", content="Atom-Powered Robots Run Amok")
TEST_ENTRY.addElement("author").addElement("name", content="John Doe")
TEST_ENTRY.addElement("content", content="Some text.")

baseURI = "http://localhost:8086/"
componentJID = "pubsub"

class GatewayTest(unittest.TestCase):
    timeout = 2

    def setUp(self):
        self.client = gateway.GatewayClient(baseURI)
        self.client.startService()
        self.addCleanup(self.client.stopService)

        def trapConnectionRefused(failure):
            from twisted.internet.error import ConnectionRefusedError
            failure.trap(ConnectionRefusedError)
            raise unittest.SkipTest("Gateway to test against is not available")

        def trapNotFound(failure):
            from twisted.web.error import Error
            failure.trap(Error)

        d = self.client.ping()
        d.addErrback(trapConnectionRefused)
        d.addErrback(trapNotFound)
        return d


    def tearDown(self):
        return self.client.stopService()


    def test_create(self):

        def cb(response):
            self.assertIn('uri', response)

        d = self.client.create()
        d.addCallback(cb)
        return d

    def test_publish(self):

        def cb(response):
            self.assertIn('uri', response)

        d = self.client.publish(TEST_ENTRY)
        d.addCallback(cb)
        return d

    def test_publishExistingNode(self):

        def cb2(response, xmppURI):
            self.assertEquals(xmppURI, response['uri'])

        def cb1(response):
            xmppURI = response['uri']
            d = self.client.publish(TEST_ENTRY, xmppURI)
            d.addCallback(cb2, xmppURI)
            return d

        d = self.client.create()
        d.addCallback(cb1)
        return d

    def test_publishNonExisting(self):
        def cb(err):
            self.assertEqual('404', err.status)

        d = self.client.publish(TEST_ENTRY, 'xmpp:%s?node=test' % componentJID)
        self.assertFailure(d, error.Error)
        d.addCallback(cb)
        return d

    def test_delete(self):
        def cb(response):
            xmppURI = response['uri']
            d = self.client.delete(xmppURI)
            return d

        d = self.client.create()
        d.addCallback(cb)
        return d

    def test_deleteWithRedirect(self):
        def cb(response):
            xmppURI = response['uri']
            redirectURI = 'xmpp:%s?node=test' % componentJID
            d = self.client.delete(xmppURI, redirectURI)
            return d

        d = self.client.create()
        d.addCallback(cb)
        return d

    def test_deleteNotification(self):
        def onNotification(data, headers):
            try:
                self.assertTrue(headers.hasHeader('Event'))
                self.assertEquals(['DELETED'], headers.getRawHeaders('Event'))
                self.assertFalse(headers.hasHeader('Link'))
            except:
                self.client.deferred.errback()
            else:
                self.client.deferred.callback(None)

        def cb(response):
            xmppURI = response['uri']
            d = self.client.subscribe(xmppURI)
            d.addCallback(lambda _: xmppURI)
            return d

        def cb2(xmppURI):
            d = self.client.delete(xmppURI)
            return d

        self.client.callback = onNotification
        self.client.deferred = defer.Deferred()
        d = self.client.create()
        d.addCallback(cb)
        d.addCallback(cb2)
        return defer.gatherResults([d, self.client.deferred])

    def test_deleteNotificationWithRedirect(self):
        redirectURI = 'xmpp:%s?node=test' % componentJID

        def onNotification(data, headers):
            try:
                self.assertTrue(headers.hasHeader('Event'))
                self.assertEquals(['DELETED'], headers.getRawHeaders('Event'))
                self.assertEquals(['<%s>; rel=alternate' % redirectURI],
                                  headers.getRawHeaders('Link'))
            except:
                self.client.deferred.errback()
            else:
                self.client.deferred.callback(None)

        def cb(response):
            xmppURI = response['uri']
            d = self.client.subscribe(xmppURI)
            d.addCallback(lambda _: xmppURI)
            return d

        def cb2(xmppURI):
            d = self.client.delete(xmppURI, redirectURI)
            return d

        self.client.callback = onNotification
        self.client.deferred = defer.Deferred()
        d = self.client.create()
        d.addCallback(cb)
        d.addCallback(cb2)
        return defer.gatherResults([d, self.client.deferred])

    def test_list(self):
        d = self.client.listNodes()
        return d

    def test_subscribe(self):
        def cb(response):
            xmppURI = response['uri']
            d = self.client.subscribe(xmppURI)
            return d

        d = self.client.create()
        d.addCallback(cb)
        return d

    def test_subscribeGetNotification(self):

        def onNotification(data, headers):
            self.client.deferred.callback(None)

        def cb(response):
            xmppURI = response['uri']
            d = self.client.subscribe(xmppURI)
            d.addCallback(lambda _: xmppURI)
            return d

        def cb2(xmppURI):
            d = self.client.publish(TEST_ENTRY, xmppURI)
            return d


        self.client.callback = onNotification
        self.client.deferred = defer.Deferred()
        d = self.client.create()
        d.addCallback(cb)
        d.addCallback(cb2)
        return defer.gatherResults([d, self.client.deferred])


    def test_subscribeTwiceGetNotification(self):

        def onNotification1(data, headers):
            d = client1.stopService()
            d.chainDeferred(client1.deferred)

        def onNotification2(data, headers):
            d = client2.stopService()
            d.chainDeferred(client2.deferred)

        def cb(response):
            xmppURI = response['uri']
            d = client1.subscribe(xmppURI)
            d.addCallback(lambda _: xmppURI)
            return d

        def cb2(xmppURI):
            d = client2.subscribe(xmppURI)
            d.addCallback(lambda _: xmppURI)
            return d

        def cb3(xmppURI):
            d = self.client.publish(TEST_ENTRY, xmppURI)
            return d


        client1 = gateway.GatewayClient(baseURI, callbackPort=8088)
        client1.startService()
        client1.callback = onNotification1
        client1.deferred = defer.Deferred()
        client2 = gateway.GatewayClient(baseURI, callbackPort=8089)
        client2.startService()
        client2.callback = onNotification2
        client2.deferred = defer.Deferred()

        d = self.client.create()
        d.addCallback(cb)
        d.addCallback(cb2)
        d.addCallback(cb3)
        dl = defer.gatherResults([d, client1.deferred, client2.deferred])
        return dl


    def test_subscribeGetDelayedNotification(self):

        def onNotification(data, headers):
            self.client.deferred.callback(None)

        def cb(response):
            xmppURI = response['uri']
            self.assertNot(self.client.deferred.called)
            d = self.client.publish(TEST_ENTRY, xmppURI)
            d.addCallback(lambda _: xmppURI)
            return d

        def cb2(xmppURI):
            d = self.client.subscribe(xmppURI)
            return d


        self.client.callback = onNotification
        self.client.deferred = defer.Deferred()
        d = self.client.create()
        d.addCallback(cb)
        d.addCallback(cb2)
        return defer.gatherResults([d, self.client.deferred])

    def test_subscribeGetDelayedNotification2(self):
        """
        Test that subscribing as second results in a notification being sent.
        """

        def onNotification1(data, headers):
            client1.deferred.callback(None)
            client1.stopService()

        def onNotification2(data, headers):
            client2.deferred.callback(None)
            client2.stopService()

        def cb(response):
            xmppURI = response['uri']
            self.assertNot(client1.deferred.called)
            self.assertNot(client2.deferred.called)
            d = self.client.publish(TEST_ENTRY, xmppURI)
            d.addCallback(lambda _: xmppURI)
            return d

        def cb2(xmppURI):
            d = client1.subscribe(xmppURI)
            d.addCallback(lambda _: xmppURI)
            return d

        def cb3(xmppURI):
            d = client2.subscribe(xmppURI)
            return d

        client1 = gateway.GatewayClient(baseURI, callbackPort=8088)
        client1.startService()
        client1.callback = onNotification1
        client1.deferred = defer.Deferred()
        client2 = gateway.GatewayClient(baseURI, callbackPort=8089)
        client2.startService()
        client2.callback = onNotification2
        client2.deferred = defer.Deferred()


        d = self.client.create()
        d.addCallback(cb)
        d.addCallback(cb2)
        d.addCallback(cb3)
        dl = defer.gatherResults([d, client1.deferred, client2.deferred])
        return dl


    def test_subscribeNonExisting(self):
        def cb(err):
            self.assertEqual('403', err.status)

        d = self.client.subscribe('xmpp:%s?node=test' % componentJID)
        self.assertFailure(d, error.Error)
        d.addCallback(cb)
        return d


    def test_subscribeRootGetNotification(self):

        def onNotification(data, headers):
            self.client.deferred.callback(None)

        def cb(response):
            xmppURI = response['uri']
            jid, nodeIdentifier = gateway.getServiceAndNode(xmppURI)
            rootNode = gateway.getXMPPURI(jid, '')

            d = self.client.subscribe(rootNode)
            d.addCallback(lambda _: xmppURI)
            return d

        def cb2(xmppURI):
            return self.client.publish(TEST_ENTRY, xmppURI)


        self.client.callback = onNotification
        self.client.deferred = defer.Deferred()
        d = self.client.create()
        d.addCallback(cb)
        d.addCallback(cb2)
        return defer.gatherResults([d, self.client.deferred])


    def test_unsubscribeNonExisting(self):
        def cb(err):
            self.assertEqual('403', err.status)

        d = self.client.unsubscribe('xmpp:%s?node=test' % componentJID)
        self.assertFailure(d, error.Error)
        d.addCallback(cb)
        return d


    def test_items(self):
        def cb(response):
            xmppURI = response['uri']
            d = self.client.items(xmppURI)
            return d

        d = self.client.publish(TEST_ENTRY)
        d.addCallback(cb)
        return d


    def test_itemsMaxItems(self):
        def cb(response):
            xmppURI = response['uri']
            d = self.client.items(xmppURI, 2)
            return d

        d = self.client.publish(TEST_ENTRY)
        d.addCallback(cb)
        return d
