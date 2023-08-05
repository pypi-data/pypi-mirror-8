#   Copyright 2013 Nebula Inc.
#
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

from openstackclient.tests import fakes
from openstackclient.tests import utils


container_name = 'bit-bucket'
container_bytes = 1024
container_count = 1

container_name_2 = 'archive'
container_name_3 = 'bit-blit'

CONTAINER = {
    'name': container_name,
    'bytes': container_bytes,
    'count': container_count,
}

CONTAINER_2 = {
    'name': container_name_2,
    'bytes': container_bytes * 2,
    'count': container_count * 2,
}

CONTAINER_3 = {
    'name': container_name_3,
    'bytes': container_bytes * 3,
    'count': container_count * 3,
}

object_name_1 = 'punch-card'
object_bytes_1 = 80
object_hash_1 = '1234567890'
object_content_type_1 = 'text'
object_modified_1 = 'today'

object_name_2 = 'floppy-disk'
object_bytes_2 = 1440000
object_hash_2 = '0987654321'
object_content_type_2 = 'text'
object_modified_2 = 'today'

OBJECT = {
    'name': object_name_1,
    'bytes': object_bytes_1,
    'hash': object_hash_1,
    'content_type': object_content_type_1,
    'last_modified': object_modified_1,
}

OBJECT_2 = {
    'name': object_name_2,
    'bytes': object_bytes_2,
    'hash': object_hash_2,
    'content_type': object_content_type_2,
    'last_modified': object_modified_2,
}


class FakeObjectv1Client(object):
    def __init__(self, **kwargs):
        self.endpoint = kwargs['endpoint']
        self.token = kwargs['token']


class TestObjectv1(utils.TestCommand):
    def setUp(self):
        super(TestObjectv1, self).setUp()

        self.app.client_manager.object_store = FakeObjectv1Client(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN,
        )
