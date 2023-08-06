# Copyright 2014 - Mirantis, Inc.
# All Rights Reserved
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

import argparse
import logging

from cliff import command
from cliff import show

from mistralclient.api.v2 import actions
from mistralclient.commands.v2 import base

LOG = logging.getLogger(__name__)


def format_list(action=None):
    return format(action, lister=True)


def format(action=None, lister=False):
    columns = (
        'Name',
        'Is system',
        'Input',
        'Description',
        'Tags',
        'Created at',
        'Updated at'
    )

    if action:
        tags = getattr(action, 'tags', None) or []
        input = action.input if not lister else base.cut(action.input)
        desc = (action.description if not lister
                else base.cut(action.description))

        data = (
            action.name,
            action.is_system,
            input,
            desc,
            ', '.join(tags) or '<none>',
            action.created_at,
        )

        if hasattr(action, 'updated_at'):
            data += (action.updated_at,)
        else:
            data += (None,)
    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


class List(base.MistralLister):
    """List all actions."""

    def _get_format_function(self):
        return format_list

    def _get_resources(self, parsed_args):
        return actions.ActionManager(self.app.client).list()


class Get(show.ShowOne):
    """Show specific action."""

    def get_parser(self, prog_name):
        parser = super(Get, self).get_parser(prog_name)

        parser.add_argument('name', help='Action name')

        return parser

    def take_action(self, parsed_args):
        action = actions.ActionManager(self.app.client).get(
            parsed_args.name)

        return format(action)


class Create(base.MistralLister):
    """Create new action."""

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)

        parser.add_argument(
            'definition',
            type=argparse.FileType('r'),
            help='Action definition file'
        )

        return parser

    def _validate_parsed_args(self, parsed_args):
        if not parsed_args.definition:
            raise RuntimeError("Provide action definition file.")

    def _get_format_function(self):
        return format

    def _get_resources(self, parsed_args):
        return actions.ActionManager(self.app.client)\
            .create(parsed_args.definition.read())


class Delete(command.Command):
    """Delete action."""

    def get_parser(self, prog_name):
        parser = super(Delete, self).get_parser(prog_name)

        parser.add_argument('name', help='Action name')

        return parser

    def take_action(self, parsed_args):
        actions.ActionManager(self.app.client).delete(parsed_args.name)


class Update(base.MistralLister):
    """Update action."""

    def get_parser(self, prog_name):
        parser = super(Update, self).get_parser(prog_name)

        parser.add_argument(
            'definition',
            type=argparse.FileType('r'),
            help='Action definition file'
        )

        return parser

    def _get_format_function(self):
        return format

    def _get_resources(self, parsed_args):
        return actions.ActionManager(self.app.client).\
            update(parsed_args.definition.read())


class GetDefinition(command.Command):
    """Show action definition."""

    def get_parser(self, prog_name):
        parser = super(GetDefinition, self).get_parser(prog_name)

        parser.add_argument('name', help='Action name')

        return parser

    def take_action(self, parsed_args):
        definition = actions.ActionManager(self.app.client)\
            .get(parsed_args.name).definition

        self.app.stdout.write(definition or "\n")
