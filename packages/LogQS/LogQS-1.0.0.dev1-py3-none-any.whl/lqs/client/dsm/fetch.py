from lqs.interface.dsm import FetchInterface

from lqs.client.common import RESTInterface


class Fetch(FetchInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _api_key(self, **params):
        api_key_id = params.pop("api_key_id")
        result = self._get_resource(f"apiKeys/{api_key_id}")
        return result

    def _datastore(self, **params):
        datastore_id = params.pop("datastore_id")
        result = self._get_resource(f"dataStores/{datastore_id}")
        return result

    def _datastore_association(self, **params):
        datastore_association_id = params.pop("datastore_association_id")
        result = self._get_resource(f"dataStoreAssociations/{datastore_association_id}")
        return result

    def _role(self, **params):
        role_id = params.pop("role_id")
        result = self._get_resource(f"roles/{role_id}")
        return result

    def _user(self, **params):
        user_id = params.pop("user_id")
        result = self._get_resource(f"users/{user_id}")
        return result
