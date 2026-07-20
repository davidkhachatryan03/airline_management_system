import uuid6

from src.common.types import (
    BirthDate,
    Email,
    FullName,
    IsBlacklisted,
    IsVip,
    PassengerId,
    PhoneNumber,
)
from src.entities.base_entity import BaseEntity


class Passenger(BaseEntity):

    def __init__(
        self,
        id: PassengerId,
        full_name: FullName,
        birth_date: BirthDate,
        email: Email,
        phone_number: PhoneNumber,
        is_blacklisted: IsBlacklisted,
        is_vip: IsVip,
    ) -> None:

        self.id = id
        self.full_name = full_name
        self.birth_date = birth_date
        self.email = email
        self.phone_number = phone_number
        self.is_blacklisted = is_blacklisted
        self.is_vip = is_vip

    @property
    def id(self) -> PassengerId:
        return self._id

    @id.setter
    def id(self, value: PassengerId) -> None:
        if not isinstance(value, PassengerId.__value__):
            raise TypeError("The type of the id is not UUID.")

        self._id = value

    @property
    def full_name(self) -> FullName:
        return self._full_name

    @full_name.setter
    def full_name(self, value: FullName) -> None:
        if not isinstance(value, FullName.__value__):
            raise TypeError("The type of the full name is not str.")

        value = value.strip()

        if not value:
            raise ValueError("The full name can not be empty.")

        if len(value) > 100:
            raise ValueError("The full name must be 100 characters long or less.")

        self._full_name = value

    @property
    def birth_date(self) -> BirthDate:
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: BirthDate) -> None:
        if not isinstance(value, BirthDate.__value__):
            raise TypeError("The type of the birth date is not date.")

        self._birth_date = value

    @property
    def email(self) -> Email:
        return self._email

    @email.setter
    def email(self, value: Email) -> None:
        if not isinstance(value, Email.__value__):
            raise TypeError("The type of the email is not str.")

        value = value.strip()

        if not value:
            raise ValueError("The email can not be empty.")

        if len(value) > 100:
            raise ValueError("The full name must be 100 characters long or less.")

        self._email = value

    @property
    def phone_number(self) -> PhoneNumber:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: PhoneNumber) -> None:
        if not isinstance(value, PhoneNumber.__value__):
            raise TypeError("The type of the phone number is not str.")

        value_formatted: PhoneNumber = value.strip()

        if not value_formatted:
            raise ValueError("The phone number can not be empty.")

        if len(value_formatted) > 20:
            raise ValueError("The phone number must be 20 characters long or less.")

        self._phone_number = value_formatted

    @property
    def is_blacklisted(self) -> IsBlacklisted:
        return self._is_blacklisted

    @is_blacklisted.setter
    def is_blacklisted(self, value: IsBlacklisted) -> None:
        if value not in [True, False, 1, 0]:
            raise TypeError(
                "The type of the blacklisted value must be True, False, 1 or 0."
            )

        self._is_blacklisted = bool(value)

    @property
    def is_vip(self) -> IsVip:
        return self._is_vip

    @is_vip.setter
    def is_vip(self, value: IsVip) -> None:
        if value not in [True, False, 1, 0]:
            raise TypeError("The type of the vip value must be True, False, 1 or 0.")

        self._is_vip = value

    @classmethod
    def new_passenger(
        cls,
        full_name: FullName,
        birth_date: BirthDate,
        email: Email,
        phone_number: PhoneNumber,
    ) -> "Passenger":
        return cls(
            id=uuid6.uuid7(),
            full_name=full_name,
            birth_date=birth_date,
            email=email,
            phone_number=phone_number,
            is_blacklisted=False,
            is_vip=False,
        )
