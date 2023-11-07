from abc import ABC, abstractmethod
from uuid import UUID

from lqs.interface.dsm.models import (
    APIKeyUpdateRequest,
    DataStoreUpdateRequest,
    DataStoreAssociationUpdateRequest,
    RoleUpdateRequest,
    UserUpdateRequest,
)


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
    def _datastore(self, **kwargs) -> dict:
        pass

    def datastore(self, datastore_id: UUID, data: dict):
        return self._datastore(
            datastore_id=datastore_id,
            data=self._process_data(data),
        )

    def _datastore_by_model(self, datastore_id: UUID, data: DataStoreUpdateRequest):
        return self._datastore(
            datastore_id=datastore_id,
            data=data.model_dump(exclude_unset=True),
        )

    @abstractmethod
    def _datastore_association(self, **kwargs) -> dict:
        pass

    def datastore_association(self, datastore_association_id: UUID, data: dict):
        return self._datastore_association(
            datastore_association_id=datastore_association_id,
            data=self._process_data(data),
        )

    def _datastore_association_by_model(
        self, datastore_association_id: UUID, data: DataStoreAssociationUpdateRequest
    ):
        return self._datastore_association(
            datastore_association_id=datastore_association_id,
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
    def _user(self, **kwargs) -> dict:
        pass

    def user(self, user_id: UUID, data: dict) -> dict:
        return self._user(user_id=user_id, data=self._process_data(data))

    def _user_by_model(self, user_id: UUID, data: UserUpdateRequest) -> dict:
        return self._user(
            user_id=user_id,
            data=data.model_dump(exclude_unset=True),
        )
