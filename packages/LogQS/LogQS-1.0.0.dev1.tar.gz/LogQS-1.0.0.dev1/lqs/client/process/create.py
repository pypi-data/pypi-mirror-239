from lqs.interface.process import CreateInterface

from lqs.client.common import RESTInterface


class Create(CreateInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _event(self, **params):
        return self._create_resource("events", params)

    def _job(self, **params):
        return self._create_resource("jobs", params)
