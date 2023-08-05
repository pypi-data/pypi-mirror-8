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
Tests for L{idavoll.memory_storage} and L{idavoll.pgsql_storage}.
"""

from zope.interface.verify import verifyObject
from twisted.trial import unittest
from twisted.words.protocols.jabber import jid
from twisted.internet import defer
from twisted.words.xish import domish

from sat_pubsub import error, iidavoll, const

OWNER = jid.JID('owner@example.com/Work')
SUBSCRIBER = jid.JID('subscriber@example.com/Home')
SUBSCRIBER_NEW = jid.JID('new@example.com/Home')
SUBSCRIBER_TO_BE_DELETED = jid.JID('to_be_deleted@example.com/Home')
SUBSCRIBER_PENDING = jid.JID('pending@example.com/Home')
PUBLISHER = jid.JID('publisher@example.com')
ITEM = domish.Element((None, 'item'))
ITEM['id'] = 'current'
ITEM.addElement(('testns', 'test'), content=u'Test \u2083 item')
ITEM_NEW = domish.Element((None, 'item'))
ITEM_NEW['id'] = 'new'
ITEM_NEW.addElement(('testns', 'test'), content=u'Test \u2083 item')
ITEM_UPDATED = domish.Element((None, 'item'))
ITEM_UPDATED['id'] = 'current'
ITEM_UPDATED.addElement(('testns', 'test'), content=u'Test \u2084 item')
ITEM_TO_BE_DELETED = domish.Element((None, 'item'))
ITEM_TO_BE_DELETED['id'] = 'to-be-deleted'
ITEM_TO_BE_DELETED.addElement(('testns', 'test'), content=u'Test \u2083 item')

def decode(object):
    if isinstance(object, str):
        object = object.decode('utf-8')
    return object



class StorageTests:

    def _assignTestNode(self, node):
        self.node = node


    def setUp(self):
        d = self.s.getNode('pre-existing')
        d.addCallback(self._assignTestNode)
        return d


    def test_interfaceIStorage(self):
        self.assertTrue(verifyObject(iidavoll.IStorage, self.s))


    def test_interfaceINode(self):
        self.assertTrue(verifyObject(iidavoll.INode, self.node))


    def test_interfaceILeafNode(self):
        self.assertTrue(verifyObject(iidavoll.ILeafNode, self.node))


    def test_getNode(self):
        return self.s.getNode('pre-existing')


    def test_getNonExistingNode(self):
        d = self.s.getNode('non-existing')
        self.assertFailure(d, error.NodeNotFound)
        return d


    def test_getNodeIDs(self):
        def cb(nodeIdentifiers):
            self.assertIn('pre-existing', nodeIdentifiers)
            self.assertNotIn('non-existing', nodeIdentifiers)

        return self.s.getNodeIds().addCallback(cb)


    def test_createExistingNode(self):
        config = self.s.getDefaultConfiguration('leaf')
        config['pubsub#node_type'] = 'leaf'
        d = self.s.createNode('pre-existing', OWNER, config)
        self.assertFailure(d, error.NodeExists)
        return d


    def test_createNode(self):
        def cb(void):
            d = self.s.getNode('new 1')
            return d

        config = self.s.getDefaultConfiguration('leaf')
        config['pubsub#node_type'] = 'leaf'
        d = self.s.createNode('new 1', OWNER, config)
        d.addCallback(cb)
        return d


    def test_createNodeChangingConfig(self):
        """
        The configuration passed to createNode must be free to be changed.
        """
        def cb(result):
            node1, node2 = result
            self.assertTrue(node1.getConfiguration()['pubsub#persist_items'])

        config = {
                "pubsub#persist_items": True,
                "pubsub#deliver_payloads": True,
                "pubsub#send_last_published_item": 'on_sub',
                "pubsub#node_type": 'leaf',
                "pubsub#access_model": 'open',
                const.OPT_PUBLISH_MODEL: const.VAL_PMODEL_OPEN
                }

        def unsetPersistItems(_):
            config["pubsub#persist_items"] = False

        d = defer.succeed(None)
        d.addCallback(lambda _: self.s.createNode('new 1', OWNER, config))
        d.addCallback(unsetPersistItems)
        d.addCallback(lambda _: self.s.createNode('new 2', OWNER, config))
        d.addCallback(lambda _: defer.gatherResults([
                                    self.s.getNode('new 1'),
                                    self.s.getNode('new 2')]))
        d.addCallback(cb)
        return d


    def test_deleteNonExistingNode(self):
        d = self.s.deleteNode('non-existing')
        self.assertFailure(d, error.NodeNotFound)
        return d


    def test_deleteNode(self):
        def cb(void):
            d = self.s.getNode('to-be-deleted')
            self.assertFailure(d, error.NodeNotFound)
            return d

        d = self.s.deleteNode('to-be-deleted')
        d.addCallback(cb)
        return d


    def test_getAffiliations(self):
        def cb(affiliations):
            self.assertIn(('pre-existing', 'owner'), affiliations)

        d = self.s.getAffiliations(OWNER)
        d.addCallback(cb)
        return d


    def test_getSubscriptions(self):
        def cb(subscriptions):
            found = False
            for subscription in subscriptions:
                if (subscription.nodeIdentifier == 'pre-existing' and
                    subscription.subscriber == SUBSCRIBER and
                    subscription.state == 'subscribed'):
                    found = True
            self.assertTrue(found)

        d = self.s.getSubscriptions(SUBSCRIBER)
        d.addCallback(cb)
        return d


    # Node tests

    def test_getType(self):
        self.assertEqual(self.node.getType(), 'leaf')


    def test_getConfiguration(self):
        config = self.node.getConfiguration()
        self.assertIn('pubsub#persist_items', config.iterkeys())
        self.assertIn('pubsub#deliver_payloads', config.iterkeys())
        self.assertEqual(config['pubsub#persist_items'], True)
        self.assertEqual(config['pubsub#deliver_payloads'], True)


    def test_setConfiguration(self):
        def getConfig(node):
            d = node.setConfiguration({'pubsub#persist_items': False})
            d.addCallback(lambda _: node)
            return d

        def checkObjectConfig(node):
            config = node.getConfiguration()
            self.assertEqual(config['pubsub#persist_items'], False)

        def getNode(void):
            return self.s.getNode('to-be-reconfigured')

        def checkStorageConfig(node):
            config = node.getConfiguration()
            self.assertEqual(config['pubsub#persist_items'], False)

        d = self.s.getNode('to-be-reconfigured')
        d.addCallback(getConfig)
        d.addCallback(checkObjectConfig)
        d.addCallback(getNode)
        d.addCallback(checkStorageConfig)
        return d


    def test_getMetaData(self):
        metaData = self.node.getMetaData()
        for key, value in self.node.getConfiguration().iteritems():
            self.assertIn(key, metaData.iterkeys())
            self.assertEqual(value, metaData[key])
        self.assertIn('pubsub#node_type', metaData.iterkeys())
        self.assertEqual(metaData['pubsub#node_type'], 'leaf')


    def test_getAffiliation(self):
        def cb(affiliation):
            self.assertEqual(affiliation, 'owner')

        d = self.node.getAffiliation(OWNER)
        d.addCallback(cb)
        return d


    def test_getNonExistingAffiliation(self):
        def cb(affiliation):
            self.assertEqual(affiliation, None)

        d = self.node.getAffiliation(SUBSCRIBER)
        d.addCallback(cb)
        return d


    def test_addSubscription(self):
        def cb1(void):
            return self.node.getSubscription(SUBSCRIBER_NEW)

        def cb2(subscription):
            self.assertEqual(subscription.state, 'pending')

        d = self.node.addSubscription(SUBSCRIBER_NEW, 'pending', {})
        d.addCallback(cb1)
        d.addCallback(cb2)
        return d


    def test_addExistingSubscription(self):
        d = self.node.addSubscription(SUBSCRIBER, 'pending', {})
        self.assertFailure(d, error.SubscriptionExists)
        return d


    def test_getSubscription(self):
        def cb(subscriptions):
            self.assertEquals(subscriptions[0].state, 'subscribed')
            self.assertEquals(subscriptions[1].state, 'pending')
            self.assertEquals(subscriptions[2], None)

        d = defer.gatherResults([self.node.getSubscription(SUBSCRIBER),
                                 self.node.getSubscription(SUBSCRIBER_PENDING),
                                 self.node.getSubscription(OWNER)])
        d.addCallback(cb)
        return d


    def test_removeSubscription(self):
        return self.node.removeSubscription(SUBSCRIBER_TO_BE_DELETED)


    def test_removeNonExistingSubscription(self):
        d = self.node.removeSubscription(OWNER)
        self.assertFailure(d, error.NotSubscribed)
        return d


    def test_getNodeSubscriptions(self):
        def extractSubscribers(subscriptions):
            return [subscription.subscriber for subscription in subscriptions]

        def cb(subscribers):
            self.assertIn(SUBSCRIBER, subscribers)
            self.assertNotIn(SUBSCRIBER_PENDING, subscribers)
            self.assertNotIn(OWNER, subscribers)

        d = self.node.getSubscriptions('subscribed')
        d.addCallback(extractSubscribers)
        d.addCallback(cb)
        return d


    def test_isSubscriber(self):
        def cb(subscribed):
            self.assertEquals(subscribed[0][1], True)
            self.assertEquals(subscribed[1][1], True)
            self.assertEquals(subscribed[2][1], False)
            self.assertEquals(subscribed[3][1], False)

        d = defer.DeferredList([self.node.isSubscribed(SUBSCRIBER),
                                self.node.isSubscribed(SUBSCRIBER.userhostJID()),
                                self.node.isSubscribed(SUBSCRIBER_PENDING),
                                self.node.isSubscribed(OWNER)])
        d.addCallback(cb)
        return d


    def test_storeItems(self):
        def cb1(void):
            return self.node.getItemsById("", False, ['new'])

        def cb2(result):
            self.assertEqual(ITEM_NEW.toXml(), result[0].toXml())

        d = self.node.storeItems([(const.VAL_AMODEL_DEFAULT, {}, ITEM_NEW)], PUBLISHER)
        d.addCallback(cb1)
        d.addCallback(cb2)
        return d


    def test_storeUpdatedItems(self):
        def cb1(void):
            return self.node.getItemsById("", False, ['current'])

        def cb2(result):
            self.assertEqual(ITEM_UPDATED.toXml(), result[0].toXml())

        d = self.node.storeItems([(const.VAL_AMODEL_DEFAULT, {}, ITEM_UPDATED)], PUBLISHER)
        d.addCallback(cb1)
        d.addCallback(cb2)
        return d


    def test_removeItems(self):
        def cb1(result):
            self.assertEqual(['to-be-deleted'], result)
            return self.node.getItemsById("", False, ['to-be-deleted'])

        def cb2(result):
            self.assertEqual(0, len(result))

        d = self.node.removeItems(['to-be-deleted'])
        d.addCallback(cb1)
        d.addCallback(cb2)
        return d


    def test_removeNonExistingItems(self):
        def cb(result):
            self.assertEqual([], result)

        d = self.node.removeItems(['non-existing'])
        d.addCallback(cb)
        return d


    def test_getItems(self):
        def cb(result):
            items = [item.toXml() for item in result]
            self.assertIn(ITEM.toXml(), items)
        d = self.node.getItems("", False)
        d.addCallback(cb)
        return d


    def test_lastItem(self):
        def cb(result):
            self.assertEqual(1, len(result))
            self.assertEqual(ITEM.toXml(), result[0].toXml())

        d = self.node.getItems("", False, 1)
        d.addCallback(cb)
        return d


    def test_getItemsById(self):
        def cb(result):
            self.assertEqual(1, len(result))

        d = self.node.getItemsById("", False, ['current'])
        d.addCallback(cb)
        return d


    def test_getNonExistingItemsById(self):
        def cb(result):
            self.assertEqual(0, len(result))

        d = self.node.getItemsById("", False, ['non-existing'])
        d.addCallback(cb)
        return d


    def test_purge(self):
        def cb1(node):
            d = node.purge()
            d.addCallback(lambda _: node)
            return d

        def cb2(node):
            return node.getItems("", False)

        def cb3(result):
            self.assertEqual([], result)

        d = self.s.getNode('to-be-purged')
        d.addCallback(cb1)
        d.addCallback(cb2)
        d.addCallback(cb3)
        return d


    def test_getNodeAffilatiations(self):
        def cb1(node):
            return node.getAffiliations()

        def cb2(affiliations):
            affiliations = dict(((a[0].full(), a[1]) for a in affiliations))
            self.assertEquals(affiliations[OWNER.userhost()], 'owner')

        d = self.s.getNode('pre-existing')
        d.addCallback(cb1)
        d.addCallback(cb2)
        return d



class MemoryStorageStorageTestCase(unittest.TestCase, StorageTests):

    def setUp(self):
        from sat_pubsub.memory_storage import Storage, PublishedItem, LeafNode
        from sat_pubsub.memory_storage import Subscription

        defaultConfig = Storage.defaultConfig['leaf']

        self.s = Storage()
        self.s._nodes['pre-existing'] = \
                LeafNode('pre-existing', OWNER, defaultConfig)
        self.s._nodes['to-be-deleted'] = \
                LeafNode('to-be-deleted', OWNER, None)
        self.s._nodes['to-be-reconfigured'] = \
                LeafNode('to-be-reconfigured', OWNER, defaultConfig)
        self.s._nodes['to-be-purged'] = \
                LeafNode('to-be-purged', OWNER, None)

        subscriptions = self.s._nodes['pre-existing']._subscriptions
        subscriptions[SUBSCRIBER.full()] = Subscription('pre-existing',
                                                        SUBSCRIBER,
                                                        'subscribed')
        subscriptions[SUBSCRIBER_TO_BE_DELETED.full()] = \
                Subscription('pre-existing', SUBSCRIBER_TO_BE_DELETED,
                             'subscribed')
        subscriptions[SUBSCRIBER_PENDING.full()] = \
                Subscription('pre-existing', SUBSCRIBER_PENDING,
                             'pending')

        item = PublishedItem(ITEM_TO_BE_DELETED, PUBLISHER)
        self.s._nodes['pre-existing']._items['to-be-deleted'] = item
        self.s._nodes['pre-existing']._itemlist.append(item)
        self.s._nodes['to-be-purged']._items['to-be-deleted'] = item
        self.s._nodes['to-be-purged']._itemlist.append(item)
        item = PublishedItem(ITEM, PUBLISHER)
        self.s._nodes['pre-existing']._items['current'] = item
        self.s._nodes['pre-existing']._itemlist.append(item)

        return StorageTests.setUp(self)



class PgsqlStorageStorageTestCase(unittest.TestCase, StorageTests):

    dbpool = None

    def setUp(self):
        from sat_pubsub.pgsql_storage import Storage
        from twisted.enterprise import adbapi
        if self.dbpool is None:
            self.__class__.dbpool = adbapi.ConnectionPool('psycopg2',
                                            database='pubsub_test',
                                            cp_reconnect=True,
                                            client_encoding='utf-8',
                                            )
        self.s = Storage(self.dbpool)
        self.dbpool.start()
        d = self.dbpool.runInteraction(self.init)
        d.addCallback(lambda _: StorageTests.setUp(self))
        return d


    def tearDown(self):
        return self.dbpool.runInteraction(self.cleandb)


    def init(self, cursor):
        self.cleandb(cursor)
        cursor.execute("""INSERT INTO nodes
                          (node, node_type, persist_items)
                          VALUES ('pre-existing', 'leaf', TRUE)""")
        cursor.execute("""INSERT INTO nodes (node) VALUES ('to-be-deleted')""")
        cursor.execute("""INSERT INTO nodes (node) VALUES ('to-be-reconfigured')""")
        cursor.execute("""INSERT INTO nodes (node) VALUES ('to-be-purged')""")
        cursor.execute("""INSERT INTO entities (jid) VALUES (%s)""",
                       (OWNER.userhost(),))
        cursor.execute("""INSERT INTO affiliations
                          (node_id, entity_id, affiliation)
                          SELECT node_id, entity_id, 'owner'
                          FROM nodes, entities
                          WHERE node='pre-existing' AND jid=%s""",
                       (OWNER.userhost(),))
        cursor.execute("""INSERT INTO entities (jid) VALUES (%s)""",
                       (SUBSCRIBER.userhost(),))
        cursor.execute("""INSERT INTO subscriptions
                          (node_id, entity_id, resource, state)
                          SELECT node_id, entity_id, %s, 'subscribed'
                          FROM nodes, entities
                          WHERE node='pre-existing' AND jid=%s""",
                       (SUBSCRIBER.resource,
                        SUBSCRIBER.userhost()))
        cursor.execute("""INSERT INTO entities (jid) VALUES (%s)""",
                       (SUBSCRIBER_TO_BE_DELETED.userhost(),))
        cursor.execute("""INSERT INTO subscriptions
                          (node_id, entity_id, resource, state)
                          SELECT node_id, entity_id, %s, 'subscribed'
                          FROM nodes, entities
                          WHERE node='pre-existing' AND jid=%s""",
                       (SUBSCRIBER_TO_BE_DELETED.resource,
                        SUBSCRIBER_TO_BE_DELETED.userhost()))
        cursor.execute("""INSERT INTO entities (jid) VALUES (%s)""",
                       (SUBSCRIBER_PENDING.userhost(),))
        cursor.execute("""INSERT INTO subscriptions
                          (node_id, entity_id, resource, state)
                          SELECT node_id, entity_id, %s, 'pending'
                          FROM nodes, entities
                          WHERE node='pre-existing' AND jid=%s""",
                       (SUBSCRIBER_PENDING.resource,
                        SUBSCRIBER_PENDING.userhost()))
        cursor.execute("""INSERT INTO entities (jid) VALUES (%s)""",
                       (PUBLISHER.userhost(),))
        cursor.execute("""INSERT INTO items
                          (node_id, publisher, item, data, date)
                          SELECT node_id, %s, 'to-be-deleted', %s,
                                 now() - interval '1 day'
                          FROM nodes
                          WHERE node='pre-existing'""",
                       (PUBLISHER.userhost(),
                        ITEM_TO_BE_DELETED.toXml()))
        cursor.execute("""INSERT INTO items (node_id, publisher, item, data)
                          SELECT node_id, %s, 'to-be-deleted', %s
                          FROM nodes
                          WHERE node='to-be-purged'""",
                       (PUBLISHER.userhost(),
                        ITEM_TO_BE_DELETED.toXml()))
        cursor.execute("""INSERT INTO items (node_id, publisher, item, data)
                          SELECT node_id, %s, 'current', %s
                          FROM nodes
                          WHERE node='pre-existing'""",
                       (PUBLISHER.userhost(),
                        ITEM.toXml()))


    def cleandb(self, cursor):
        cursor.execute("""DELETE FROM nodes WHERE node in
                          ('non-existing', 'pre-existing', 'to-be-deleted',
                           'new 1', 'new 2', 'new 3', 'to-be-reconfigured',
                           'to-be-purged')""")
        cursor.execute("""DELETE FROM entities WHERE jid=%s""",
                       (OWNER.userhost(),))
        cursor.execute("""DELETE FROM entities WHERE jid=%s""",
                       (SUBSCRIBER.userhost(),))
        cursor.execute("""DELETE FROM entities WHERE jid=%s""",
                       (SUBSCRIBER_TO_BE_DELETED.userhost(),))
        cursor.execute("""DELETE FROM entities WHERE jid=%s""",
                       (SUBSCRIBER_PENDING.userhost(),))
        cursor.execute("""DELETE FROM entities WHERE jid=%s""",
                       (PUBLISHER.userhost(),))

try:
    import psycopg2
except ImportError:
    PgsqlStorageStorageTestCase.skip = "Psycopg2 not available"
