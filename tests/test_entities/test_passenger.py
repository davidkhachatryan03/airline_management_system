import pytest
from src.entities import PassengerCreated

def test_valid_passenger(valid_passenger: dict) -> None:
    passenger_created = PassengerCreated(**valid_passenger)

    assert passenger_created.full_name == valid_passenger["full_name"]
    assert passenger_created.email == valid_passenger["email"]
    assert passenger_created.phone_number == valid_passenger["phone_number"]
    assert passenger_created.is_blacklisted == valid_passenger["is_blacklisted"]
    assert passenger_created.is_vip == valid_passenger["is_vip"]

@pytest.mark.parametrize("field, value, expected_exception", [
    ("full_name", True, TypeError),
    ("full_name", "   ", ValueError),
    ("full_name", "", ValueError),
    ("full_name", "abcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyz", ValueError),      
    ("email", True, TypeError),
    ("email", "   ", ValueError),
    ("email", "", ValueError),
    ("email", "abcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyz", ValueError),                 
    ("phone_number", True, TypeError),
    ("phone_number", 0, ValueError),
    ("phone_number", -100, ValueError),             
    ("is_blacklisted", 123, TypeError),   
    ("is_vip", 123, TypeError),               
])

def test_invalid_passenger(valid_passenger: dict, field: str, value, expected_exception) -> None:
    test_data = valid_passenger.copy()
    test_data[field] = value

    with pytest.raises(expected_exception):
        PassengerCreated(**test_data)