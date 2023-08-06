# Copyright 2014 StackStorm, Inc.
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

import pkg_resources as pkg

import mock

from mistralclient.tests.unit import base
from mistralclient.commands.v1 import executions
from mistralclient.api.v1.executions import Execution

EXECUTION = Execution(mock, {
    'id': '123',
    'workbook_name': 'some',
    'task': 'else',
    'state': 'RUNNING'
})


class TestCLIExecutions(base.BaseCommandTest):
    @mock.patch('mistralclient.api.v1.executions.ExecutionManager.create')
    def test_create_ctx_string(self, mock):
        mock.return_value = EXECUTION

        result = self.call(executions.Create,
                           app_args=['name', 'id', '{ "context": true }'])

        self.assertEqual(('123', 'some', 'else', 'RUNNING'), result[1])

    @mock.patch('mistralclient.api.v1.executions.ExecutionManager.create')
    def test_create_ctx_file(self, mock):
        mock.return_value = EXECUTION
        path = pkg.resource_filename('mistralclient',
                                     'tests/unit/resources/ctx.json')
        result = self.call(executions.Create,
                           app_args=['name', 'id', path])

        self.assertEqual(('123', 'some', 'else', 'RUNNING'), result[1])

    @mock.patch('mistralclient.api.v1.executions.ExecutionManager.update')
    def test_update(self, mock):
        mock.return_value = EXECUTION

        result = self.call(executions.Update,
                           app_args=['name', 'id', 'SUCCESS'])

        self.assertEqual(('123', 'some', 'else', 'RUNNING'), result[1])

    @mock.patch('mistralclient.api.v1.executions.ExecutionManager.list')
    def test_list(self, mock):
        mock.return_value = (EXECUTION,)

        result = self.call(executions.List, app_args=['name'])

        self.assertEqual([('123', 'some', 'else', 'RUNNING')], result[1])

    @mock.patch('mistralclient.api.v1.executions.ExecutionManager.get')
    def test_get(self, mock):
        mock.return_value = EXECUTION

        result = self.call(executions.Get, app_args=['name', 'id'])

        self.assertEqual(('123', 'some', 'else', 'RUNNING'), result[1])

    @mock.patch('mistralclient.api.v1.executions.ExecutionManager.delete')
    def test_delete(self, mock):
        result = self.call(executions.Delete, app_args=['name', 'id'])

        self.assertIsNone(result)
