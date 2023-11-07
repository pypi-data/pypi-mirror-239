from lqs.interface.process import UpdateInterface

from lqs.client.common import RESTInterface


class Update(UpdateInterface, RESTInterface):
    def __init__(self, config, http_client=None):
        super().__init__(config=config, http_client=http_client)

    def _event(self, **params) -> dict:
        event_id = params.pop("event_id")
        data = params.pop("data")
        return self._update_resource(f"events/{event_id}", data)

    def _job(self, **params) -> dict:
        job_id = params.pop("job_id")
        data = params.pop("data")
        return self._update_resource(f"jobs/{job_id}", data)
