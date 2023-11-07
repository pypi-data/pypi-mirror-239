from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID


class FetchInterface(ABC):
    @abstractmethod
    def _api_key(self, **kwargs) -> dict:
        pass

    def api_key(self, api_key_id: UUID) -> dict:
        return self._api_key(
            api_key_id=api_key_id,
        )

    @abstractmethod
    def _digestion(self, **kwargs) -> dict:
        pass

    def digestion(self, digestion_id: UUID) -> dict:
        return self._digestion(
            digestion_id=digestion_id,
        )

    @abstractmethod
    def _digestion_part(self, **kwargs) -> dict:
        pass

    def digestion_part(
        self, digestion_part_id: UUID, digestion_id: Optional[UUID] = None
    ) -> dict:
        return self._digestion_part(
            digestion_id=digestion_id,
            digestion_part_id=digestion_part_id,
        )

    @abstractmethod
    def _digestion_topic(self, **kwargs) -> dict:
        pass

    def digestion_topic(
        self, digestion_topic_id: UUID, digestion_id: Optional[UUID] = None
    ) -> dict:
        return self._digestion_topic(
            digestion_topic_id=digestion_topic_id,
        )

    @abstractmethod
    def _group(self, **kwargs) -> dict:
        pass

    def group(self, group_id: UUID) -> dict:
        return self._group(
            group_id=group_id,
        )

    @abstractmethod
    def _hook(self, **kwargs) -> dict:
        pass

    def hook(self, hook_id: UUID, workflow_id: Optional[UUID] = None) -> dict:
        return self._hook(
            workflow_id=workflow_id,
            hook_id=hook_id,
        )

    @abstractmethod
    def _ingestion(self, **kwargs) -> dict:
        pass

    def ingestion(self, ingestion_id: UUID) -> dict:
        return self._ingestion(
            ingestion_id=ingestion_id,
        )

    @abstractmethod
    def _ingestion_part(self, **kwargs) -> dict:
        pass

    def ingestion_part(
        self, ingestion_part_id: UUID, ingestion_id: Optional[UUID] = None
    ) -> dict:
        return self._ingestion_part(
            ingestion_id=ingestion_id,
            ingestion_part_id=ingestion_part_id,
        )

    @abstractmethod
    def _label(self, **kwargs) -> dict:
        pass

    def label(self, label_id: UUID) -> dict:
        return self._label(
            label_id=label_id,
        )

    @abstractmethod
    def _log(self, **kwargs) -> dict:
        pass

    def log(self, log_id: UUID) -> dict:
        return self._log(
            log_id=log_id,
        )

    @abstractmethod
    def _object_store(self, **kwargs) -> dict:
        pass

    def object_store(self, object_store_id: UUID) -> dict:
        return self._object_store(
            object_store_id=object_store_id,
        )

    @abstractmethod
    def _me(self, **kwargs) -> dict:
        pass

    def me(self) -> dict:
        return self._me()

    @abstractmethod
    def _query(self, **kwargs) -> dict:
        pass

    def query(self, query_id: UUID, log_id: Optional[UUID] = None) -> dict:
        return self._query(
            log_id=log_id,
            query_id=query_id,
        )

    @abstractmethod
    def _record(self, **kwargs) -> dict:
        pass

    def record(self, timestamp: float, topic_id: UUID) -> dict:
        return self._record(
            timestamp=timestamp,
            topic_id=topic_id,
        )

    @abstractmethod
    def _role(self, **kwargs) -> dict:
        pass

    def role(self, role_id: UUID) -> dict:
        return self._role(
            role_id=role_id,
        )

    @abstractmethod
    def _tag(self, **kwargs) -> dict:
        pass

    def tag(self, tag_id: UUID, log_id: Optional[UUID] = None) -> dict:
        return self._tag(
            log_id=log_id,
            tag_id=tag_id,
        )

    @abstractmethod
    def _topic(self, **kwargs) -> dict:
        pass

    def topic(self, topic_id: UUID) -> dict:
        return self._topic(
            topic_id=topic_id,
        )

    @abstractmethod
    def _user(self, **kwargs) -> dict:
        pass

    def user(self, user_id: UUID) -> dict:
        return self._user(
            user_id=user_id,
        )

    @abstractmethod
    def _workflow(self, **kwargs) -> dict:
        pass

    def workflow(self, workflow_id: UUID) -> dict:
        return self._workflow(
            workflow_id=workflow_id,
        )

    # Objects

    @abstractmethod
    def _object(self, **kwargs) -> dict:
        pass

    def object(
        self,
        object_key: str,
        log_id: Optional[UUID] = None,
        object_store_id: Optional[UUID] = None,
        redirect: Optional[bool] = False,
        offset: Optional[int] = None,
        length: Optional[int] = None,
    ) -> dict | bytes:
        return self._object(
            log_id=log_id,
            object_store_id=object_store_id,
            object_key=object_key,
            redirect=redirect,
            offset=offset,
            length=length,
        )

    @abstractmethod
    def _object_part(self, **kwargs) -> dict:
        pass

    def object_part(self, log_id: UUID, object_key: str, part_number: int) -> dict:
        return self._object_part(
            log_id=log_id,
            object_key=object_key,
            part_number=part_number,
        )
