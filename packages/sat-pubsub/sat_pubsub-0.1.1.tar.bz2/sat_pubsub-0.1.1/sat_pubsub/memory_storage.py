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

import copy
from zope.interface import implements
from twisted.internet import defer
from twisted.words.protocols.jabber import jid

from wokkel.pubsub import Subscription

from sat_pubsub import error, iidavoll

class Storage:

    implements(iidavoll.IStorage)

    defaultConfig = {
            'leaf': {
                "pubsub#persist_items": True,
                "pubsub#deliver_payloads": True,
                "pubsub#send_last_published_item": 'on_sub',
            },
            'collection': {
                "pubsub#deliver_payloads": True,
                "pubsub#send_last_published_item": 'on_sub',
            }
    }

    def __init__(self):
        rootNode = CollectionNode('', jid.JID('localhost'),
                                  copy.copy(self.defaultConfig['collection']))
        self._nodes = {'': rootNode}


    def getNode(self, nodeIdentifier):
        try:
            node = self._nodes[nodeIdentifier]
        except KeyError:
            return defer.fail(error.NodeNotFound())

        return defer.succeed(node)


    def getNodeIds(self):
        return defer.succeed(self._nodes.keys())


    def createNode(self, nodeIdentifier, owner, config):
        if nodeIdentifier in self._nodes:
            return defer.fail(error.NodeExists())

        if config['pubsub#node_type'] != 'leaf':
            raise error.NoCollections()

        node = LeafNode(nodeIdentifier, owner, config)
        self._nodes[nodeIdentifier] = node

        return defer.succeed(None)


    def deleteNode(self, nodeIdentifier):
        try:
            del self._nodes[nodeIdentifier]
        except KeyError:
            return defer.fail(error.NodeNotFound())

        return defer.succeed(None)


    def getAffiliations(self, entity):
        entity = entity.userhost()
        return defer.succeed([(node.nodeIdentifier, node._affiliations[entity])
                              for name, node in self._nodes.iteritems()
                              if entity in node._affiliations])


    def getSubscriptions(self, entity):
        subscriptions = []
        for node in self._nodes.itervalues():
            for subscriber, subscription in node._subscriptions.iteritems():
                subscriber = jid.internJID(subscriber)
                if subscriber.userhostJID() == entity.userhostJID():
                    subscriptions.append(subscription)

        return defer.succeed(subscriptions)


    def getDefaultConfiguration(self, nodeType):
        if nodeType == 'collection':
            raise error.NoCollections()

        return self.defaultConfig[nodeType]


class Node:

    implements(iidavoll.INode)

    def __init__(self, nodeIdentifier, owner, config):
        self.nodeIdentifier = nodeIdentifier
        self._affiliations = {owner.userhost(): 'owner'}
        self._subscriptions = {}
        self._config = copy.copy(config)


    def getType(self):
        return self.nodeType


    def getConfiguration(self):
        return self._config


    def getMetaData(self):
        config = copy.copy(self._config)
        config["pubsub#node_type"] = self.nodeType
        return config


    def setConfiguration(self, options):
        for option in options:
            if option in self._config:
                self._config[option] = options[option]

        return defer.succeed(None)


    def getAffiliation(self, entity):
        return defer.succeed(self._affiliations.get(entity.userhost()))


    def getSubscription(self, subscriber):
        try:
            subscription = self._subscriptions[subscriber.full()]
        except KeyError:
            return defer.succeed(None)
        else:
            return defer.succeed(subscription)


    def getSubscriptions(self, state=None):
        return defer.succeed(
                [subscription
                 for subscription in self._subscriptions.itervalues()
                 if state is None or subscription.state == state])



    def addSubscription(self, subscriber, state, options):
        if self._subscriptions.get(subscriber.full()):
            return defer.fail(error.SubscriptionExists())

        subscription = Subscription(self.nodeIdentifier, subscriber, state,
                                    options)
        self._subscriptions[subscriber.full()] = subscription
        return defer.succeed(None)


    def removeSubscription(self, subscriber):
        try:
            del self._subscriptions[subscriber.full()]
        except KeyError:
            return defer.fail(error.NotSubscribed())

        return defer.succeed(None)


    def isSubscribed(self, entity):
        for subscriber, subscription in self._subscriptions.iteritems():
            if jid.internJID(subscriber).userhost() == entity.userhost() and \
                    subscription.state == 'subscribed':
                return defer.succeed(True)

        return defer.succeed(False)


    def getAffiliations(self):
        affiliations = [(jid.internJID(entity), affiliation) for entity, affiliation
                       in self._affiliations.iteritems()]

        return defer.succeed(affiliations)



