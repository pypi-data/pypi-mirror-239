from lqs.interface.dsm import ListInterface

from lqs.client.common import RESTInterface


class List(ListInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _api_key(self, **params) -> dict:
        resource_path = "apiKeys" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _datastore(self, **params) -> dict:
        resource_path = "dataStores" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _datastore_association(self, **params) -> dict:
        resource_path = "dataStoreAssociations" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _role(self, **params) -> dict:
        topic_id = params.pop("topic_id")
        resource_path = f"topics/{topic_id}/rows" + self._get_url_param_string(
            params, []
        )
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _user(self, **params) -> dict:
        resource_path = "users" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result
