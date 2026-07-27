from typing import Any, Generic, TypeVar
from uuid import UUID

from src.entities import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class FakeBaseRepository(Generic[T]):

    def __init__(self, identity_key: tuple[str, ...] = ()) -> None:
        self.identity_key = identity_key
        self.storage: dict[UUID | int, T] = {}

    def insert(self, entities: list[T]) -> None:
        for entity in entities:
            self.storage[entity.id] = entity

    def retrieve_by_ids(self, ids: list[UUID] | list[int]) -> list[T]:
        return [self.storage[id] for id in ids if id in self.storage]

    def retrieve_by_identity_keys(
        self, identity_keys: list[tuple[Any, ...]]
    ) -> list[T]:
        storage_by_identity_key: dict[tuple[str, ...], T] = {
            entity.identity_key: entity for entity in self.storage.values()
        }

        return [
            storage_by_identity_key[identity_key]
            for identity_key in identity_keys
            if identity_key in storage_by_identity_key
        ]
