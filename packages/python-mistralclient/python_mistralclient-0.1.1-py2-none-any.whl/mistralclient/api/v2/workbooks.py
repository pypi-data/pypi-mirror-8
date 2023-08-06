# Copyright 2014 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from mistralclient.api import base


class Workbook(base.Resource):
    resource_name = 'Workbook'


class WorkbookManager(base.ResourceManager):
    resource_class = Workbook

    def create(self, definition):
        self._ensure_not_empty(definition=definition)

        return self._create('/workbooks', {'definition': definition})

    def update(self, definition):
        self._ensure_not_empty(definition=definition)

        return self._update('/workbooks', {'definition': definition})

    def list(self):
        return self._list('/workbooks', response_key='workbooks')

    def get(self, name):
        self._ensure_not_empty(name=name)

        return self._get('/workbooks/%s' % name)

    def delete(self, name):
        self._ensure_not_empty(name=name)

        self._delete('/workbooks/%s' % name)
