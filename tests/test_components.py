# -*- coding: utf-8 -*-

"""Unittests for Janitoo Server.
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
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time, datetime
import unittest
import threading
import logging
from pkg_resources import iter_entry_points
import mock

from janitoo_nosetests import JNTTBase
from janitoo_nosetests.server import JNTTServer, JNTTServerCommon
from janitoo_nosetests.thread import JNTTThread, JNTTThreadCommon
from janitoo_nosetests.component import JNTTComponent, JNTTComponentCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC
from janitoo.runner import jnt_parse_args
from janitoo.options import JNTOptions
from janitoo.utils import HADD, HADD_SEP, CADD, json_dumps, json_loads

from janitoo_raspberry_1wire.bus_1wire import OnewireBus
from janitoo_raspberry_1wire.thread_1wire import Rpi1wireThread
import janitoo_raspberry_1wire.components as components

class TestSpyComponent(JNTTComponent, JNTTComponentCommon):
    """Test the component
    """
    component_name = "bluez.spy"


#~ class TestSpy(JNTTBase):
    #~ """Test
    #~ """
    #~ conf = "tests/data/janitoo_bluez.conf"
#~
    #~ def test_101_get(self):
        #~ self.skipCITest()
        #~ self.skipDockerTest()
        #~ with mock.patch('sys.argv', ['test', 'start', '--conf_file=%s' % self.getDataFile(self.conf)]):
            #~ options = JNTOptions(vars(jnt_parse_args()))
        #~ bus = OnewireBus(options=options)
        #~ compo = components.DS18B20( bus=bus, hexadd="28-00000463b745")
        #~ temp = compo.temperature(None,0)
        #~ self.assertNotEqual(temp, None)
        #~ self.assertTrue(compo.check_heartbeat())

    #~ def test_101_get_bad(self):
        #~ self.skipRasperryTest()
        #~ with mock.patch('sys.argv', ['test', 'start', '--conf_file=%s' % self.getDataFile(self.conf)]):
            #~ options = JNTOptions(vars(jnt_parse_args()))
        #~ bus = OnewireBus(options=options)
        #~ compo = components.DS18B20( bus=bus)
        #~ temp = compo.temperature(None,0)
        #~ self.assertEqual(temp, None)
        #~ self.assertFalse(compo.check_heartbeat())
