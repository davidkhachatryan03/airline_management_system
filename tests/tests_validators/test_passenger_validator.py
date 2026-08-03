from factory.declarations import Iterator

from src.core.validators import PassengerValidator
from tests.factories import PassengerFactory


def test_passenger_validator_is_blacklisted() -> None:
    passenger_validator = PassengerValidator()

    passengers = PassengerFactory.build_batch(
        4, is_blacklisted=Iterator([True, True, False, False])
    )

    assert passenger_validator.is_blacklisted(passengers) == [
        passengers[0].id,
        passengers[1].id,
    ]
