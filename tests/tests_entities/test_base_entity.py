from decimal import Decimal

from tests.factories import BookingFactory, FlightFactory, PassengerFactory


def test_to_dict_extracts_properties_and_ignores_internal_state():
    passenger = PassengerFactory(full_name="John Doe")

    passenger._internal_db_state = "hidden"

    result = passenger.to_dict()

    assert "id" in result
    assert "full_name" in result
    assert result["id"] == passenger.id
    assert result["full_name"] == "John Doe"

    assert "_internal_db_state" not in result
    assert "_id" not in result


def test_to_dict_ignores_methods():
    booking = BookingFactory()

    booking.calculate_tax = lambda: booking.paid_amount_usd * Decimal("0.21")

    result = booking.to_dict()

    assert "calculate_tax" not in result
    assert "booking_reference" in result


def test_to_dict_handles_nested_entity():
    flight = FlightFactory(base_price_usd=Decimal("150.00"))
    booking = BookingFactory()

    booking.flight = flight

    result = booking.to_dict()

    assert isinstance(result["flight"], dict)
    assert result["flight"]["base_price_usd"] == Decimal("150.00")
    assert result["flight"]["id"] == flight.id


def test_to_dict_handles_list_of_nested_entities():
    flight_1 = FlightFactory()
    flight_2 = FlightFactory()

    booking = BookingFactory()
    booking.flights_list = [flight_1, flight_2]

    result = booking.to_dict()

    assert isinstance(result["flights_list"], list)
    assert len(result["flights_list"]) == 2
    assert result["flights_list"][0]["id"] == flight_1.id
    assert result["flights_list"][1]["id"] == flight_2.id


def test_to_dict_handles_empty_lists():
    booking = BookingFactory()
    booking.flights_list = []

    result = booking.to_dict()

    assert "flights_list" in result
    assert result["flights_list"] == []
    assert isinstance(result["flights_list"], list)
