from uuid import UUID

from src.common.types import RowId, RowIdentityKey
from src.core.validators import BaseValidator


def test_check_existence_id_int(base_validator: BaseValidator) -> None:
    ids_int_one = [1, 2, 3, 4]
    ids_int_two = [1, 2, 3, 99]

    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(
        ids_int_one, ids_int_one
    )
    assert len(missing_ids) == 0

    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(
        ids_int_one, ids_int_two
    )
    assert len(missing_ids) == len(set(ids_int_one) - set(ids_int_two))


def test_check_existence_id_uuid(base_validator: BaseValidator) -> None:
    ids_uuid_one = [
        UUID("019f5bde-6af2-7383-bd1b-dd5954d4e3aa"),
        UUID("019f5bdf-2240-7424-87a9-c42508929ae8"),
        UUID("019f5bdf-4768-7956-9dad-cd7c3c2c3d51"),
    ]
    ids_uuid_two = [
        UUID("019f5bde-6af2-7383-bd1b-dd5954d4e3aa"),
        UUID("019f5bdf-2240-7424-87a9-c42508929ae8"),
        UUID("019f5be0-4d7f-7677-bc9e-ec3d9c733189"),
    ]

    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(
        ids_uuid_one, ids_uuid_one
    )
    assert len(missing_ids) == 0

    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(
        ids_uuid_one, ids_uuid_two
    )
    assert len(missing_ids) == len(set(ids_uuid_one) - set(ids_uuid_two))


def test_check_existence_identity_keys(
    base_validator: BaseValidator,
) -> None:
    identity_keys_one = [("A", "B"), ("C", "D")]
    identity_keys_two = [("E", "F"), ("G", "H")]

    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(
        identity_keys_one, identity_keys_one
    )
    assert len(missing_ids) == 0

    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(
        identity_keys_one, identity_keys_two
    )
    assert len(missing_ids) == len(set(identity_keys_one) - set(identity_keys_two))
