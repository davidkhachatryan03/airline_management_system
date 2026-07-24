import random
import string

import uuid6

from src.common.types import (BookingId, CurrentStatusId, FlightId,
                              PaidAmountUsd, PassengerId, TicketId,
                              TicketNumber)
from src.entities.base_entity import BaseEntity


class Ticket(BaseEntity):

    def __init__(
        self,
        id: TicketId,
        ticket_number: TicketNumber,
        paid_amount_usd: PaidAmountUsd,
        current_status_id: CurrentStatusId,
        booking_id: BookingId,
        flight_id: FlightId,
        passenger_id: PassengerId,
    ) -> None:

        self.id = id
        self.ticket_number = ticket_number
        self.paid_amount_usd = paid_amount_usd
        self.current_status_id = current_status_id
        self.booking_id = booking_id
        self.flight_id = flight_id
        self.passenger_id = passenger_id

    @property
    def id(self) -> TicketId:
        return self._id

    @id.setter
    def id(self, value: TicketId) -> None:
        if not isinstance(value, TicketId.__value__):
            raise TypeError("The type of the id is not UUID.")

        self._id = value

    @property
    def ticket_number(self) -> TicketNumber:
        return self._ticket_number

    @ticket_number.setter
    def ticket_number(self, value: TicketNumber) -> None:
        if not isinstance(value, TicketNumber.__value__):
            raise TypeError("The type of the ticket number is not str.")

        value_formatted: TicketNumber = value.strip()

        if not value_formatted:
            raise ValueError("The ticket number can not be empty.")

        if len(value_formatted) != 13:
            raise ValueError("The ticket number must be exactly 13 characters long.")

        if not value_formatted.isnumeric():
            raise ValueError("The ticket number must only contain digits.")

        self._ticket_number = value_formatted

    @property
    def paid_amount_usd(self) -> PaidAmountUsd:
        return self._paid_amount_usd

    @paid_amount_usd.setter
    def paid_amount_usd(self, value: PaidAmountUsd) -> None:
        if not isinstance(value, PaidAmountUsd.__value__):
            raise TypeError(f"The type of the paid amount is not decimal.")

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

    @property
    def booking_id(self) -> BookingId:
        return self._booking_id

    @booking_id.setter
    def booking_id(self, value: BookingId) -> None:
        if not isinstance(value, BookingId.__value__):
            raise TypeError("The type of the booking id is not UUID.")

        self._booking_id = value

    @property
    def flight_id(self) -> FlightId:
        return self._flight_id

    @flight_id.setter
    def flight_id(self, value: FlightId) -> None:
        if not isinstance(value, FlightId.__value__):
            raise TypeError("The type of the flight id is not UUID.")

        self._flight_id = value

    @property
    def passenger_id(self) -> PassengerId:
        return self._passenger_id

    @passenger_id.setter
    def passenger_id(self, value: PassengerId) -> None:
        if not isinstance(value, PassengerId.__value__):
            raise TypeError("The type of the passenger id is not UUID.")

        self._passenger_id = value

    @classmethod
    def new_ticket(
        cls,
        paid_amount_usd: PaidAmountUsd,
        booking_id: BookingId,
        flight_id: FlightId,
        passenger_id: PassengerId,
    ) -> "Ticket":
        return cls(
            id=uuid6.uuid7(),
            ticket_number=cls._generate_ticket_number(),
            paid_amount_usd=paid_amount_usd,
            current_status_id=1,
            booking_id=booking_id,
            flight_id=flight_id,
            passenger_id=passenger_id,
        )

    @staticmethod
    def _generate_ticket_number() -> TicketNumber:
        first_digit = str(random.randint(1, 9))
        rest_digits = "".join(random.choices(string.digits, k=12))

        return first_digit + rest_digits
