# Copyright 2014 Mirantis, Inc.
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

import mock

from mistralclient.tests.unit import base

from mistralclient.commands.v2 import cron_triggers as cron_triggers_cmd
from mistralclient.api.v2 import cron_triggers


TRIGGER_DICT = {
    'name': 'my_trigger',
    'pattern': '* * * * *',
    'workflow_name': 'flow1',
    'workflow_input': {},
    'next_execution_time': '1',
    'created_at': '1',
    'updated_at': '1'
}


TRIGGER = cron_triggers.CronTrigger(mock, TRIGGER_DICT)


class TestCLIWorkbooksV2(base.BaseCommandTest):
    @mock.patch('argparse.open', create=True)
    @mock.patch('mistralclient.api.v2.cron_triggers.CronTriggerManager.create')
    def test_create(self, mock, mock_open):
        mock.return_value = TRIGGER
        mock_open.return_value = mock.MagicMock(spec=file)

        result = self.call(
            cron_triggers_cmd.Create,
            app_args=['my_trigger', '* * * * *', 'flow1']
        )

        self.assertEqual(
            ('my_trigger', '* * * * *', 'flow1', '1', '1', '1'),
            result[1]
        )

    @mock.patch('mistralclient.api.v2.cron_triggers.CronTriggerManager.list')
    def test_list(self, mock):
        mock.return_value = (TRIGGER,)

        result = self.call(cron_triggers_cmd.List)

        self.assertEqual(
            [('my_trigger', '* * * * *', 'flow1', '1', '1', '1')],
            result[1]
        )

    @mock.patch('mistralclient.api.v2.cron_triggers.CronTriggerManager.get')
    def test_get(self, mock):
        mock.return_value = TRIGGER

        result = self.call(cron_triggers_cmd.Get, app_args=['name'])

        self.assertEqual(
            ('my_trigger', '* * * * *', 'flow1', '1', '1', '1'),
            result[1]
        )

    @mock.patch('mistralclient.api.v2.cron_triggers.CronTriggerManager.delete')
    def test_delete(self, mock):
        self.assertIsNone(
            self.call(cron_triggers_cmd.Delete, app_args=['name'])
        )
