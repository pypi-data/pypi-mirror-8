import os
import testtools

from tempest import clients
from tempest.common import rest_client

from mistralclient.api import base
from mistralclient.api.v1 import client as mclient


class ClientAuth(rest_client.RestClient):
    def __init__(self, auth_provider, url):
        super(ClientAuth, self).__init__(auth_provider)

        self.mistral_client = mclient.Client(
            auth_token=self.auth_provider.get_token(),
            mistral_url=url)


class MistralBase(testtools.TestCase):

    _mistral_url = None

    @classmethod
    def setUpClass(cls):
        super(MistralBase, cls).setUpClass()

        if 'WITHOUT_AUTH' in os.environ:
            cls.mistral_client = mclient.Client(
                mistral_url=cls._mistral_url)
        else:
            mgr = clients.Manager()
            cls.mistral_client = ClientAuth(
                mgr.auth_provider, cls._mistral_url).mistral_client

        cls.definition = open(os.path.relpath(
            'functionaltests/resources/v1/wb_v1.yaml',
            os.getcwd()), 'rb').read()

        cls.wb = cls.mistral_client.workbooks.create(
            "wb", "Description", ["tags"])

    @classmethod
    def tearDownClass(cls):
        super(MistralBase, cls).tearDownClass()

        for wb in cls.mistral_client.workbooks.list():
            cls.mistral_client.workbooks.delete(wb.name)

    def tearDown(self):
        super(MistralBase, self).tearDown()
        for ex in self.mistral_client.executions.list(None):
            # TODO(akuznetsova): remove try/except after
            # https://bugs.launchpad.net/mistral/+bug/1353306
            # will be fixed
            """ try/except construction was added because of problem
                with concurrent transactions in sqlite and appropriate
                error: APIException: (OperationalError) database is locked.
                This isn't a tests problem, so they are considered passed.
            """
            try:
                self.mistral_client.executions.delete(None, ex.id)
            except base.APIException:
                pass

    def create_execution(self):
        self.mistral_client.workbooks.upload_definition("wb", self.definition)
        execution = self.mistral_client.executions.create("wb", "hello")
        return execution

    def assert_item_in_list(self, items, **props):
        def _matches(item, **props):
            for prop_name, prop_val in props.iteritems():
                v = item[prop_name] if isinstance(item, dict) \
                    else getattr(item, prop_name)

                if v != prop_val:
                    return False

            return True

        filtered_items = filter(lambda item: _matches(item, **props), items)

        return len(filtered_items) != 0
