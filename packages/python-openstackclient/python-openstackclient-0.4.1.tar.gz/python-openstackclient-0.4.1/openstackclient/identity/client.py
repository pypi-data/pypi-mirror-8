#   Copyright 2012-2013 OpenStack Foundation
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

import logging

from keystoneclient.v2_0 import client as identity_client_v2_0
from openstackclient.common import utils


LOG = logging.getLogger(__name__)

DEFAULT_IDENTITY_API_VERSION = '2.0'
API_VERSION_OPTION = 'os_identity_api_version'
API_NAME = 'identity'
API_VERSIONS = {
    '2.0': 'openstackclient.identity.client.IdentityClientv2_0',
    '3': 'keystoneclient.v3.client.Client',
}


def make_client(instance):
    """Returns an identity service client."""
    identity_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)
    LOG.debug('Instantiating identity client: %s', identity_client)

    if instance._url:
        LOG.debug('Using token auth')
        client = identity_client(
            endpoint=instance._url,
            token=instance._token,
            cacert=instance._cacert,
            insecure=instance._insecure,
            trust_id=instance._trust_id,
        )
    else:
        LOG.debug('Using password auth')
        client = identity_client(
            username=instance._username,
            password=instance._password,
            user_domain_id=instance._user_domain_id,
            user_domain_name=instance._user_domain_name,
            project_domain_id=instance._project_domain_id,
            project_domain_name=instance._project_domain_name,
            domain_id=instance._domain_id,
            domain_name=instance._domain_name,
            tenant_name=instance._project_name,
            tenant_id=instance._project_id,
            auth_url=instance._auth_url,
            region_name=instance._region_name,
            cacert=instance._cacert,
            insecure=instance._insecure,
            trust_id=instance._trust_id,
        )

        # TODO(dtroyer): the identity v2 role commands use this yet, fix that
        #                so we can remove it
        instance.auth_ref = client.auth_ref

        # NOTE(dtroyer): this is hanging around until restapi is replace by
        #                ksc session
        instance.session.set_auth(
            client.auth_ref.auth_token,
        )

    return client


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-identity-api-version',
        metavar='<identity-api-version>',
        default=utils.env(
            'OS_IDENTITY_API_VERSION',
            default=DEFAULT_IDENTITY_API_VERSION),
        help='Identity API version, default=' +
             DEFAULT_IDENTITY_API_VERSION +
             ' (Env: OS_IDENTITY_API_VERSION)')
    parser.add_argument(
        '--os-trust-id',
        metavar='<trust-id>',
        default=utils.env('OS_TRUST_ID'),
        help='Trust ID to use when authenticating. '
             'This can only be used with Keystone v3 API '
             '(Env: OS_TRUST_ID)')
    return parser


class IdentityClientv2_0(identity_client_v2_0.Client):
    """Tweak the earlier client class to deal with some changes"""
    def __getattr__(self, name):
        # Map v3 'projects' back to v2 'tenants'
        if name == "projects":
            return self.tenants
        else:
            raise AttributeError(name)
