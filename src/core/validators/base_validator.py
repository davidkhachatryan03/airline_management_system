from collections.abc import Sequence
from typing import Sequence, TypeVar

T = TypeVar("T")


class BaseValidator:

    def check_existence(self, list_one: Sequence[T], list_two: Sequence[T]) -> set[T]:
        missing_ids = set(list_one) - set(list_two)

        return missing_ids
