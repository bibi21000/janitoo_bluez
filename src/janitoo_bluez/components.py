# -*- coding: utf-8 -*-
"""The Bluetooth components

"""

__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

# Set default logging handler to avoid "No handler found" warnings.
import logging
logger = logging.getLogger(__name__)
import os
import threading

from janitoo.component import JNTComponent

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_CAMERA_PREVIEW = 0x2200

assert(COMMAND_DESC[COMMAND_CAMERA_PREVIEW] == 'COMMAND_CAMERA_PREVIEW')
##############################################################

from janitoo_bluez import OID

import bluetooth

def make_spy(**kwargs):
    return SpyComponent(**kwargs)

class SpyComponent(JNTComponent):
    """ A spy component for bluetooth """

    def __init__(self, bus=None, addr=None, **kwargs):
        """
        """
        oid = kwargs.pop('oid', '%s.spy'%OID)
        name = kwargs.pop('name', "Spyer")
        product_name = kwargs.pop('product_name', "Spy for bluetooth devices")
        product_type = kwargs.pop('product_type', "Spy for bluetooth devices")
        JNTComponent.__init__(self, oid=oid, bus=bus, addr=addr, name=name,
                product_name=product_name, product_type=product_type, **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)

        uuid="presence"
        self.values[uuid] = self.value_factory['sensor_presence'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The presence of a bluetooth device',
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

        uuid="addr"
        self.values[uuid] = self.value_factory['config_string'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The MAC address of the bluetooth device',
            label='Addr',
            default=kwargs.get("addr", "E4:D1:C5:FA:F8:E8"),
        )
        uuid="timer_delay"
        self.values[uuid] = self.value_factory['config_integer'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The delay between 2 checks',
            label='Timer.',
            default=kwargs.pop('timer_delay', 30),
        )
        uuid="hysteresis"
        self.values[uuid] = self.value_factory['config_integer'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The number of negative scans before sending an absence notification',
            label='Hysteresis.',
            default=kwargs.pop('hysteresis', 3),
        )
        self.check_timer = None
        self._check_active = False

    def stop_check(self):
        """Check the sonic component

        """
        if self.check_timer is not None:
            self.check_timer.cancel()
            self.check_timer = None

    def on_check(self):
        """Make a check using a timer.

        """
        self.stop_check()
        if self.check_timer is None:
            self.check_timer = threading.Timer(self.values['timer_delay'].data, self.on_check)
            self.check_timer.start()
        self.check_devices()

    def check_devices(self):
        """Make a check using a timer.

        """
        if self._check_active:
            return
        self._check_active = True
        try:
            found = bluetooth.discover_devices()
            for dev in self.devices:
                if dev[1] in found and not self.values["presence"].instances[config]['data']:
                    self.values["presence"].instances[config]['data'] = True
                    # Notify new device
                elif dev[1] not in found and not self.values["presence"].instances[config]['data'] and dev[2] == self.values["hysteresis"].instances[config]['data']:
                    self.values["presence"].instances[config]['data'] = False
                    # Notify device away
                elif dev not in found and dev[2] < self.values["hysteresis"].instances[config]['data']:
                    self.values["presence"].instances[config]['data'] = False
                    dev[2] += 1
        except Exception:
            logger.exception("[%s] - Error when checking bluetooth devices", self.__class__.__name__)
        self._check_active = False

    def start(self, mqttc):
        """Start the component.

        """
        JNTComponent.start(self, mqttc)
        configs = len(self.values["addr"].get_index_configs())
        if configs == 0:
            self.devices = [(0, self.values["addr"].data, 0)]
        else:
            self.devices = []
            for config in range(configs):
                self.devices += (config, self.values["addr"].instances[config]['data'])
        self.on_check()
        return True

    def stop(self):
        """Stop the component.

        """
        self.stop_check()
        JNTComponent.stop(self)
        return True

    def check_heartbeat(self):
        """Check that the component is 'available'

        """
        return True
