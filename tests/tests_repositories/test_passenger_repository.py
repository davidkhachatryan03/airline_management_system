from src.core.repositories import PassengerRepository
from src.entities import Passenger


def test_insert_passenger(
    passenger_repository: PassengerRepository, passenger: Passenger
) -> None:
    passenger_repository.insert_passengers([passenger])

    last_inserted_passenger: Passenger = passenger_repository.retrieve_passengers(
        limit=1
    )[0]

    assert last_inserted_passenger.id == passenger.id
    assert last_inserted_passenger.full_name == passenger.full_name
    assert last_inserted_passenger.birth_date == passenger.birth_date
    assert last_inserted_passenger.email == passenger.email
    assert last_inserted_passenger.phone_number == passenger.phone_number
    assert last_inserted_passenger.is_blacklisted == passenger.is_blacklisted
    assert last_inserted_passenger.is_vip == passenger.is_vip


def test_retrieve_all_bookings(
    passenger_repository: PassengerRepository, passengers: list[Passenger]
) -> None:
    passenger_repository.insert_passengers(passengers)

    all_inserted_passengers: list[Passenger] = passenger_repository.retrieve_passengers(
        limit=3
    )

    assert len(all_inserted_passengers) == len(passengers)
