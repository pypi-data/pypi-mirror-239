from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from lqs.interface.core.models import (
    APIKeyUpdateRequest,
    DigestionUpdateRequest,
    DigestionPartUpdateRequest,
    DigestionTopicUpdateRequest,
    GroupUpdateRequest,
    HookUpdateRequest,
    IngestionUpdateRequest,
    IngestionPartUpdateRequest,
    LabelUpdateRequest,
    LogUpdateRequest,
    ObjectStoreUpdateRequest,
    QueryUpdateRequest,
    RecordUpdateRequest,
    RoleUpdateRequest,
    TagUpdateRequest,
    TopicUpdateRequest,
    UserUpdateRequest,
    WorkflowUpdateRequest,
)

from lqs.interface.base.models import ObjectUpdateRequest


class UpdateInterface(ABC):
    def _process_data(self, data):
        if not isinstance(data, dict):
            return data.model_dump(exclude_unset=True)
        return data

    @abstractmethod
    def _api_key(self, **kwargs) -> dict:
        pass

    def api_key(self, api_key_id: UUID, data: dict) -> dict:
        return self._api_key(
            api_key_id=api_key_id,
            data=self._process_data(data),
        )

    def _api_key_by_model(self, api_key_id: UUID, data: APIKeyUpdateRequest) -> dict:
        return self._api_key(
            api_key_id=api_key_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _digestion(self, **kwargs) -> dict:
        pass

    def digestion(self, digestion_id: UUID, data: dict) -> dict:
        return self._digestion(
            digestion_id=digestion_id,
            data=self._process_data(data),
        )

    def _digestion_by_model(
        self, digestion_id: UUID, data: DigestionUpdateRequest
    ) -> dict:
        return self._digestion(
            digestion_id=digestion_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _digestion_part(self, **kwargs) -> dict:
        pass

    def digestion_part(
        self, digestion_part_id: UUID, data: dict, digestion_id: Optional[UUID] = None
    ) -> dict:
        return self._digestion_part(
            digestion_id=digestion_id,
            digestion_part_id=digestion_part_id,
            data=self._process_data(data),
        )

    def _digestion_part_by_model(
        self,
        digestion_part_id: UUID,
        data: DigestionPartUpdateRequest,
        digestion_id: Optional[UUID] = None,
    ) -> dict:
        return self._digestion_part(
            digestion_id=digestion_id,
            digestion_part_id=digestion_part_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _digestion_topic(self, **kwargs) -> dict:
        pass

    def digestion_topic(
        self,
        digestion_topic_id: UUID,
        data: dict,
        digestion_id: Optional[UUID] = None,
    ) -> dict:
        return self._digestion_topic(
            digestion_id=digestion_id,
            digestion_topic_id=digestion_topic_id,
            data=self._process_data(data),
        )

    def _digestion_topic_by_model(
        self,
        digestion_topic_id: UUID,
        data: DigestionTopicUpdateRequest,
        digestion_id: Optional[UUID] = None,
    ) -> dict:
        return self._digestion_topic(
            digestion_id=digestion_id,
            digestion_topic_id=digestion_topic_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _group(self, **kwargs) -> dict:
        pass

    def group(self, group_id: UUID, data: dict) -> dict:
        return self._group(
            group_id=group_id,
            data=self._process_data(data),
        )

    def _group_by_model(self, group_id: UUID, data: GroupUpdateRequest) -> dict:
        return self._group(
            group_id=group_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _hook(self, **kwargs) -> dict:
        pass

    def hook(
        self, hook_id: UUID, data: dict, workflow_id: Optional[UUID] = None
    ) -> dict:
        return self._hook(
            workflow_id=workflow_id,
            hook_id=hook_id,
            data=self._process_data(data),
        )

    def _hook_by_model(
        self, hook_id: UUID, data: HookUpdateRequest, workflow_id: Optional[UUID] = None
    ) -> dict:
        return self._hook(
            workflow_id=workflow_id,
            hook_id=hook_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _ingestion(self, **kwargs) -> dict:
        pass

    def ingestion(self, ingestion_id: UUID, data: dict) -> dict:
        return self._ingestion(
            ingestion_id=ingestion_id,
            data=self._process_data(data),
        )

    def _ingestion_by_model(
        self, ingestion_id: UUID, data: IngestionUpdateRequest
    ) -> dict:
        return self._ingestion(
            ingestion_id=ingestion_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _ingestion_part(self, **kwargs) -> dict:
        pass

    def ingestion_part(
        self,
        ingestion_part_id: UUID,
        data: dict,
        ingestion_id: Optional[UUID] = None,
    ) -> dict:
        return self._ingestion_part(
            ingestion_id=ingestion_id,
            ingestion_part_id=ingestion_part_id,
            data=self._process_data(data),
        )

    def _ingestion_part_by_model(
        self,
        ingestion_part_id: UUID,
        data: IngestionPartUpdateRequest,
        ingestion_id: Optional[UUID] = None,
    ) -> dict:
        return self._ingestion_part(
            ingestion_id=ingestion_id,
            ingestion_part_id=ingestion_part_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _label(self, **kwargs) -> dict:
        pass

    def label(self, label_id: UUID, data: dict) -> dict:
        return self._label(
            label_id=label_id,
            data=self._process_data(data),
        )

    def _label_by_model(self, label_id: UUID, data: LabelUpdateRequest) -> dict:
        return self._label(
            label_id=label_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _log(self, **kwargs) -> dict:
        pass

    def log(self, log_id: UUID, data: dict) -> dict:
        return self._log(
            log_id=log_id,
            data=self._process_data(data),
        )

    def _log_by_model(self, log_id: UUID, data: LogUpdateRequest) -> dict:
        return self._log(
            log_id=log_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _object_store(self, **kwargs) -> dict:
        pass

    def object_store(self, object_store_id: UUID, data: dict) -> dict:
        return self._object_store(
            object_store_id=object_store_id,
            data=self._process_data(data),
        )

    def _object_store_by_model(
        self, object_store_id: UUID, data: ObjectStoreUpdateRequest
    ) -> dict:
        return self._object_store(
            object_store_id=object_store_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _query(self, **kwargs) -> dict:
        pass

    def query(self, query_id: UUID, data: dict, log_id: Optional[UUID] = None) -> dict:
        return self._query(
            log_id=log_id,
            query_id=query_id,
            data=self._process_data(data),
        )

    def _query_by_model(
        self, query_id: UUID, data: QueryUpdateRequest, log_id: Optional[UUID] = None
    ) -> dict:
        return self._query(
            log_id=log_id,
            query_id=query_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _record(self, **kwargs) -> dict:
        pass

    def record(self, timestamp: float, topic_id: UUID, data: dict) -> dict:
        return self._record(
            timestamp=timestamp,
            topic_id=topic_id,
            data=self._process_data(data),
        )

    def _record_by_model(
        self, timestamp: float, topic_id: UUID, data: RecordUpdateRequest
    ) -> dict:
        return self._record(
            timestamp=timestamp,
            topic_id=topic_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _role(self, **kwargs) -> dict:
        pass

    def role(self, role_id: UUID, data: dict) -> dict:
        return self._role(
            role_id=role_id,
            data=self._process_data(data),
        )

    def _role_by_model(self, role_id: UUID, data: RoleUpdateRequest) -> dict:
        return self._role(
            role_id=role_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _tag(self, **kwargs) -> dict:
        pass

    def tag(self, tag_id: UUID, data: dict, log_id: Optional[UUID] = None) -> dict:
        return self._tag(
            log_id=log_id,
            tag_id=tag_id,
            data=self._process_data(data),
        )

    def _tag_by_model(
        self, tag_id: UUID, data: TagUpdateRequest, log_id: Optional[UUID] = None
    ) -> dict:
        return self._tag(
            log_id=log_id,
            tag_id=tag_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _topic(self, **kwargs) -> dict:
        pass

    def topic(self, topic_id: UUID, data: dict) -> dict:
        return self._topic(
            topic_id=topic_id,
            data=self._process_data(data),
        )

    def _topic_by_model(self, topic_id: UUID, data: TopicUpdateRequest) -> dict:
        return self._topic(
            topic_id=topic_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _user(self, **kwargs) -> dict:
        pass

    def user(self, user_id: UUID, data: dict) -> dict:
        return self._user(user_id=user_id, data=self._process_data(data))

    def _user_by_model(self, user_id: UUID, data: UserUpdateRequest) -> dict:
        return self._user(user_id=user_id, data=data.model_dump(exclude_unset=True))

    @abstractmethod
    def _workflow(self, **kwargs) -> dict:
        pass

    def workflow(self, workflow_id: UUID, data: dict) -> dict:
        return self._workflow(
            workflow_id=workflow_id,
            data=self._process_data(data),
        )

    def _workflow_by_model(
        self, workflow_id: UUID, data: WorkflowUpdateRequest
    ) -> dict:
        return self._workflow(
            workflow_id=workflow_id,
            data=data.model_dump(exclude_unset=True),
        )

    # Objects

    @abstractmethod
    def _object(self, **kwargs) -> dict:
        pass

    def object(self, log_id: UUID, object_key: str, data: dict) -> dict:
        return self._object(
            log_id=log_id,
            object_key=object_key,
            data=self._process_data(data),
        )

    def _object_by_model(
        self, log_id: UUID, object_key: str, data: ObjectUpdateRequest
    ) -> dict:
        return self._object(
            log_id=log_id,
            object_key=object_key,
            data=data.model_dump(exclude_unset=True),
        )
