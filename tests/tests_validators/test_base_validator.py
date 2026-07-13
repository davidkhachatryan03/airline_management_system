from src.common.types import CurrentStatusId, RowId, RowIdentityKey
from src.core.validators import BaseValidator

def test_check_existence_id_int(base_validator: BaseValidator, ids_int_one: list[RowId], ids_int_two: list[RowId]) -> None:
    assert base_validator.check_existence(ids_int_one, ids_int_one)
    assert not base_validator.check_existence(ids_int_one, ids_int_two)

def test_check_existence_id_uuid(base_validator: BaseValidator, ids_uuid_one: list[RowId], ids_uuid_two: list[RowId]) -> None:
    assert base_validator.check_existence(ids_uuid_one, ids_uuid_one)
    assert not base_validator.check_existence(ids_uuid_one, ids_uuid_two)

def test_check_existence_identity_keys(base_validator: BaseValidator, identity_keys_one: list[RowIdentityKey], identity_keys_two: list[RowIdentityKey]) -> None:
    assert base_validator.check_existence(identity_keys_one, identity_keys_one)
    assert not base_validator.check_existence(identity_keys_one, identity_keys_two)

def test_check_statuses(base_validator: BaseValidator, statuses_all_True: list[CurrentStatusId], statuses_mixed: list[CurrentStatusId]) -> None:
    assert base_validator.check_statuses(statuses_all_True)
    assert not base_validator.check_statuses(statuses_mixed)