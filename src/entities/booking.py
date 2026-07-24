import random
import string
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

import uuid6

from src.common.types import (BasePriceUsd, BookingDatetime, BookingId,
                              BookingReference, CurrentStatusId, PaidAmountUsd,
                              PassengerId)
from src.entities.base_entity import BaseEntity
from src.entities.flight import Flight
from src.entities.ticket import Ticket


class Booking(BaseEntity):

    def __init__(
        self,
        id: BookingId,
        booking_reference: BookingReference,
        booking_datetime: BookingDatetime,
        paid_amount_usd: PaidAmountUsd,
        current_status_id: CurrentStatusId,
    ) -> None:

        self.id = id
        self.booking_reference = booking_reference
        self.booking_datetime = booking_datetime
        self.paid_amount_usd = paid_amount_usd
        self.current_status_id = current_status_id

    @property
    def id(self) -> BookingId:
        return self._id

    @id.setter
    def id(self, value: BookingId) -> None:
        if not isinstance(value, BookingId.__value__):
            raise TypeError("The type of the id is not UUID.")

        self._id = value

    @property
    def booking_reference(self) -> BookingReference:
        return self._booking_reference

    @booking_reference.setter
    def booking_reference(self, value: BookingReference) -> None:
        if not isinstance(value, BookingReference.__value__):
            raise TypeError("The type of the booking reference is not str.")

        value_formatted: BookingReference = value.strip()

        if not value_formatted:
            raise ValueError("The booking reference can not be empty.")

        if len(value_formatted) != 6:
            raise ValueError("The booking reference mut be 6 characters long.")

        self._booking_reference = value_formatted

    @property
    def booking_datetime(self) -> BookingDatetime:
        return self._booking_datetime

    @booking_datetime.setter
    def booking_datetime(self, value: BookingDatetime) -> None:
        if not isinstance(value, BookingDatetime.__value__):
            raise TypeError("The type of the booking datetime is not datetime.")

        self._booking_datetime = value

    @property
    def paid_amount_usd(self) -> PaidAmountUsd:
        return self._paid_amount_usd

    @paid_amount_usd.setter
    def paid_amount_usd(self, value: PaidAmountUsd) -> None:
        if not isinstance(value, PaidAmountUsd.__value__):
            raise TypeError("The type of the paid amount is not decimal.")

        if value <= 0:
            raise ValueError("The paid amount can not be negative or zero.")

        self._paid_amount_usd = value

    @property
    def current_status_id(self) -> CurrentStatusId:
        return self._current_status_id

    @current_status_id.setter
    def current_status_id(self, value: CurrentStatusId) -> None:
        if not isinstance(value, CurrentStatusId.__value__):
            raise TypeError("The type of the current status id is not int.")

        if value <= 0:
            raise ValueError("The current status id can not be negative or zero.")

        self._current_status_id = value

    def generate_tickets(
        self,
        passenger_ids: list[PassengerId],
        flights: list[Flight],
        booking_id: BookingId,
    ) -> list[Ticket]:
        tickets_created: list[Ticket] = []

        for passenger_id in passenger_ids:
            for flight in flights:
                ticket_created = Ticket.new_ticket(
                    paid_amount_usd=flight.base_price_usd,
                    booking_id=booking_id,
                    flight_id=flight.id,
                    passenger_id=passenger_id,
                )

                tickets_created.append(ticket_created)

        return tickets_created

    @classmethod
    def new_booking(
        cls, flights_base_prices: list[BasePriceUsd], number_of_passengers: int
    ) -> "Booking":
        return cls(
            id=uuid6.uuid7(),
            booking_reference=cls._generate_reference(),
            booking_datetime=datetime.now(),
            paid_amount_usd=cls._calculate_paid_amount_usd(
                flights_base_prices, number_of_passengers
            ),
            current_status_id=1,
        )

    @staticmethod
    def _generate_reference() -> BookingReference:
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choices(chars, k=6))

    @staticmethod
    def _calculate_paid_amount_usd(
        flights_base_prices: list[BasePriceUsd], number_of_passengers: int
    ) -> PaidAmountUsd:
        paid_amount_usd: Decimal = (
            sum(
                (base_price_usd for base_price_usd in flights_base_prices), Decimal("0")
            )
            * number_of_passengers
        ).quantize(Decimal("0.01"), ROUND_HALF_UP)

        return paid_amount_usd
