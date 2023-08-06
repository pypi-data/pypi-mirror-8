#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Pushi System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Pushi System.
#
# Hive Pushi System is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Pushi System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Pushi System. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json

import netius.clients

class PushiChannel(netius.observer.Observable):

    def __init__(self, owner, name):
        netius.observer.Observable.__init__(self)
        self.owner = owner
        self.name = name
        self.data = None
        self.subscribed = False

    def confirm(self, data):
        alias = data["alias"] if data else []
        for name in alias:
            channel = PushiChannel(self.owner, name)
            self.owner.channels[name] = channel
            self.owner.on_subscribe_pushi(name, {})

        self.data = data
        self.subscribed = True

        self.trigger("subscribe", self, data)

    def send(self, event, data, persist = True):
        self.owner.send_channel(event, data, self.name, persist = persist)

class PushiConnection(netius.clients.WSConnection):

    def __init__(self, *args, **kwargs):
        netius.clients.WSConnection.__init__(self, *args, **kwargs)
        self.state = "disconnected"
        self.socket_id = None
        self.channels = dict()

    def receive_ws(self, data):
        data = data.decode("utf-8")
        data_j = json.loads(data)

        is_connected = self.state == "disconnected" and\
            data_j["event"] == "pusher:connection_established"

        if is_connected:
            data = json.loads(data_j["data"])
            self.on_connect_pushi(data)
        elif self.state == "connected":
            self.on_message_pushi(data_j)

    def on_connect_pushi(self, data):
        self.socket_id = data["socket_id"]
        self.state = "connected"
        self.trigger("connect_pushi", self)

    def on_disconnect_pushi(self, data):
        self.socket_id = None
        self.channels = dict()
        self.state = "disconnected"
        self.trigger("disconnect_pushi", self)

    def on_message_pushi(self, data_j):
        # unpacks the complete set of information from the json based
        # data structure so that it gets processed in the method
        data = data_j["data"]
        event = data_j["event"]
        channel = data_j["channel"]

        # tries to gather the channel object/information reference
        # for the channel that received the message and verifies if
        # the current channel is peer related or not
        _channel = self.channels[channel]
        is_peer = channel.startswith("peer-")

        # in case no channel information is found for the channel
        # (no subscription) and the channel is not peer related the
        # message is ignored as there's no channel subscription
        if channel and not _channel and not is_peer: return

        if event == "pusher_internal:subscription_succeeded":
            data = json.loads(data_j["data"])
            self.on_subscribe_pushi(channel, data)

        elif event == "pusher:member_added":
            member = json.loads(data_j["member"])
            self.on_member_added_pushi(channel, member)

        elif event == "pusher:member_removed":
            member = json.loads(data_j["member"])
            self.on_member_removed_pushi(channel, member)

        self.trigger(event, self, data, channel)

    def on_subscribe_pushi(self, channel, data):
        _channel = self.channels[channel]
        _channel.confirm(data)
        self.trigger("subscribe", self, channel, data)

    def on_member_added_pushi(self, channel, member):
        pass

    def on_member_removed_pushi(self, channel, member):
        pass

    def subscribe_pushi(self, channel, channel_data = None, force = False, callback = None):
        exists = channel in self.channels
        if exists and not force: return

        is_private = self._is_private(channel)
        if is_private: self._subscribe_private(channel, channel_data = channel_data)
        else: self._subscribe_public(channel)

        name = channel
        channel = PushiChannel(self, name)
        self.channels[name] = channel

        if callback: channel.bind("subscribe", callback)

        return channel

    def send_event(self, event, data, persist = True, callback = None):
        json_d = dict(
            event = event,
            data = data,
            persist = persist
        )
        self.send_pushi(json_d, callback = callback)

    def send_channel(self, event, data, channel, persist = True, callback = None):
        json_d = dict(
            event = event,
            data = data,
            channel = channel,
            persist = persist
        )
        self.send_pushi(json_d, callback = callback)

    def send_pushi(self, json_d, callback = None):
        data = json.dumps(json_d)
        self.send_ws(data, callback = callback)

    def _subscribe_public(self, channel):
        self.send_event("pusher:subscribe", dict(
            channel = channel
        ))

    def _subscribe_private(self, channel, channel_data = None):
        if not self.owner.api: raise RuntimeError("No private app available")
        auth = self.owner.api.authenticate(channel,self.socket_id)
        self.sendEvent("pusher:subscribe", dict(
            channel = channel,
            auth = auth,
            channel_data = channel_data
        ))

    def _is_private(self, channel):
        return channel.startswith("private-") or\
            channel.startswith("presence-") or\
            channel.startswith("personal-")

class PushiClient(netius.clients.WSClient):

    PUXIAPP_URL = "wss://puxiapp.com/"
    """ The default puxiapp url that is going to be used
    to establish new client's connections """

    def __init__(self, url = None, client_key = None, api = None, *args, **kwargs):
        netius.clients.WSClient.__init__(self, *args, **kwargs)
        self.base_url = url or PushiClient.PUXIAPP_URL
        self.client_key = client_key
        self.api = api
        self.url = self.base_url + self.client_key

    def new_connection(self, socket, address, ssl = False):
        return PushiConnection(
            owner = self,
            socket = socket,
            address = address,
            ssl = ssl
        )

    def connect_pushi(self, callback = None):
        connection = self.connect_ws(self.url)
        if not callback: return
        connection.bind("connect_pushi", callback)

if __name__ == "__main__":
    def on_subscribe(channel, data):
        channel.send("message", "Hello World", persist = False)
        connection = channel.owner
        client = connection.owner
        client.close()

    def on_connect(connection):
        connection.subscribe_pushi("global", callback = on_subscribe)

    client_key = netius.conf("PUSHI_KEY")
    client = PushiClient(client_key = client_key)
    client.connect_pushi(callback = on_connect)
