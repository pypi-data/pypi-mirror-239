from abc import ABC, abstractmethod
from uuid import UUID


class FetchInterface(ABC):
    @abstractmethod
    def _event(self, **kwargs) -> dict:
        pass

    def event(self, event_id: UUID) -> dict:
        return self._event(
            event_id=event_id,
        )

    @abstractmethod
    def _job(self, **kwargs) -> dict:
        pass

    def job(self, job_id: UUID) -> dict:
        return self._job(
            job_id=job_id,
        )
