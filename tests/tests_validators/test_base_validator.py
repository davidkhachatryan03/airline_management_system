from src.common.types import RowId, RowIdentityKey
from src.core.validators import BaseValidator


def test_check_existence_id_int(base_validator: BaseValidator, ids_int_one: list[RowId], ids_int_two: list[RowId]) -> None:
    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(ids_int_one, ids_int_one)
    assert len(missing_ids) == 0

    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(ids_int_one, ids_int_two)
    assert len(missing_ids) == len(set(ids_int_one) - set(ids_int_two))

def test_check_existence_id_uuid(base_validator: BaseValidator, ids_uuid_one: list[RowId], ids_uuid_two: list[RowId]) -> None:
    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(ids_uuid_one, ids_uuid_one)
    assert len(missing_ids) == 0

    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(ids_uuid_one, ids_uuid_two)
    assert len(missing_ids) == len(set(ids_uuid_one) - set(ids_uuid_two))

def test_check_existence_identity_keys(base_validator: BaseValidator, identity_keys_one: list[RowIdentityKey], identity_keys_two: list[RowIdentityKey]) -> None:
    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(identity_keys_one, identity_keys_one)
    assert len(missing_ids) == 0

    missing_ids: set[RowId] | set[RowIdentityKey] = base_validator.check_existence(identity_keys_one, identity_keys_two)
    assert len(missing_ids) == len(set(identity_keys_one) - set(identity_keys_two))