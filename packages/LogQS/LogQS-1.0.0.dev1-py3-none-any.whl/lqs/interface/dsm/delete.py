from abc import ABC, abstractmethod
from uuid import UUID


class DeleteInterface(ABC):
    @abstractmethod
    def _api_key(self, **kwargs):
        pass

    def api_key(self, api_key_id: UUID):
        return self._api_key(
            api_key_id=api_key_id,
        )

    @abstractmethod
    def _datastore(self, **kwargs):
        pass

    def datastore(self, datastore_id: UUID):
        return self._datastore(
            datastore_id=datastore_id,
        )

    @abstractmethod
    def _datastore_association(self, **kwargs):
        pass

    def datastore_association(self, datastore_association_id: UUID):
        return self._datastore_association(
            datastore_association_id=datastore_association_id,
        )

    @abstractmethod
    def _role(self, **kwargs):
        pass

    def role(self, role_id: UUID):
        return self._role(
            role_id=role_id,
        )

    @abstractmethod
    def _user(self, **kwargs):
        pass

    def user(self, user_id: UUID):
        return self._user(
            user_id=user_id,
        )
