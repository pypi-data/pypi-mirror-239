from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from lqs.interface.dsm.models import (
    APIKeyCreateRequest,
    DataStoreCreateRequest,
    DataStoreAssociationCreateRequest,
    RoleCreateRequest,
    UserCreateRequest,
)


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
    def _datastore(self, **kwargs) -> dict:
        pass

    def datastore(self, name: str) -> dict:
        return self._datastore(
            name=name,
        )

    def _datastore_by_model(self, data: DataStoreCreateRequest) -> dict:
        return self.datastore(**data.model_dump())

    @abstractmethod
    def _datastore_association(self, **kwargs) -> dict:
        pass

    def datastore_association(
        self,
        user_id: UUID,
        datastore_id: UUID,
        owner: bool = False,
        datastore_user_id: Optional[UUID] = None,
        datastore_username: Optional[str] = None,
        datastore_role_id: Optional[UUID] = None,
        datastore_admin: bool = False,
        datastore_disabled: bool = False,
    ) -> dict:
        return self._datastore_association(
            user_id=user_id,
            datastore_id=datastore_id,
            datastore_user_id=datastore_user_id,
            owner=owner,
            datastore_username=datastore_username,
            datastore_role_id=datastore_role_id,
            datastore_admin=datastore_admin,
            datastore_disabled=datastore_disabled,
        )

    def _datastore_association_by_model(
        self, data: DataStoreAssociationCreateRequest
    ) -> dict:
        return self.datastore_association(**data.model_dump())

    @abstractmethod
    def _role(self, **kwargs) -> dict:
        pass

    def role(
        self,
        name: str,
        policy: dict,
        note: Optional[str] = None,
        disabled: Optional[bool] = False,
        default: Optional[bool] = False,
    ) -> dict:
        return self._role(
            name=name,
            policy=policy,
            note=note,
            disabled=disabled,
            default=default,
        )

    def _role_by_model(self, data: RoleCreateRequest) -> dict:
        return self.role(**data.model_dump())

    @abstractmethod
    def _user(self, **kwargs) -> dict:
        pass

    def user(
        self,
        username: str,
        role_id: Optional[UUID] = None,
        admin: Optional[bool] = False,
        disabled: Optional[bool] = False,
        external_id: Optional[str] = None,
        password: Optional[str] = None,
    ) -> dict:
        return self._user(
            username=username,
            role_id=role_id,
            admin=admin,
            disabled=disabled,
            external_id=external_id,
            password=password,
        )

    def _user_by_model(self, data: UserCreateRequest) -> dict:
        return self.user(**data.model_dump())
