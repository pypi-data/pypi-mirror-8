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

import mock

from openstackclient.tests import fakes
from openstackclient.tests import utils


domain_id = 'd1'
domain_name = 'oftheking'
domain_description = 'domain description'

DOMAIN = {
    'id': domain_id,
    'name': domain_name,
    'description': domain_description,
    'enabled': True,
}

group_id = 'gr-010'
group_name = 'spencer davis'

GROUP = {
    'id': group_id,
    'name': group_name,
}

project_id = '8-9-64'
project_name = 'beatles'
project_description = 'Fab Four'

PROJECT = {
    'id': project_id,
    'name': project_name,
    'description': project_description,
    'enabled': True,
    'domain_id': domain_id,
}

PROJECT_2 = {
    'id': project_id + '-2222',
    'name': project_name + ' reprise',
    'description': project_description + 'plus four more',
    'enabled': True,
    'domain_id': domain_id,
}

role_id = 'r1'
role_name = 'roller'

ROLE = {
    'id': role_id,
    'name': role_name,
}

service_id = 's-123'
service_name = 'Texaco'
service_type = 'gas'

SERVICE = {
    'id': service_id,
    'name': service_name,
    'type': service_type,
    'enabled': True,
}

endpoint_id = 'e-123'
endpoint_url = 'http://127.0.0.1:35357'
endpoint_region = 'RegionOne'
endpoint_interface = 'admin'

ENDPOINT = {
    'id': endpoint_id,
    'url': endpoint_url,
    'region': endpoint_region,
    'interface': endpoint_interface,
    'service_id': service_id,
    'enabled': True,
}

user_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
user_name = 'paul'
user_description = 'Sir Paul'
user_email = 'paul@applecorps.com'

USER = {
    'id': user_id,
    'name': user_name,
    'project_id': project_id,
    'email': user_email,
    'enabled': True,
    'domain_id': domain_id,
}

token_expires = '2014-01-01T00:00:00Z'
token_id = 'tttttttt-tttt-tttt-tttt-tttttttttttt'

TOKEN_WITH_TENANT_ID = {
    'expires': token_expires,
    'id': token_id,
    'tenant_id': project_id,
    'user_id': user_id,
}

TOKEN_WITH_DOMAIN_ID = {
    'expires': token_expires,
    'id': token_id,
    'domain_id': domain_id,
    'user_id': user_id,
}

idp_id = 'test_idp'
idp_description = 'super exciting IdP description'

IDENTITY_PROVIDER = {
    'id': idp_id,
    'enabled': True,
    'description': idp_description
}

# Assignments

ASSIGNMENT_WITH_PROJECT_ID_AND_USER_ID = {
    'scope': {'project': {'id': project_id}},
    'user': {'id': user_id},
    'role': {'id': role_id},
}

ASSIGNMENT_WITH_PROJECT_ID_AND_GROUP_ID = {
    'scope': {'project': {'id': project_id}},
    'group': {'id': group_id},
    'role': {'id': role_id},
}

ASSIGNMENT_WITH_DOMAIN_ID_AND_USER_ID = {
    'scope': {'domain': {'id': domain_id}},
    'user': {'id': user_id},
    'role': {'id': role_id},
}

ASSIGNMENT_WITH_DOMAIN_ID_AND_GROUP_ID = {
    'scope': {'domain': {'id': domain_id}},
    'group': {'id': group_id},
    'role': {'id': role_id},
}

consumer_id = 'test consumer id'
consumer_description = 'someone we trust'
consumer_secret = 'test consumer secret'

OAUTH_CONSUMER = {
    'id': consumer_id,
    'secret': consumer_secret,
    'description': consumer_description
}

access_token_id = 'test access token id'
access_token_secret = 'test access token secret'
access_token_expires = '2014-05-18T03:13:18.152071Z'

OAUTH_ACCESS_TOKEN = {
    'id': access_token_id,
    'expires': access_token_expires,
    'key': access_token_id,
    'secret': access_token_secret
}

request_token_id = 'test request token id'
request_token_secret = 'test request token secret'
request_token_expires = '2014-05-17T11:10:51.511336Z'

OAUTH_REQUEST_TOKEN = {
    'id': request_token_id,
    'expires': request_token_expires,
    'key': request_token_id,
    'secret': request_token_secret
}

oauth_verifier_pin = '6d74XaDS'
OAUTH_VERIFIER = {
    'oauth_verifier': oauth_verifier_pin
}


class FakeIdentityv3Client(object):
    def __init__(self, **kwargs):
        self.domains = mock.Mock()
        self.domains.resource_class = fakes.FakeResource(None, {})
        self.endpoints = mock.Mock()
        self.endpoints.resource_class = fakes.FakeResource(None, {})
        self.groups = mock.Mock()
        self.groups.resource_class = fakes.FakeResource(None, {})
        self.oauth1 = mock.Mock()
        self.oauth1.resource_class = fakes.FakeResource(None, {})
        self.projects = mock.Mock()
        self.projects.resource_class = fakes.FakeResource(None, {})
        self.roles = mock.Mock()
        self.roles.resource_class = fakes.FakeResource(None, {})
        self.services = mock.Mock()
        self.services.resource_class = fakes.FakeResource(None, {})
        self.service_catalog = mock.Mock()
        self.users = mock.Mock()
        self.users.resource_class = fakes.FakeResource(None, {})
        self.role_assignments = mock.Mock()
        self.role_assignments.resource_class = fakes.FakeResource(None, {})
        self.auth_token = kwargs['token']
        self.management_url = kwargs['endpoint']


class FakeFederationManager(object):
    def __init__(self, **kwargs):
        self.identity_providers = mock.Mock()
        self.identity_providers.resource_class = fakes.FakeResource(None, {})


class FakeFederatedClient(FakeIdentityv3Client):
    def __init__(self, **kwargs):
        super(FakeFederatedClient, self).__init__(**kwargs)
        self.federation = FakeFederationManager()


class FakeOAuth1Client(FakeIdentityv3Client):
    def __init__(self, **kwargs):
        super(FakeOAuth1Client, self).__init__(**kwargs)

        self.access_tokens = mock.Mock()
        self.access_tokens.resource_class = fakes.FakeResource(None, {})
        self.consumers = mock.Mock()
        self.consumers.resource_class = fakes.FakeResource(None, {})
        self.request_tokens = mock.Mock()
        self.request_tokens.resource_class = fakes.FakeResource(None, {})


class TestIdentityv3(utils.TestCommand):
    def setUp(self):
        super(TestIdentityv3, self).setUp()

        self.app.client_manager.identity = FakeIdentityv3Client(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN,
        )


class TestFederatedIdentity(utils.TestCommand):
    def setUp(self):
        super(TestFederatedIdentity, self).setUp()

        self.app.client_manager.identity = FakeFederatedClient(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN
        )


class TestOAuth1(utils.TestCommand):
    def setUp(self):
        super(TestOAuth1, self).setUp()

        self.app.client_manager.identity = FakeOAuth1Client(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN
        )
