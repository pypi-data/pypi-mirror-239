from abc import ABC, abstractmethod
from uuid import UUID

from lqs.interface.process.models import (
    EventUpdateRequest,
    JobUpdateRequest,
)


class UpdateInterface(ABC):
    def _process_data(self, data):
        if not isinstance(data, dict):
            return data.model_dump(exclude_unset=True)
        return data

    @abstractmethod
    def _event(self, **kwargs) -> dict:
        pass

    def event(self, event_id: UUID, data: dict) -> dict:
        return self._event(
            event_id=event_id,
            data=self._process_data(data),
        )

    def _event_by_model(self, event_id: UUID, data: EventUpdateRequest) -> dict:
        return self._event(
            event_id=event_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _job(self, **kwargs) -> dict:
        pass

    def job(self, job_id: UUID, data: dict) -> dict:
        return self._job(
            job_id=job_id,
            data=self._process_data(data),
        )

    def _job_by_model(self, job_id: UUID, data: JobUpdateRequest) -> dict:
        return self._job(
            job_id=job_id,
            data=data.model_dump(exclude_unset=True),
        )
