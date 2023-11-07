from lqs.interface.dsm import CreateInterface

from lqs.client.common import RESTInterface


class Create(CreateInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _api_key(self, **params):
        return self._create_resource("apiKeys", params)

    def _datastore(self, **params):
        return self._create_resource("dataStores", params)

    def _datastore_association(self, **params):
        return self._create_resource("dataStoreAssociations", params)

    def _role(self, **params):
        return self._create_resource("roles", params)

    def _user(self, **params):
        return self._create_resource("users", params)
