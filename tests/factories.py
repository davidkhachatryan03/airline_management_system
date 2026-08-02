import random
from decimal import Decimal

from factory.base import Factory
from factory.declarations import LazyFunction, Sequence
from factory.faker import Faker
from uuid6 import uuid7

from src.entities import (
    Airplane,
    BoardingPass,
    Booking,
    Document,
    Flight,
    Passenger,
    Route,
    Ticket,
)


class AirplaneFactory(Factory):
    class Meta:
        model = Airplane

    id = Sequence(lambda n: n + 1)
    tail_number = Faker("bothify", text="LV-####")
    manufacturer = "Boeing"
    model = "737-800"
    capacity = 150
    range_km = 4500
    flight_hour_cost_usd = Decimal("1200.00")
    current_status_id = 1


class PassengerFactory(Factory):
    class Meta:
        model = Passenger

    id = LazyFunction(uuid7)
    full_name = Faker("name")
    birth_date = Faker("date_of_birth", minimum_age=18)
    email = Faker("email")
    phone_number = Faker("numerify", text="54911########")
    is_blacklisted = False
    is_vip = False


class DocumentFactory(Factory):
    class Meta:
        model = Document

    id = LazyFunction(uuid7)
    document_number = Faker("numerify", text="########")
    valid_from = Faker("past_date")
    valid_until = Faker("future_date")
    issue_country = random.choice(["ARG", "BRA", "CHL", "ESP", "URY", "USA"])
    passenger_id = LazyFunction(uuid7)
    document_type_id = 1


class RouteFactory(Factory):
    class Meta:
        model = Route

    id = Sequence(lambda n: n + 1)
    flight_number = Faker(
        "bothify", text="??####", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    origin = Faker("lexify", text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    destination = Faker("lexify", text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    distance_km = 1500
    duration_min = 180


class FlightFactory(Factory):
    class Meta:
        model = Flight

    id = LazyFunction(uuid7)
    scheduled_departure_datetime = Faker("future_datetime")
    scheduled_arrival_datetime = Faker("future_datetime")
    actual_departure_datetime = None
    actual_arrival_datetime = None
    operating_cost_usd = Decimal("5000.00")
    base_price_usd = Decimal("150.00")
    current_status_id = 1
    route_id = Sequence(lambda n: n + 1)
    airplane_id = Sequence(lambda n: n + 1)


class BookingFactory(Factory):
    class Meta:
        model = Booking

    id = LazyFunction(uuid7)
    booking_reference = Faker(
        "lexify", text="??????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    booking_datetime = Faker("past_datetime")
    paid_amount_usd = Decimal("450.00")
    current_status_id = 1


class TicketFactory(Factory):
    class Meta:
        model = Ticket

    id = LazyFunction(uuid7)
    ticket_number = Faker("numerify", text="#############")
    paid_amount_usd = Decimal("150.00")
    current_status_id = 1
    booking_id = LazyFunction(uuid7)
    flight_id = LazyFunction(uuid7)
    passenger_id = LazyFunction(uuid7)


class BoardingPassFactory(Factory):
    class Meta:
        model = BoardingPass

    id = LazyFunction(uuid7)
    issue_datetime = Faker("past_datetime")
    boarding_datetime = None
    current_status_id = 1
    ticket_id = LazyFunction(uuid7)
