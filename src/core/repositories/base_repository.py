from typing import Any, Generic, Sequence, TypeVar
from uuid import RFC_4122, UUID

from src.common import DBManager
from src.entities import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):

    def __init__(
        self,
        db_manager: DBManager,
        table_name: str,
        columns: tuple[str, ...],
        entity: type[T],
        identity_key: tuple[str, ...] = (),
        uuid_columns: tuple[str, ...] = (),
    ) -> None:
        self.db_manager = db_manager
        self.table_name = table_name
        self.columns = ",".join(columns)
        self.identity_key = ",".join(identity_key)
        self.entity = entity
        self.uuid_columns = uuid_columns

    def _to_db_value(self, value: Any) -> Any:
        if isinstance(value, UUID):
            return value.bytes

        return value

    def _from_db_value(self, value: Any) -> Any:
        if isinstance(value, bytes):

            if len(value) == 16:

                candidate = UUID(bytes=value)

                is_rfc_standard = candidate.variant == RFC_4122

                is_valid_version = candidate.version == 7

                if is_rfc_standard and is_valid_version:
                    return candidate

        return value

    def _map_row_to_entity(self, row: tuple[Any, ...]) -> T:
        parsed_row = tuple(self._from_db_value(val) for val in row)
        return self.entity(*parsed_row)

    def insert(self, rows: list[T]) -> None:
        if not rows:
            return

        row_dicts = [row.to_dict() for row in rows]
        columns = list(row_dicts[0].keys())

        cols_str = "(" + ",".join(columns) + ")"
        placeholders = "(" + ",".join(["%s"] * len(columns)) + ")"
        query = f"INSERT INTO {self.table_name} {cols_str} VALUES {placeholders}"

        values_to_insert = []
        for d in row_dicts:
            values_to_insert.append(tuple(self._to_db_value(d[col]) for col in columns))

        self.db_manager.execute_write_many(query, values_to_insert)

    def retrieve(self, limit=5) -> list[T]:
        query = f"SELECT {self.columns} FROM {self.table_name} LIMIT %s"

        raw_results = self.db_manager.execute_read(query, (limit,))
        return [self._map_row_to_entity(row) for row in raw_results]

    def delete(self) -> None:
        query = f"DELETE FROM {self.table_name}"
        self.db_manager.execute_write(query)

    def retrieve_by_ids(self, ids: Sequence[UUID] | Sequence[int]) -> list[T]:
        if not ids:
            return []

        placeholders = ",".join(["%s"] * len(ids))
        query = (
            f"SELECT {self.columns} FROM {self.table_name} WHERE id IN ({placeholders})"
        )

        formatted_ids = tuple(self._to_db_value(i) for i in ids)

        raw_results = self.db_manager.execute_read(query, formatted_ids)
        return [self._map_row_to_entity(row) for row in raw_results]

    def retrieve_by_identity_keys(
        self, identity_keys: Sequence[tuple[Any, ...]]
    ) -> list[T]:
        if not identity_keys:
            return []

        placeholders = ",".join(
            ["(" + ",".join(["%s"] * len(identity_keys[0])) + ")"] * len(identity_keys)
        )
        query = f"SELECT {self.columns} FROM {self.table_name} WHERE ({self.identity_key}) IN ({placeholders})"

        formatted_keys = tuple(
            self._to_db_value(value)
            for key_tuple in identity_keys
            for value in key_tuple
        )

        raw_results = self.db_manager.execute_read(query, formatted_keys)
        return [self._map_row_to_entity(row) for row in raw_results]
