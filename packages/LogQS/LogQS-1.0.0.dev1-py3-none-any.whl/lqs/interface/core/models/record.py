from typing import List, Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from lqs.interface.core.models.__common__ import (
    PaginationModel,
    ProcessState,
    optional_field,
)


class Record(BaseModel):
    timestamp: int
    topic_id: UUID
    log_id: UUID
    ingestion_id: Optional[UUID]

    data_offset: Optional[int]
    data_length: Optional[int]
    chunk_compression: Optional[str]
    chunk_offset: Optional[int]
    chunk_length: Optional[int]

    workflow_id: Optional[UUID]
    workflow_context: Optional[dict]
    state: ProcessState
    error: Optional[dict]

    note: Optional[str]
    source: Optional[str]
    message_data: Optional[dict]
    context: Optional[dict]

    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    deleted_by: Optional[UUID]


class RecordDataResponse(BaseModel):
    data: Record


class RecordListResponse(PaginationModel):
    data: List[Record]


class RecordCreateRequest(BaseModel):
    timestamp: int
    data_offset: Optional[int] = None
    data_length: Optional[int] = None
    chunk_compression: Optional[str] = None
    chunk_offset: Optional[int] = None
    chunk_length: Optional[int] = None
    note: Optional[str] = None
    workflow_id: Optional[UUID] = None
    workflow_context: Optional[dict] = None
    state: ProcessState = ProcessState.ready
    source: Optional[str] = None
    message_data: Optional[dict] = None
    context: Optional[dict] = None


class RecordUpdateRequest(BaseModel):
    workflow_id: Optional[UUID] = optional_field
    workflow_context: Optional[dict] = optional_field
    state: ProcessState = optional_field
    error: Optional[dict] = optional_field
    context: Optional[dict] = optional_field


# Record Objects


class RecordObject(BaseModel):
    timestamp: int
    presigned_url: Optional[str] = None


class RecordObjectDataResponse(BaseModel):
    data: RecordObject


class RecordObjectListResponse(PaginationModel):
    data: List[RecordObject]
