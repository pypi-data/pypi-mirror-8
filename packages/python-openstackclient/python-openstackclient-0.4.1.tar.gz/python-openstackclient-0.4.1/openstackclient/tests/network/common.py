#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import argparse
import mock

from openstackclient.tests import utils


class TestNetworkBase(utils.TestCommand):
    def setUp(self):
        super(TestNetworkBase, self).setUp()
        self.app = mock.Mock(name='app')
        self.app.client_manager = mock.Mock(name='client_manager')
        self.namespace = argparse.Namespace()

    given_show_options = [
        '-f',
        'shell',
        '-c',
        'id',
        '--prefix',
        'TST',
    ]
    then_show_options = [
        ('formatter', 'shell'),
        ('columns', ['id']),
        ('prefix', 'TST'),
    ]
    given_list_options = [
        '-f',
        'csv',
        '-c',
        'id',
        '--quote',
        'all',
    ]
    then_list_options = [
        ('formatter', 'csv'),
        ('columns', ['id']),
        ('quote_mode', 'all'),
    ]
