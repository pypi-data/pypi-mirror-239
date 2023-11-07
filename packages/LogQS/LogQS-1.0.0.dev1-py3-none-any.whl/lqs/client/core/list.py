from lqs.interface.core import ListInterface

from lqs.client.common import RESTInterface


class List(ListInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _api_key(self, **params) -> dict:
        resource_path = "apiKeys" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _digestion(self, **params) -> dict:
        resource_path = "digestions" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _digestion_part(self, **params) -> dict:
        digestion_id = params.pop("digestion_id")
        resource_path = f"digestions/{digestion_id}/parts" + self._get_url_param_string(
            params, []
        )
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _digestion_topic(self, **params) -> dict:
        digestion_id = params.pop("digestion_id")
        resource_path = (
            f"digestions/{digestion_id}/topics" + self._get_url_param_string(params, [])
        )
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _group(self, **params) -> dict:
        resource_path = "groups" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _hook(self, **params) -> dict:
        workflow_id = params.pop("workflow_id")
        resource_path = f"workflows/{workflow_id}/hooks" + self._get_url_param_string(
            params, []
        )
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _ingestion(self, **params) -> dict:
        resource_path = "ingestions" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _ingestion_part(self, **params) -> dict:
        ingestion_id = params.pop("ingestion_id")
        resource_path = f"ingestions/{ingestion_id}/parts" + self._get_url_param_string(
            params, []
        )
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _label(self, **params) -> dict:
        resource_path = "labels" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _log(self, **params) -> dict:
        resource_path = "logs" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _object_store(self, **params) -> dict:
        resource_path = "objectStores" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _query(self, **params) -> dict:
        log_id = params.pop("log_id")
        resource_path = f"logs/{log_id}/queries" + self._get_url_param_string(
            params, []
        )
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _record(self, **params) -> dict:
        topic_id = params.pop("topic_id")
        resource_path = f"topics/{topic_id}/records" + self._get_url_param_string(
            params, []
        )
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

    def _tag(self, **params) -> dict:
        log_id = params.pop("log_id")
        resource_path = f"logs/{log_id}/tags" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _topic(self, **params) -> dict:
        resource_path = "topics" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _user(self, **params) -> dict:
        resource_path = "users" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _workflow(self, **params) -> dict:
        resource_path = "workflows" + self._get_url_param_string(params, [])
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    # Objects

    def _object(self, **params) -> dict:
        log_id = params.pop("log_id")
        object_store_id = params.pop("object_store_id")
        if log_id is not None:
            if object_store_id is not None:
                raise ValueError(
                    "log_id and object_store_id cannot be specified at the same time"
                )
            resource_path = f"logs/{log_id}/objects" + self._get_url_param_string(
                params, []
            )
        elif object_store_id is not None:
            resource_path = (
                f"objectStores/{object_store_id}/objects"
                + self._get_url_param_string(params, [])
            )
        else:
            raise ValueError("Either log_id or object_store_id must be specified")
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _object_part(self, **params) -> dict:
        log_id = params.pop("log_id")
        object_key = params.pop("object_key")
        resource_path = (
            f"logs/{log_id}/objects/{object_key}/parts"
            + self._get_url_param_string(params, [])
        )
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result

    def _record_object(self, **params) -> dict:
        topic_id = params.pop("topic_id")
        resource_path = f"topics/{topic_id}/objects" + self._get_url_param_string(
            params, []
        )
        result = self._get_resource(resource_path)
        assert isinstance(result, dict)
        return result
