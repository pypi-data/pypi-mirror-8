#   Copyright 2012 OpenStack Foundation
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

"""Identity v2 EC2 Credentials action implementations"""

import logging
import six

from cliff import command
from cliff import lister
from cliff import show

from openstackclient.common import utils


class CreateEC2Creds(show.ShowOne):
    """Create EC2 credentials"""

    log = logging.getLogger(__name__ + ".CreateEC2Creds")

    def get_parser(self, prog_name):
        parser = super(CreateEC2Creds, self).get_parser(prog_name)
        parser.add_argument(
            '--project',
            metavar='<project>',
            help='Specify a project [admin only]',
        )
        parser.add_argument(
            '--user',
            metavar='<user>',
            help='Specify a user [admin only]',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        identity_client = self.app.client_manager.identity

        if parsed_args.project:
            project = utils.find_resource(
                identity_client.tenants,
                parsed_args.project,
            ).id
        else:
            # Get the project from the current auth
            project = identity_client.auth_tenant_id
        if parsed_args.user:
            user = utils.find_resource(
                identity_client.users,
                parsed_args.user,
            ).id
        else:
            # Get the user from the current auth
            user = identity_client.auth_user_id

        creds = identity_client.ec2.create(user, project)

        info = {}
        info.update(creds._info)
        return zip(*sorted(six.iteritems(info)))


class DeleteEC2Creds(command.Command):
    """Delete EC2 credentials"""

    log = logging.getLogger(__name__ + '.DeleteEC2Creds')

    def get_parser(self, prog_name):
        parser = super(DeleteEC2Creds, self).get_parser(prog_name)
        parser.add_argument(
            'access_key',
            metavar='<access-key>',
            help='Credentials access key',
        )
        parser.add_argument(
            '--user',
            metavar='<user>',
            help='Specify a user [admin only]',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        identity_client = self.app.client_manager.identity

        if parsed_args.user:
            user = utils.find_resource(
                identity_client.users,
                parsed_args.user,
            ).id
        else:
            # Get the user from the current auth
            user = identity_client.auth_user_id

        identity_client.ec2.delete(user, parsed_args.access_key)


class ListEC2Creds(lister.Lister):
    """List EC2 credentials"""

    log = logging.getLogger(__name__ + '.ListEC2Creds')

    def get_parser(self, prog_name):
        parser = super(ListEC2Creds, self).get_parser(prog_name)
        parser.add_argument(
            '--user',
            metavar='<user>',
            help='Specify a user [admin only]',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        identity_client = self.app.client_manager.identity

        if parsed_args.user:
            user = utils.find_resource(
                identity_client.users,
                parsed_args.user,
            ).id
        else:
            # Get the user from the current auth
            user = identity_client.auth_user_id

        columns = ('access', 'secret', 'tenant_id', 'user_id')
        column_headers = ('Access', 'Secret', 'Project ID', 'User ID')
        data = identity_client.ec2.list(user)

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters={},
                ) for s in data))


class ShowEC2Creds(show.ShowOne):
    """Show EC2 credentials"""

    log = logging.getLogger(__name__ + '.ShowEC2Creds')

    def get_parser(self, prog_name):
        parser = super(ShowEC2Creds, self).get_parser(prog_name)
        parser.add_argument(
            'access_key',
            metavar='<access-key>',
            help='Credentials access key',
        )
        parser.add_argument(
            '--user',
            metavar='<user>',
            help='Specify a user [admin only]',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        identity_client = self.app.client_manager.identity

        if parsed_args.user:
            user = utils.find_resource(
                identity_client.users,
                parsed_args.user,
            ).id
        else:
            # Get the user from the current auth
            user = identity_client.auth_user_id

        creds = identity_client.ec2.get(user, parsed_args.access_key)

        info = {}
        info.update(creds._info)
        return zip(*sorted(six.iteritems(info)))
