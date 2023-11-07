from typing import List, Optional

from pydantic import BaseModel

from lqs.interface.dsm.models.__common__ import (
    CommonModel,
    PaginationModel,
    optional_field,
)


class Role(CommonModel):
    name: str
    policy: dict
    note: Optional[str]

    disabled: bool
    default: bool
    managed: bool


class RoleDataResponse(BaseModel):
    data: Role


class RoleListResponse(PaginationModel):
    data: List[Role]


class RoleCreateRequest(BaseModel):
    name: str
    policy: dict

    note: Optional[str] = None
    disabled: bool = False
    default: bool = False


class RoleUpdateRequest(BaseModel):
    name: str = optional_field
    policy: dict = optional_field
    note: Optional[str] = optional_field
    disabled: bool = optional_field
    default: bool = optional_field
