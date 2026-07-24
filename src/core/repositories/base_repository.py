from typing import Any, Generic, Sequence, TypeVar
from uuid import UUID

from src.common import DBManager

T = TypeVar("T")


class BaseRepository(Generic[T]):

    def __init__(
        self,
        db_manager: DBManager,
        table_name: str,
        columns: tuple[str, ...],
        entity: type[T],
        identity_key: tuple[str, ...] = (),
    ) -> None:
        self.db_manager = db_manager
        self.table_name = table_name
        self.columns = ",".join(columns)
        self.identity_key = ",".join(identity_key)
        self.entity = entity

    def insert(self, rows: list[T]) -> None:
        self.db_manager.insert_rows(self.table_name, rows)

    def retrieve(self, limit=5) -> list[T]:
        query = "SELECT {} FROM {} LIMIT %s".format(self.columns, self.table_name)

        results: list[tuple[Any, ...]] = self.db_manager.retrieve_many_columns(
            query, (limit,)
        )

        return [self.entity(*result) for result in results]

    def retrieve_by_ids(self, ids: Sequence[UUID] | Sequence[int]) -> list[T]:
        if not ids:
            return []

        placeholders = ",".join(["%s"] * len(ids))

        query = "SELECT {} FROM {} WHERE id IN ({})".format(
            self.columns, self.table_name, placeholders
        )

        results: list[tuple[Any, ...]] = self.db_manager.retrieve_many_columns(
            query, ids
        )

        return [self.entity(*result) for result in results]

    def retrieve_by_identity_keys(
        self, identity_keys: Sequence[tuple[Any, ...]]
    ) -> list[T]:
        if not identity_keys:
            return []

        placeholders = ",".join(
            ["(" + ",".join(["%s"] * len(identity_keys[0])) + ")"] * len(identity_keys)
        )

        query = "SELECT {} FROM {} WHERE ({}) IN ({})".format(
            self.columns, self.table_name, self.identity_key, placeholders
        )

        identity_keys_plain = [
            value for identity_key in identity_keys for value in identity_key
        ]

        results: list[tuple[Any, ...]] = self.db_manager.retrieve_many_columns(
            query, identity_keys_plain
        )

        return [self.entity(*result) for result in results]
