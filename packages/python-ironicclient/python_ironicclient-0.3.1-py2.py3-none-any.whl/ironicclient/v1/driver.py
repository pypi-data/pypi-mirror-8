# -*- coding: utf-8 -*-
#
# Copyright 2013 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from ironicclient.common import base


class Driver(base.Resource):
    def __repr__(self):
        return "<Driver %s>" % self._info


class DriverManager(base.Manager):
    resource_class = Driver

    def list(self):
        return self._list('/v1/drivers', "drivers")

    def get(self, driver_name):
        try:
            return self._list('/v1/drivers/%s' % driver_name)[0]
        except IndexError:
            return None

    def properties(self, driver_name):
        try:
            info = self._list('/v1/drivers/%s/properties' % driver_name)[0]
            if info:
                return info.to_dict()
            return {}
        except IndexError:
            return {}

    def vendor_passthru(self, **kwargs):
        driver_name = kwargs['driver_name']
        method = kwargs['method']
        args = kwargs['args']
        path = "/v1/drivers/%(driver_name)s/vendor_passthru/%(method)s" % {
                                                    'driver_name': driver_name,
                                                    'method': method
                                                    }
        return self._update(path, args, method='POST')
