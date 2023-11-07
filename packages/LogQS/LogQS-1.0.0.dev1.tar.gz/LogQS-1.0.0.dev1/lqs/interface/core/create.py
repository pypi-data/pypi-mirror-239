from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from lqs.interface.core.models import (
    APIKeyCreateRequest,
    DigestionCreateRequest,
    DigestionPartCreateRequest,
    DigestionPartIndex,
    DigestionTopicCreateRequest,
    GroupCreateRequest,
    HookCreateRequest,
    IngestionCreateRequest,
    IngestionPartIndex,
    IngestionPartCreateRequest,
    LabelCreateRequest,
    LogCreateRequest,
    ObjectStoreCreateRequest,
    QueryCreateRequest,
    RecordCreateRequest,
    RoleCreateRequest,
    TagCreateRequest,
    TopicCreateRequest,
    UserCreateRequest,
    WorkflowCreateRequest,
)

from lqs.interface.base.models import ObjectCreateRequest, ObjectPartCreateRequest


class CreateInterface(ABC):
    @abstractmethod
    def _api_key(self, **kwargs) -> dict:
        pass

    def api_key(self, user_id: UUID, name: str, disabled: bool = False) -> dict:
        return self._api_key(
            user_id=user_id,
            name=name,
            disabled=disabled,
        )

    def _api_key_by_model(self, data: APIKeyCreateRequest) -> dict:
        return self.api_key(**data.model_dump())

    @abstractmethod
    def _digestion(self, **kwargs) -> dict:
        pass

    def digestion(
        self,
        log_id: UUID,
        name: Optional[str] = None,
        workflow_id: Optional[UUID] = None,
        workflow_context: Optional[dict] = None,
        note: Optional[str] = None,
        context: Optional[dict] = None,
        state: str = "ready",
    ) -> dict:
        return self._digestion(
            log_id=log_id,
            name=name,
            workflow_id=workflow_id,
            workflow_context=workflow_context,
            note=note,
            context=context,
            state=state,
        )

    def _digestion_by_model(self, data: DigestionCreateRequest) -> dict:
        return self.digestion(**data.model_dump())

    @abstractmethod
    def _digestion_part(self, **kwargs) -> dict:
        pass

    def digestion_part(
        self,
        digestion_id: UUID,
        sequence: int,
        workflow_id: Optional[UUID] = None,
        workflow_context: Optional[dict] = None,
        state: str = "queued",
        index: Optional[List[DigestionPartIndex]] = None,
    ) -> dict:
        return self._digestion_part(
            digestion_id=digestion_id,
            sequence=sequence,
            workflow_id=workflow_id,
            workflow_context=workflow_context,
            state=state,
            index=index,
        )

    def _digestion_part_by_model(
        self, digestion_id: UUID, data: DigestionPartCreateRequest
    ) -> dict:
        return self.digestion_part(digestion_id=digestion_id, **data.model_dump())

    @abstractmethod
    def _digestion_topic(self, **kwargs) -> dict:
        pass

    def digestion_topic(
        self,
        digestion_id: UUID,
        topic_id: UUID,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        frequency: Optional[float] = None,
        message_data_filter: Optional[dict] = None,
    ) -> dict:
        return self._digestion_topic(
            digestion_id=digestion_id,
            topic_id=topic_id,
            start_time=start_time,
            end_time=end_time,
            frequency=frequency,
            message_data_filter=message_data_filter,
        )

    def _digestion_topic_by_model(
        self, digestion_id: UUID, data: DigestionTopicCreateRequest
    ) -> dict:
        return self.digestion_topic(digestion_id=digestion_id, **data.model_dump())

    @abstractmethod
    def _group(self, **kwargs) -> dict:
        pass

    def group(
        self,
        name: str,
        default_workflow_id: Optional[UUID] = None,
    ) -> dict:
        return self._group(
            name=name,
            default_workflow_id=default_workflow_id,
        )

    def _group_by_model(self, data: GroupCreateRequest) -> dict:
        return self.group(**data.model_dump())

    @abstractmethod
    def _hook(self, **kwargs) -> dict:
        pass

    def hook(
        self,
        workflow_id: UUID,
        trigger_process: str,
        trigger_state: str,
        name: Optional[str] = None,
        note: Optional[str] = None,
        managed: Optional[bool] = False,
        disabled: Optional[bool] = False,
        uri: Optional[str] = None,
        secret: Optional[str] = None,
    ) -> dict:
        return self._hook(
            workflow_id=workflow_id,
            trigger_process=trigger_process,
            trigger_state=trigger_state,
            name=name,
            note=note,
            managed=managed,
            disabled=disabled,
            uri=uri,
            secret=secret,
        )

    def _hook_by_model(self, workflow_id: UUID, data: HookCreateRequest) -> dict:
        return self.hook(workflow_id=workflow_id, **data.model_dump())

    @abstractmethod
    def _ingestion(self, **kwargs) -> dict:
        pass

    def ingestion(
        self,
        log_id: UUID,
        name: Optional[str] = None,
        object_store_id: Optional[UUID] = None,
        object_key: Optional[str] = None,
        workflow_id: Optional[UUID] = None,
        workflow_context: Optional[dict] = None,
        state: str = "ready",
        note: Optional[str] = None,
        context: Optional[dict] = None,
    ) -> dict:
        return self._ingestion(
            log_id=log_id,
            name=name,
            object_store_id=object_store_id,
            object_key=object_key,
            workflow_id=workflow_id,
            workflow_context=workflow_context,
            state=state,
            note=note,
            context=context,
        )

    def _ingestion_by_model(self, data: IngestionCreateRequest) -> dict:
        return self.ingestion(**data.model_dump())

    @abstractmethod
    def _ingestion_part(self, **kwargs) -> dict:
        pass

    def ingestion_part(
        self,
        ingestion_id: UUID,
        sequence: int,
        source: Optional[str] = None,
        workflow_id: Optional[UUID] = None,
        workflow_context: Optional[dict] = None,
        state: str = "queued",
        index: Optional[List[IngestionPartIndex]] = None,
    ) -> dict:
        return self._ingestion_part(
            ingestion_id=ingestion_id,
            sequence=sequence,
            source=source,
            workflow_id=workflow_id,
            workflow_context=workflow_context,
            state=state,
            index=index,
        )

    def _ingestion_part_by_model(
        self, ingestion_id: UUID, data: IngestionPartCreateRequest
    ) -> dict:
        return self.ingestion_part(ingestion_id=ingestion_id, **data.model_dump())

    @abstractmethod
    def _label(self, **kwargs) -> dict:
        pass

    def label(self, value: str, note: Optional[str] = None) -> dict:
        return self._label(
            value=value,
            note=note,
        )

    def _label_by_model(self, data: LabelCreateRequest) -> dict:
        return self.label(**data.model_dump())

    @abstractmethod
    def _log(self, **kwargs) -> dict:
        pass

    def log(
        self,
        group_id: UUID,
        name: str,
        note: Optional[str] = None,
        context: Optional[dict] = None,
        time_adjustment: Optional[int] = None,
        default_workflow_id: Optional[UUID] = None,
    ) -> dict:
        return self._log(
            group_id=group_id,
            name=name,
            note=note,
            context=context,
            time_adjustment=time_adjustment,
            default_workflow_id=default_workflow_id,
        )

    def _log_by_model(self, data: LogCreateRequest) -> dict:
        return self.log(**data.model_dump())

    @abstractmethod
    def _object_store(self, **kwargs) -> dict:
        pass

    def object_store(
        self,
        bucket_name: str,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        region_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        note: Optional[str] = None,
        disabled: Optional[bool] = False,
    ) -> dict:
        return self._object_store(
            bucket_name=bucket_name,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            region_name=region_name,
            endpoint_url=endpoint_url,
            note=note,
            disabled=disabled,
        )

    def _object_store_by_model(self, data: ObjectStoreCreateRequest) -> dict:
        return self.object_store(**data.model_dump())

    @abstractmethod
    def _query(self, **kwargs) -> dict:
        pass

    def query(
        self,
        log_id: UUID,
        name: Optional[str] = None,
        note: Optional[str] = None,
        statement: Optional[str] = None,
        parameters: Optional[dict] = None,
        workflow_id: Optional[UUID] = None,
        workflow_context: Optional[dict] = None,
        state: str = "queued",
        error: Optional[dict] = None,
        context: Optional[dict] = None,
    ) -> dict:
        return self._query(
            log_id=log_id,
            name=name,
            note=note,
            statement=statement,
            parameters=parameters,
            workflow_id=workflow_id,
            workflow_context=workflow_context,
            state=state,
            error=error,
            context=context,
        )

    def _query_by_model(self, log_id: UUID, data: QueryCreateRequest) -> dict:
        return self.query(log_id=log_id, **data.model_dump())

    @abstractmethod
    def _record(self, **kwargs) -> dict:
        pass

    def record(
        self,
        timestamp: int,
        topic_id: UUID,
        data_offset: Optional[int] = None,
        data_length: Optional[int] = None,
        chunk_compression: Optional[str] = None,
        chunk_offset: Optional[int] = None,
        chunk_length: Optional[int] = None,
        workflow_id: Optional[UUID] = None,
        workflow_context: Optional[dict] = None,
        state: str = "completed",
        note: Optional[str] = None,
        source: Optional[str] = None,
        message_data: Optional[dict] = None,
        context: Optional[dict] = None,
    ) -> dict:
        return self._record(
            timestamp=timestamp,
            topic_id=topic_id,
            data_offset=data_offset,
            data_length=data_length,
            chunk_compression=chunk_compression,
            chunk_offset=chunk_offset,
            chunk_length=chunk_length,
            workflow_id=workflow_id,
            workflow_context=workflow_context,
            state=state,
            note=note,
            source=source,
            message_data=message_data,
            context=context,
        )

    def _record_by_model(self, topic_id: UUID, data: RecordCreateRequest) -> dict:
        return self.record(topic_id=topic_id, **data.model_dump())

    @abstractmethod
    def _role(self, **kwargs) -> dict:
        pass

    def role(
        self,
        name: str,
        policy: dict,
        note: Optional[str] = None,
        disabled: Optional[bool] = False,
        managed: Optional[bool] = False,
        default: Optional[bool] = False,
    ) -> dict:
        return self._role(
            name=name,
            policy=policy,
            note=note,
            disabled=disabled,
            managed=managed,
            default=default,
        )

    def _role_by_model(self, data: RoleCreateRequest) -> dict:
        return self.role(**data.model_dump())

    @abstractmethod
    def _tag(self, **kwargs) -> dict:
        pass

    def tag(
        self,
        label_id: UUID,
        log_id: UUID,
        topic_id: Optional[UUID] = None,
        note: Optional[str] = None,
        context: Optional[dict] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> dict:
        return self._tag(
            label_id=label_id,
            log_id=log_id,
            topic_id=topic_id,
            note=note,
            context=context,
            start_time=start_time,
            end_time=end_time,
        )

    def _tag_by_model(self, log_id: UUID, data: TagCreateRequest) -> dict:
        return self.tag(log_id=log_id, **data.model_dump())

    @abstractmethod
    def _topic(self, **kwargs) -> dict:
        pass

    def topic(
        self,
        log_id: UUID,
        name: str,
        associated_topic_id: Optional[UUID] = None,
        latched: Optional[bool] = False,
        context: Optional[dict] = None,
        type_name: Optional[str] = None,
        type_encoding: Optional[str] = None,
        type_data: Optional[dict] = None,
        type_schema: Optional[str] = None,
    ) -> dict:
        return self._topic(
            name=name,
            log_id=log_id,
            associated_topic_id=associated_topic_id,
            latched=latched,
            context=context,
            type_name=type_name,
            type_encoding=type_encoding,
            type_data=type_data,
            type_schema=type_schema,
        )

    def _topic_by_model(self, data: TopicCreateRequest) -> dict:
        return self.topic(**data.model_dump())

    @abstractmethod
    def _user(self, **kwargs) -> dict:
        pass

    def user(
        self,
        username: str,
        role_id: Optional[UUID] = None,
        admin: Optional[bool] = False,
        disabled: Optional[bool] = False,
        managed: Optional[bool] = False,
        password: Optional[str] = None,
    ) -> dict:
        return self._user(
            username=username,
            role_id=role_id,
            admin=admin,
            disabled=disabled,
            managed=managed,
            password=password,
        )

    def _user_by_model(self, data: UserCreateRequest) -> dict:
        return self.user(**data.model_dump())

    @abstractmethod
    def _workflow(self, **kwargs) -> dict:
        pass

    def workflow(
        self,
        name: str,
        note: Optional[str] = None,
        default: Optional[bool] = False,
        disabled: Optional[bool] = False,
        managed: Optional[bool] = False,
        context_schema: Optional[dict] = None,
    ) -> dict:
        return self._workflow(
            name=name,
            note=note,
            default=default,
            disabled=disabled,
            managed=managed,
            context_schema=context_schema,
        )

    def _workflow_by_model(self, data: WorkflowCreateRequest) -> dict:
        return self.workflow(**data.model_dump())

    # Objects

    @abstractmethod
    def _object(self, **kwargs) -> dict:
        pass

    def object(
        self,
        log_id: UUID,
        key: str,
        content_type: Optional[str] = None,
    ) -> dict:
        return self._object(
            log_id=log_id,
            key=key,
            content_type=content_type,
        )

    def _object_by_model(self, log_id: UUID, data: ObjectCreateRequest) -> dict:
        return self.object(log_id=log_id, **data.model_dump())

    @abstractmethod
    def _object_part(self, **kwargs) -> dict:
        pass

    def object_part(
        self,
        log_id: UUID,
        object_key: str,
        size: int,
        part_number: Optional[int] = None,
    ) -> dict:
        return self._object_part(
            log_id=log_id,
            object_key=object_key,
            part_number=part_number,
            size=size,
        )

    def _object_part_by_model(
        self, log_id: UUID, object_key: str, data: ObjectPartCreateRequest
    ) -> dict:
        return self.object_part(
            log_id=log_id, object_key=object_key, **data.model_dump()
        )
