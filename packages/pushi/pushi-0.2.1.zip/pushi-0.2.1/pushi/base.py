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

import os
import hmac
import hashlib

import appier

BASE_URL = "https://puxiapp.com:9090"
""" The base url to be used by the api to access
the remote endpoints, should not be changed """

class Pushi:
    """
    Base class for the construction of the pushi
    proxy object for interaction with the server
    side of the pushi system.

    Should provide the various methods that enable
    the developer to make operations for both read
    and write (create and read).
    """

    def __init__(self, app_id = None, app_key = None, app_secret = None, base_url = None):
        self.app_id = app_id or os.environ.get("PUSHI_ID", None)
        self.app_key = app_key or os.environ.get("PUSHI_KEY", None)
        self.app_secret = app_secret or os.environ.get("PUSHI_SECRET", None)
        self.base_url = base_url or os.environ.get("PUSHI_URL", BASE_URL)
        self.token = None

    def authenticate(self, channel, socket_id):
        # in case the app key is not defined for the current
        # instance an exception must be raised as it's not possible
        # to run the authentication process without an app key
        if not self.app_key: raise RuntimeError("No app key defined")

        # creates the string to hashed using both the provided
        # socket id and channel (concatenation)
        string = "%s:%s" % (socket_id, channel)
        string = appier.legacy.bytes(string)

        # runs the hmac encryption in the provided secret and
        # the constructed string and returns a string containing
        # both the key and the hexadecimal digest
        app_secret = appier.legacy.bytes(str(self.app_secret))
        structure = hmac.new(app_secret, string, hashlib.sha256)
        digest = structure.hexdigest()
        return "%s:%s" % (self.app_key, digest)

    def auth_callback(self, params):
        token = self.login()
        params["sid"] = token

    def ensure_login(self):
        if self.token: return self.token
        return self.login()

    def login(self):
        # tries to login in the pushi infra-structure using the
        # login route together with the full set of auth info
        # retrieving the result map that should contain the
        # session token, to be used in further calls
        result = appier.get(
            self.base_url + "/login",
            params = dict(
                app_id = self.app_id,
                app_key = self.app_key,
                app_secret = self.app_secret
            )
        )

        # unpacks the token value from the result map and then
        # returns the token to the caller method
        self.token = result["token"]
        return self.token

    def create(self, name):
        # runs the post call that will create the app with the provided
        # name then returns the returning map to the caller method, it
        # should contain the generated information for the app
        result = appier.post(
            self.base_url + "/apps",
            data_j = dict(
                name = name
            )
        )
        return result

    def update(self, app_id = None, **kwargs):
        # runs the ensure login call making sure that the login token
        # is currently present in the environment, this is required
        # to perform secured remote calls
        token = self.ensure_login()

        # retrieves the proper app id to be used defaulting to the current
        # defined app id in case none is provided
        app_id = app_id or self.app_id

        # runs the pit call that will create the app with the provided
        # name then returns the returning map to the caller method, it
        # should contain the newly updated information for the app
        result = appier.put(
            self.base_url + "/apps/%s" % app_id,
            params = dict(sid = token),
            data_j = kwargs,
            auth_callback = self.auth_callback
        )
        return result

    def trigger(self, channel, data, event = "message", **kwargs):
        # runs the ensure login call making sure that the login token
        # is currently present in the environment, this is required
        # to perform secured remote calls
        token = self.ensure_login()

        # creates the initial json data structure to be used as the message
        # and then "extends" it with the extra key word arguments passed
        # to this methods as a method of extension
        data_j = dict(
            data = data,
            event = event,
            channel = channel
        )
        for key in kwargs: data_j[key] = kwargs[key]

        # performs the concrete event trigger operation creating an event
        # with the provided information using a secure channel
        result = appier.post(
            self.base_url + "/apps/%s/events" % self.app_id,
            params = dict(sid = token),
            data_j = data_j,
            auth_callback = self.auth_callback
        )
        return result

    def subscribe(self, user_id, event):
        # runs the ensure login call making sure that the login token
        # is currently present in the environment, this is required
        # to perform secured remote calls
        token = self.ensure_login()

        # runs the subscription operation for the provided
        # user id and event, this operation uses the currently
        # defined app id for the operation, then returns the
        # resulting dictionary to the caller method
        result = appier.get(
            self.base_url + "/apps/%s/subscribe" % self.app_id,
            params = dict(
                sid = token,
                user_id = user_id,
                event = event
            ),
            auth_callback = self.auth_callback
        )
        return result

    def unsubscribe(self, user_id, event):
        # runs the ensure login call making sure that the login token
        # is currently present in the environment, this is required
        # to perform secured remote calls
        token = self.ensure_login()

        # runs the unsubscription operation for the provided
        # user id and event, this operation uses the currently
        # defined app id for the operation, then returns the
        # resulting dictionary to the caller method
        result = appier.get(
            self.base_url + "/apps/%s/unsubscribe" % self.app_id,
            params = dict(
                sid = token,
                user_id = user_id,
                event = event
            ),
            auth_callback = self.auth_callback
        )
        return result

    def subscribe_apn(self, token, event, auth = None, unsubscribe = True):
        # runs the ensure login call making sure that the login token
        # is currently present in the environment, this is required
        # to perform secured remote calls
        _token = self.ensure_login()

        # runs the apn subscription operation for the provided
        # token and event, this operation uses the currently
        # defined app id for the operation, then returns the
        # resulting dictionary to the caller method
        result = appier.get(
            self.base_url + "/apps/%s/subscribe_apn" % self.app_id,
            params = dict(
                sid = _token,
                token = token,
                event = event,
                auth = auth,
                unsubscribe = unsubscribe
            ),
            auth_callback = self.auth_callback
        )
        return result

    def unsubscribe_apn(self, token, event):
        # runs the ensure login call making sure that the login token
        # is currently present in the environment, this is required
        # to perform secured remote calls
        _token = self.ensure_login()

        # runs the apn unsubscription operation for the provided
        # token and event, this operation uses the currently
        # defined app id for the operation, then returns the
        # resulting dictionary to the caller method
        result = appier.get(
            self.base_url + "/apps/%s/unsubscribe_apn" % self.app_id,
            params = dict(
                sid = _token,
                token = token,
                event = event
            ),
            auth_callback = self.auth_callback
        )
        return result

    def subscribe_web(self, url, event, auth = None, unsubscribe = True):
        # runs the ensure login call making sure that the login token
        # is currently present in the environment, this is required
        # to perform secured remote calls
        token = self.ensure_login()

        # runs the web subscription operation for the provided
        # token and event, this operation uses the currently
        # defined app id for the operation, then returns the
        # resulting dictionary to the caller method
        result = appier.get(
            self.base_url + "/apps/%s/subscribe_web" % self.app_id,
            params = dict(
                sid = token,
                url = url,
                event = event,
                auth = auth,
                unsubscribe = unsubscribe
            ),
            auth_callback = self.auth_callback
        )
        return result

    def unsubscribe_web(self, url, event):
        # runs the ensure login call making sure that the login token
        # is currently present in the environment, this is required
        # to perform secured remote calls
        token = self.ensure_login()

        # runs the web unsubscription operation for the provided
        # token and event, this operation uses the currently
        # defined app id for the operation, then returns the
        # resulting dictionary to the caller method
        result = appier.get(
            self.base_url + "/apps/%s/unsubscribe_web" % self.app_id,
            params = dict(
                sid = token,
                url = url,
                event = event
            ),
            auth_callback = self.auth_callback
        )
        return result
