from abc import ABC, abstractmethod
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
    def _datastore(self, **kwargs) -> dict:
        pass

    def datastore(self, datastore_id: UUID) -> dict:
        return self._datastore(
            datastore_id=datastore_id,
        )

    @abstractmethod
    def _datastore_association(self, **kwargs) -> dict:
        pass

    def datastore_association(self, datastore_association_id: UUID) -> dict:
        return self._datastore_association(
            datastore_association_id=datastore_association_id,
        )

    @abstractmethod
    def _role(self, **kwargs) -> dict:
        pass

    def role(self, role_id: UUID) -> dict:
        return self._role(
            role_id=role_id,
        )

    @abstractmethod
    def _user(self, **kwargs) -> dict:
        pass

    def user(self, user_id: UUID) -> dict:
        return self._user(
            user_id=user_id,
        )
