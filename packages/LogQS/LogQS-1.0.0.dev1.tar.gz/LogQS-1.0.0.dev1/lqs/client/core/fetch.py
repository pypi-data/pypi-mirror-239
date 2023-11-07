from lqs.interface.core import FetchInterface

from lqs.client.common import RESTInterface


class Fetch(FetchInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _api_key(self, **params):
        api_key_id = params.pop("api_key_id")
        result = self._get_resource(f"apiKeys/{api_key_id}")
        return result

    def _digestion(self, **params):
        digestion_id = params.pop("digestion_id")
        result = self._get_resource(f"digestions/{digestion_id}")
        return result

    def _digestion_part(self, **kwargs):
        digestion_id = kwargs.pop("digestion_id")
        digestion_part_id = kwargs.pop("digestion_part_id")
        result = self._get_resource(
            f"digestions/{digestion_id}/parts/{digestion_part_id}"
        )
        return result

    def _digestion_topic(self, **params):
        digestion_id = params.pop("digestion_id")
        digestion_topic_id = params.pop("digestion_topic_id")
        result = self._get_resource(
            f"digestions/{digestion_id}/topics/{digestion_topic_id}"
        )
        return result

    def _group(self, **params):
        group_id = params.pop("group_id")
        result = self._get_resource(f"groups/{group_id}")
        return result

    def _hook(self, **params):
        workflow_id = params.pop("workflow_id")
        hook_id = params.pop("hook_id")
        result = self._get_resource(f"workflows/{workflow_id}/hooks/{hook_id}")
        return result

    def _ingestion(self, **params):
        ingestion_id = params.pop("ingestion_id")
        result = self._get_resource(f"ingestions/{ingestion_id}")
        return result

    def _ingestion_part(self, **params):
        ingestion_id = params.pop("ingestion_id")
        ingestion_part_id = params.pop("ingestion_part_id")
        result = self._get_resource(
            f"ingestions/{ingestion_id}/parts/{ingestion_part_id}"
        )
        return result

    def _label(self, **params):
        label_id = params.pop("label_id")
        result = self._get_resource(f"labels/{label_id}")
        return result

    def _log(self, **params):
        log_id = params.pop("log_id")
        result = self._get_resource(f"logs/{log_id}")
        return result

    def _object_store(self, **params):
        object_store_id = params.pop("object_store_id")
        result = self._get_resource(f"objectStores/{object_store_id}")
        return result

    def _me(self, **params):
        result = self._get_resource("users/me")
        return result

    def _query(self, **params):
        log_id = params.pop("log_id")
        query_id = params.pop("query_id")
        result = self._get_resource(f"logs/{log_id}/queries/{query_id}")
        return result

    def _record(self, **params):
        topic_id = params.pop("topic_id")
        timestamp = params.pop("timestamp")
        result = self._get_resource(f"topics/{topic_id}/records/{timestamp}")
        return result

    def _role(self, **params):
        role_id = params.pop("role_id")
        result = self._get_resource(f"roles/{role_id}")
        return result

    def _tag(self, **params):
        log_id = params.pop("log_id")
        tag_id = params.pop("tag_id")
        result = self._get_resource(f"logs/{log_id}/tags/{tag_id}")
        return result

    def _topic(self, **params):
        topic_id = params.pop("topic_id")
        result = self._get_resource(f"topics/{topic_id}")
        return result

    def _user(self, **params):
        user_id = params.pop("user_id")
        result = self._get_resource(f"users/{user_id}")
        return result

    def _workflow(self, **params):
        workflow_id = params.pop("workflow_id")
        result = self._get_resource(f"workflows/{workflow_id}")
        return result

    # Objects

    def _object(self, **params):
        log_id = params.pop("log_id")
        object_store_id = params.pop("object_store_id")
        object_key = params.pop("object_key")

        if log_id is not None:
            if object_store_id is not None:
                raise ValueError(
                    "log_id and object_store_id cannot be specified at the same time"
                )
            resource_path = (
                f"logs/{log_id}/objects/{object_key}"
                + self._get_url_param_string(params, [])
            )
        elif object_store_id is not None:
            resource_path = (
                f"objectStores/{object_store_id}/objects/{object_key}"
                + self._get_url_param_string(params, [])
            )
        else:
            raise ValueError("Either log_id or object_store_id must be specified")

        if params.get("redirect", False):
            offset = params.pop("offset", None)
            length = params.pop("length", None)
            headers = {}
            if offset is not None:
                if length is not None:
                    headers["Range"] = f"bytes={offset}-{offset + length - 1}"
                else:
                    headers["Range"] = f"bytes={offset}-"
            elif length is not None:
                headers["Range"] = f"bytes=0-{length - 1}"
            result = self._get_resource(
                resource_path, expected_content_type=None, additional_headers=headers
            )
        else:
            result = self._get_resource(resource_path)
        return result

    def _object_part(self, **params):
        log_id = params.pop("log_id")
        object_key = params.pop("object_key")
        part_number = params.pop("part_number")
        result = self._get_resource(
            f"logs/{log_id}/objects/{object_key}/parts/{part_number}"
        )
        return result
