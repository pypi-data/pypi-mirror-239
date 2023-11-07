from lqs.interface.dsm import UpdateInterface

from lqs.client.common import RESTInterface


class Update(UpdateInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _api_key(self, **params) -> dict:
        api_key_id = params.pop("api_key_id")
        data = params.pop("data")
        return self._update_resource(f"apiKeys/{api_key_id}", data)

    def _datastore(self, **params) -> dict:
        datastore_id = params.pop("datastore_id")
        data = params.pop("data")
        return self._update_resource(f"dataStores/{datastore_id}", data)

    def _datastore_association(self, **params) -> dict:
        datastore_association_id = params.pop("datastore_association_id")
        data = params.pop("data")
        return self._update_resource(
            f"dataStoreAssociations/{datastore_association_id}", data
        )

    def _role(self, **params) -> dict:
        role_id = params.pop("role_id")
        data = params.pop("data")
        return self._update_resource(f"roles/{role_id}", data)

    def _user(self, **params) -> dict:
        user_id = params.pop("user_id")
        data = params.pop("data")
        return self._update_resource(f"users/{user_id}", data)
