# Copyright (c) 2014 Cisco Systems
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
#
# @author: Ivar Lazzaro (ivarlazzaro@gmail.com), Cisco Systems, Inc.

import sys

import mock

sys.modules["apicapi"] = mock.Mock()

from neutron.tests import base

from apic_ml2.neutron.plugins.ml2.drivers.cisco.apic import apic_sync


LOOPING_CALL = 'neutron.openstack.common.loopingcall.FixedIntervalLoopingCall'
GET_PLUGIN = 'neutron.manager.NeutronManager.get_plugin'
GET_ADMIN_CONTEXT = 'neutron.context.get_admin_context'
NETWORK_CONTEXT = 'neutron.plugins.ml2.driver_context.NetworkContext'
SUBNET_CONTEXT = 'neutron.plugins.ml2.driver_context.SubnetContext'
PORT_CONTEXT = 'neutron.plugins.ml2.driver_context.PortContext'


class TestCiscoApicSync(base.BaseTestCase):

    def setUp(self):
        super(TestCiscoApicSync, self).setUp()
        self.driver = mock.Mock()
        # Patch looping call
        loopingcall_c = mock.patch(LOOPING_CALL).start()
        self.loopingcall = mock.Mock()
        loopingcall_c.return_value = self.loopingcall
        # Patch get plugin
        self.get_plugin = mock.patch(GET_PLUGIN).start()
        self.get_plugin.return_value = mock.Mock()
        # Patch get admin context
        self.get_admin_context = mock.patch(GET_ADMIN_CONTEXT).start()
        self.get_admin_context.return_value = mock.Mock()
        # Patch driver context
        mock.patch(NETWORK_CONTEXT).start()
        mock.patch(SUBNET_CONTEXT).start()
        mock.patch(PORT_CONTEXT).start()

    def test_sync_base(self):
        sync = apic_sync.ApicBaseSynchronizer(self.driver)
        sync.core_plugin = mock.Mock()
        sync.core_plugin.get_networks.return_value = [{'id': 'net'}]
        sync.core_plugin.get_subnets.return_value = [{'id': 'sub'}]
        sync.core_plugin.get_ports.return_value = [{'id': 'port',
                                                    'network_id': 'net'}]
        sync.sync_base()
        self.driver.create_network_postcommit.assert_called_once()
        self.driver.create_subnet_postcommit.assert_called_once()
        self.driver.create_port_postcommit.assert_called_once()

    def test_sync_router(self):
        sync = apic_sync.ApicRouterSynchronizer(self.driver)
        sync.core_plugin = mock.Mock()
        sync.core_plugin.get_ports.return_value = [{'id': 'port',
                                                    'network_id': 'net',
                                                    'device_id': 'dev'}]
        sync.sync_router()
        self.driver.add_router_interface_postcommit.assert_called_once()
