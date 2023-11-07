from lqs.interface.core import UpdateInterface

from lqs.client.common import RESTInterface


class Update(UpdateInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _api_key(self, **params) -> dict:
        api_key_id = params.pop("api_key_id")
        data = params.pop("data")
        return self._update_resource(f"apiKeys/{api_key_id}", data)

    def _digestion(self, **params) -> dict:
        digestion_id = params.pop("digestion_id")
        data = params.pop("data")
        return self._update_resource(f"digestions/{digestion_id}", data)

    def _digestion_part(self, **params) -> dict:
        digestion_id = params.pop("digestion_id")
        digestion_part_id = params.pop("digestion_part_id")
        data = params.pop("data")
        return self._update_resource(
            f"digestions/{digestion_id}/parts/{digestion_part_id}", data
        )

    def _digestion_topic(self, **params) -> dict:
        digestion_id = params.pop("digestion_id")
        digestion_topic_id = params.pop("digestion_topic_id")
        data = params.pop("data")
        return self._update_resource(
            f"digestions/{digestion_id}/topics/{digestion_topic_id}", data
        )

    def _group(self, **params) -> dict:
        group_id = params.pop("group_id")
        data = params.pop("data")
        return self._update_resource(f"groups/{group_id}", data)

    def _hook(self, **params) -> dict:
        workflow_id = params.pop("workflow_id")
        hook_id = params.pop("hook_id")
        data = params.pop("data")
        return self._update_resource(f"workflows/{workflow_id}/hooks/{hook_id}", data)

    def _ingestion(self, **params) -> dict:
        ingestion_id = params.pop("ingestion_id")
        data = params.pop("data")
        return self._update_resource(f"ingestions/{ingestion_id}", data)

    def _ingestion_part(self, **params) -> dict:
        ingestion_id = params.pop("ingestion_id")
        ingestion_part_id = params.pop("ingestion_part_id")
        data = params.pop("data")
        return self._update_resource(
            f"ingestions/{ingestion_id}/parts/{ingestion_part_id}", data
        )

    def _label(self, **params) -> dict:
        label_id = params.pop("label_id")
        data = params.pop("data")
        return self._update_resource(f"labels/{label_id}", data)

    def _log(self, **params) -> dict:
        log_id = params.pop("log_id")
        data = params.pop("data")
        return self._update_resource(f"logs/{log_id}", data)

    def _object_store(self, **params) -> dict:
        object_store_id = params.pop("object_store_id")
        data = params.pop("data")
        return self._update_resource(f"objectStores/{object_store_id}", data)

    def _query(self, **params) -> dict:
        log_id = params.pop("log_id")
        query_id = params.pop("query_id")
        data = params.pop("data")
        return self._update_resource(f"logs/{log_id}/queries/{query_id}", data)

    def _record(self, **params) -> dict:
        topic_id = params.pop("topic_id")
        timestamp = params.pop("timestamp")
        data = params.pop("data")
        return self._update_resource(f"topics/{topic_id}/records/{timestamp}", data)

    def _role(self, **params) -> dict:
        role_id = params.pop("role_id")
        data = params.pop("data")
        return self._update_resource(f"roles/{role_id}", data)

    def _tag(self, **params) -> dict:
        log_id = params.pop("log_id")
        tag_id = params.pop("tag_id")
        data = params.pop("data")
        return self._update_resource(f"logs/{log_id}/tags/{tag_id}", data)

    def _topic(self, **params) -> dict:
        topic_id = params.pop("topic_id")
        data = params.pop("data")
        return self._update_resource(f"topics/{topic_id}", data)

    def _user(self, **params) -> dict:
        user_id = params.pop("user_id")
        data = params.pop("data")
        return self._update_resource(f"users/{user_id}", data)

    def _workflow(self, **params) -> dict:
        workflow_id = params.pop("workflow_id")
        data = params.pop("data")
        return self._update_resource(f"workflows/{workflow_id}", data)

    # Objects

    def _object(self, **params) -> dict:
        log_id = params.pop("log_id")
        object_key = params.pop("object_key")
        data = params.pop("data")
        return self._update_resource(f"logs/{log_id}/objects/{object_key}", data)
