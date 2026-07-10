from datetime import date
from uuid import UUID
import uuid6

from src.common.types import PassengerIdentityKey

class Passenger:

    def __init__(self,
                id: UUID,
                national_identity_number: str,
                issue_country: str,
                full_name: str,
                birth_date: date,
                email: str,
                phone_number: str,
                is_blacklisted: bool,
                is_vip: bool) -> None:
        
        self.id = id
        self.full_name = full_name
        self.national_identity_number = national_identity_number
        self.issue_country = issue_country
        self.birth_date = birth_date
        self.email = email
        self.phone_number = phone_number
        self.is_blacklisted = is_blacklisted
        self.is_vip = is_vip
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @id.setter
    def id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError("The type of the id is not UUID.")
        
        self._id = value

    @property
    def national_identity_number(self) -> str:
        return self._national_identity_number
    
    @national_identity_number.setter
    def national_identity_number(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The type of the national_identity_number is not str.")
        
        value = value.strip()

        if not value:
            raise ValueError("The national_identity_number can not be empty.")
        
        if len(value) > 20:
            raise ValueError("The national_identity_number must be 20 characters long or less.")
        
        self._national_identity_number = value
    
    @property
    def issue_country(self) -> str:
        return self._issue_country
    
    @issue_country.setter
    def issue_country(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of the issue country is not str.")

        value_formatted: str = value.strip()
        
        if not value_formatted:
            raise ValueError("The issue country can not be empty.")
        
        if len(value_formatted) != 3:
            raise ValueError("The issue country must be 3 characters long.")
        
        self._issue_country = value

    @property
    def full_name(self) -> str:
        return self._full_name
    
    @full_name.setter
    def full_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The type of the full name is not str.")
        
        value = value.strip()

        if not value:
            raise ValueError("The full name can not be empty.")
        
        if len(value) > 100:
            raise ValueError("The full name must be 100 characters long or less.")
        
        self._full_name = value
    
    @property
    def birth_date(self) -> date:
        return self._birth_date
    
    @birth_date.setter
    def birth_date(self, value: date) -> None:
        if not isinstance(value, date):
            raise TypeError("The type of the birth date is not date.")
        
        self._birth_date = value

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The type of the email is not str.")
        
        value = value.strip()
        
        if not value:
            raise ValueError("The email can not be empty.")
        
        if len(value) > 100:
            raise ValueError("The full name must be 100 characters long or less.")
        
        self._email = value

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The type of the phone number is not str.")
        
        value_formatted: str = value.strip()
        
        if not value_formatted:
            raise ValueError("The phone number can not be empty.")
        
        if len(value_formatted) > 20:
            raise ValueError("The phone number must be 20 characters long or less.")
        
        self._phone_number = value_formatted
    
    @property
    def is_blacklisted(self) -> bool:
        return self._is_blacklisted
    
    @is_blacklisted.setter
    def is_blacklisted(self, value: bool) -> None:
        if value not in [True, False, 1, 0]:
            raise TypeError("The type of the blacklisted value must be True, False, 1 or 0.")
        
        self._is_blacklisted = bool(value)

    @property
    def is_vip(self) -> bool:
        return self._is_vip
    
    @is_vip.setter
    def is_vip(self, value: bool) -> None:
        if value not in [True, False, 1, 0]:
            raise TypeError("The type of the vip value must be True, False, 1 or 0.")
        
        self._is_vip = value

    @property
    def identity_key(self) -> PassengerIdentityKey:
        return (self.national_identity_number, self.issue_country)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "national_identity_number": self.national_identity_number,
            "issue_country": self.issue_country,
            "birth_date": self.birth_date,
            "email": self.email,
            "phone_number": self.phone_number,
            "is_blacklisted": self.is_blacklisted,
            "is_vip": self.is_vip
        }
    
    @classmethod
    def new_passenger(cls, full_name: str, national_identity_number: str, issue_country: str, birth_date: date, email: str, phone_number: str) -> "Passenger":
        return cls(
            id=uuid6.uuid7(), 
            full_name=full_name,
            national_identity_number=national_identity_number,
            issue_country=issue_country,
            birth_date=birth_date,
            email=email,
            phone_number=phone_number,
            is_blacklisted=False, 
            is_vip=False
        )