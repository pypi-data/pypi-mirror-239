from lqs.interface.core import CreateInterface

from lqs.client.common import RESTInterface


class Create(CreateInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _api_key(self, **params):
        return self._create_resource("apiKeys", params)

    def _digestion(self, **params):
        return self._create_resource("digestions", params)

    def _digestion_part(self, **kwargs):
        digestion_id = kwargs.pop("digestion_id")
        return self._create_resource(f"digestions/{digestion_id}/parts", kwargs)

    def _digestion_topic(self, **params):
        digestion_id = params.pop("digestion_id")
        return self._create_resource(f"digestions/{digestion_id}/topics", params)

    def _hook(self, **params):
        workflow_id = params.pop("workflow_id")
        return self._create_resource(f"workflows/{workflow_id}/hooks", params)

    def _group(self, **params):
        return self._create_resource("groups", params)

    def _ingestion(self, **params):
        return self._create_resource("ingestions", params)

    def _ingestion_part(self, **params):
        ingestion_id = params.pop("ingestion_id")
        return self._create_resource(f"ingestions/{ingestion_id}/parts", params)

    def _label(self, **params):
        return self._create_resource("labels", params)

    def _log(self, **params):
        return self._create_resource("logs", params)

    def _object_store(self, **params):
        return self._create_resource("objectStores", params)

    def _query(self, **params):
        log_id = params.pop("log_id")
        return self._create_resource(f"logs/{log_id}/queries", params)

    def _record(self, **params):
        topic_id = params.pop("topic_id")
        return self._create_resource(f"topics/{topic_id}/records", params)

    def _role(self, **params):
        return self._create_resource("roles", params)

    def _tag(self, **params):
        log_id = params.pop("log_id")
        return self._create_resource(f"logs/{log_id}/tags", params)

    def _topic(self, **params):
        return self._create_resource("topics", params)

    def _user(self, **params):
        return self._create_resource("users", params)

    def _workflow(self, **params):
        return self._create_resource("workflows", params)

    # Objects

    def _object(self, **params):
        log_id = params.pop("log_id")
        return self._create_resource(f"logs/{log_id}/objects", params)

    def _object_part(self, **params):
        log_id = params.pop("log_id")
        object_key = params.pop("object_key")
        return self._create_resource(
            f"logs/{log_id}/objects/{object_key}/parts", params
        )
