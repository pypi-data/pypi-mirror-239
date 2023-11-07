from typing import Optional
from datetime import datetime
from uuid import UUID
from abc import ABC, abstractmethod


class ListInterface(ABC):
    @abstractmethod
    def _api_key(self, **kwargs) -> dict:
        pass

    def api_key(
        self,
        name: Optional[str] = None,
        name_like: Optional[str] = None,
        user_id: Optional[UUID] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
        order: Optional[str] = "created_at",
        sort: Optional[str] = "ASC",
        created_by: Optional[UUID] = None,
        updated_by: Optional[UUID] = None,
        deleted_by: Optional[UUID] = None,
        updated_by_null: Optional[bool] = None,
        deleted_by_null: Optional[bool] = None,
        updated_at_null: Optional[bool] = None,
        deleted_at_null: Optional[bool] = None,
        created_at_lte: Optional[datetime] = None,
        updated_at_lte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
        created_at_gte: Optional[datetime] = None,
        updated_at_gte: Optional[datetime] = None,
        deleted_at_gte: Optional[datetime] = None,
    ) -> dict:
        return self._api_key(
            name=name,
            name_like=name_like,
            user_id=user_id,
            offset=offset,
            limit=limit,
            order=order,
            sort=sort,
            created_by=created_by,
            updated_by=updated_by,
            deleted_by=deleted_by,
            updated_by_null=updated_by_null,
            deleted_by_null=deleted_by_null,
            updated_at_null=updated_at_null,
            deleted_at_null=deleted_at_null,
            created_at_lte=created_at_lte,
            updated_at_lte=updated_at_lte,
            deleted_at_lte=deleted_at_lte,
            created_at_gte=created_at_gte,
            updated_at_gte=updated_at_gte,
            deleted_at_gte=deleted_at_gte,
        )

    def api_keys(self, **kwargs) -> dict:
        return self.api_key(**kwargs)

    @abstractmethod
    def _datastore(self, **kwargs) -> dict:
        pass

    def datastore(
        self,
        offset: Optional[int] = 0,
        limit: Optional[int] = 10,
        order: Optional[str] = "created_at",
        sort: Optional[str] = "ASC",
        name: Optional[str] = None,
        name_like: Optional[str] = None,
        created_by: Optional[UUID] = None,
        updated_by: Optional[UUID] = None,
        deleted_by: Optional[UUID] = None,
        updated_by_null: Optional[bool] = None,
        deleted_by_null: Optional[bool] = None,
        updated_at_null: Optional[bool] = None,
        deleted_at_null: Optional[bool] = None,
        created_at_lte: Optional[datetime] = None,
        updated_at_lte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
        created_at_gte: Optional[datetime] = None,
        updated_at_gte: Optional[datetime] = None,
        deleted_at_gte: Optional[datetime] = None,
    ) -> dict:
        return self._datastore(
            offset=offset,
            limit=limit,
            order=order,
            sort=sort,
            name=name,
            name_like=name_like,
            created_by=created_by,
            updated_by=updated_by,
            deleted_by=deleted_by,
            updated_by_null=updated_by_null,
            deleted_by_null=deleted_by_null,
            updated_at_null=updated_at_null,
            deleted_at_null=deleted_at_null,
            created_at_lte=created_at_lte,
            updated_at_lte=updated_at_lte,
            deleted_at_lte=deleted_at_lte,
            created_at_gte=created_at_gte,
            updated_at_gte=updated_at_gte,
            deleted_at_gte=deleted_at_gte,
        )

    def datastores(self, **kwargs) -> dict:
        return self.datastore(**kwargs)

    @abstractmethod
    def _datastore_association(self, **kwargs) -> dict:
        pass

    def datastore_association(
        self,
        offset: Optional[int] = 0,
        limit: Optional[int] = 10,
        order: Optional[str] = "created_at",
        sort: Optional[str] = "ASC",
        user_id: Optional[UUID] = None,
        datastore_id: Optional[UUID] = None,
        datastore_user_id: Optional[UUID] = None,
        created_by: Optional[UUID] = None,
        updated_by: Optional[UUID] = None,
        deleted_by: Optional[UUID] = None,
        updated_by_null: Optional[bool] = None,
        deleted_by_null: Optional[bool] = None,
        updated_at_null: Optional[bool] = None,
        deleted_at_null: Optional[bool] = None,
        created_at_lte: Optional[datetime] = None,
        updated_at_lte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
        created_at_gte: Optional[datetime] = None,
        updated_at_gte: Optional[datetime] = None,
        deleted_at_gte: Optional[datetime] = None,
    ) -> dict:
        return self._datastore_association(
            user_id=user_id,
            datastore_id=datastore_id,
            datastore_user_id=datastore_user_id,
            offset=offset,
            limit=limit,
            order=order,
            sort=sort,
            created_by=created_by,
            updated_by=updated_by,
            deleted_by=deleted_by,
            updated_by_null=updated_by_null,
            deleted_by_null=deleted_by_null,
            updated_at_null=updated_at_null,
            deleted_at_null=deleted_at_null,
            created_at_lte=created_at_lte,
            updated_at_lte=updated_at_lte,
            deleted_at_lte=deleted_at_lte,
            created_at_gte=created_at_gte,
            updated_at_gte=updated_at_gte,
            deleted_at_gte=deleted_at_gte,
        )

    def datastore_associations(self, **kwargs) -> dict:
        return self.datastore_association(**kwargs)

    @abstractmethod
    def _role(self, **kwargs) -> dict:
        pass

    def role(
        self,
        name: Optional[str] = None,
        name_like: Optional[str] = None,
        disabled: Optional[bool] = None,
        default: Optional[bool] = None,
        managed: Optional[bool] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
        order: Optional[str] = "timestamp",
        sort: Optional[str] = "ASC",
        created_by: Optional[UUID] = None,
        updated_by: Optional[UUID] = None,
        deleted_by: Optional[UUID] = None,
        updated_by_null: Optional[bool] = None,
        deleted_by_null: Optional[bool] = None,
        updated_at_null: Optional[bool] = None,
        deleted_at_null: Optional[bool] = None,
        created_at_lte: Optional[datetime] = None,
        updated_at_lte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
        created_at_gte: Optional[datetime] = None,
        updated_at_gte: Optional[datetime] = None,
        deleted_at_gte: Optional[datetime] = None,
    ) -> dict:
        return self._role(
            name=name,
            name_like=name_like,
            disabled=disabled,
            default=default,
            managed=managed,
            offset=offset,
            limit=limit,
            order=order,
            sort=sort,
            created_by=created_by,
            updated_by=updated_by,
            deleted_by=deleted_by,
            updated_by_null=updated_by_null,
            deleted_by_null=deleted_by_null,
            updated_at_null=updated_at_null,
            deleted_at_null=deleted_at_null,
            created_at_lte=created_at_lte,
            updated_at_lte=updated_at_lte,
            deleted_at_lte=deleted_at_lte,
            created_at_gte=created_at_gte,
            updated_at_gte=updated_at_gte,
            deleted_at_gte=deleted_at_gte,
        )

    def roles(self, **kwargs) -> dict:
        return self.role(**kwargs)

    @abstractmethod
    def _user(self, **kwargs) -> dict:
        pass

    def user(
        self,
        username: Optional[str] = None,
        username_like: Optional[str] = None,
        role_id: Optional[UUID] = None,
        external_id: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
        order: Optional[str] = "created_at",
        sort: Optional[str] = "ASC",
        created_by: Optional[UUID] = None,
        updated_by: Optional[UUID] = None,
        deleted_by: Optional[UUID] = None,
        updated_by_null: Optional[bool] = None,
        deleted_by_null: Optional[bool] = None,
        updated_at_null: Optional[bool] = None,
        deleted_at_null: Optional[bool] = None,
        created_at_lte: Optional[datetime] = None,
        updated_at_lte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
        created_at_gte: Optional[datetime] = None,
        updated_at_gte: Optional[datetime] = None,
        deleted_at_gte: Optional[datetime] = None,
    ) -> dict:
        return self._user(
            username=username,
            username_like=username_like,
            role_id=role_id,
            external_id=external_id,
            offset=offset,
            limit=limit,
            order=order,
            sort=sort,
            created_by=created_by,
            updated_by=updated_by,
            deleted_by=deleted_by,
            updated_by_null=updated_by_null,
            deleted_by_null=deleted_by_null,
            updated_at_null=updated_at_null,
            deleted_at_null=deleted_at_null,
            created_at_lte=created_at_lte,
            updated_at_lte=updated_at_lte,
            deleted_at_lte=deleted_at_lte,
            created_at_gte=created_at_gte,
            updated_at_gte=updated_at_gte,
            deleted_at_gte=deleted_at_gte,
        )

    def users(self, **kwargs) -> dict:
        return self.user(**kwargs)