class PublishedItem(object):
    """
    A published item.

    This represent an item as it was published by an entity.

    @ivar element: The DOM representation of the item that was published.
    @type element: L{Element<twisted.words.xish.domish.Element>}
    @ivar publisher: The entity that published the item.
    @type publisher: L{JID<twisted.words.protocols.jabber.jid.JID>}
    """

    def __init__(self, element, publisher):
        self.element = element
        self.publisher = publisher



class LeafNode(Node):

    implements(iidavoll.ILeafNode)

    nodeType = 'leaf'

    def __init__(self, nodeIdentifier, owner, config):
        Node.__init__(self, nodeIdentifier, owner, config)
        self._items = {}
        self._itemlist = []


    def storeItems(self, item_data, publisher):
        for access_model, item_config, element in item_data:
            item = PublishedItem(element, publisher)
            itemIdentifier = element["id"]
            if itemIdentifier in self._items:
                self._itemlist.remove(self._items[itemIdentifier])
            self._items[itemIdentifier] = item
            self._itemlist.append(item)

        return defer.succeed(None)


    def removeItems(self, itemIdentifiers):
        deleted = []

        for itemIdentifier in itemIdentifiers:
            try:
                item = self._items[itemIdentifier]
            except KeyError:
                pass
            else:
                self._itemlist.remove(item)
                del self._items[itemIdentifier]
                deleted.append(itemIdentifier)

        return defer.succeed(deleted)


    def getItems(self, authorized_groups, unrestricted, maxItems=None):
        if maxItems:
            itemList = self._itemlist[-maxItems:]
        else:
            itemList = self._itemlist
        return defer.succeed([item.element for item in itemList])


    def getItemsById(self, authorized_groups, unrestricted, itemIdentifiers):
        items = []
        for itemIdentifier in itemIdentifiers:
            try:
                item = self._items[itemIdentifier]
            except KeyError:
                pass
            else:
                items.append(item.element)
        return defer.succeed(items)


    def purge(self):
        self._items = {}
        self._itemlist = []

        return defer.succeed(None)


    def filterItemsWithPublisher(self, itemIdentifiers, requestor):
        filteredItems = []
        for itemIdentifier in itemIdentifiers:
            try:
                if self._items[itemIdentifier].publisher.userhost() == requestor.userhost():
                    filteredItems.append(self.items[itemIdentifier])
            except KeyError, AttributeError:
                pass
        return defer.succeed(filteredItems)


class CollectionNode(Node):
    nodeType = 'collection'



class GatewayStorage(object):
    """
    Memory based storage facility for the XMPP-HTTP gateway.
    """

    def __init__(self):
        self.callbacks = {}


    def addCallback(self, service, nodeIdentifier, callback):
        try:
            callbacks = self.callbacks[service, nodeIdentifier]
        except KeyError:
            callbacks = set([callback])
            self.callbacks[service, nodeIdentifier] = callbacks
        else:
            callbacks.add(callback)
            pass

        return defer.succeed(None)


    def removeCallback(self, service, nodeIdentifier, callback):
        try:
            callbacks = self.callbacks[service, nodeIdentifier]
            callbacks.remove(callback)
        except KeyError:
            return defer.fail(error.NotSubscribed())
        else:
            if not callbacks:
                del self.callbacks[service, nodeIdentifier]

            return defer.succeed(not callbacks)


    def getCallbacks(self, service, nodeIdentifier):
        try:
            callbacks = self.callbacks[service, nodeIdentifier]
        except KeyError:
            return defer.fail(error.NoCallbacks())
        else:
            return defer.succeed(callbacks)


    def hasCallbacks(self, service, nodeIdentifier):
        return defer.succeed((service, nodeIdentifier) in self.callbacks)
