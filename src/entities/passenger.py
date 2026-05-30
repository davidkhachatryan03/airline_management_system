from uuid import UUID
import uuid6
from datetime import date

class Passenger:

    def __init__(self,
                id: UUID,
                full_name: str,
                birth_date: date,
                email: str,
                phone_number: str,
                is_blacklisted: bool,
                is_vip: bool) -> None:
        
        self.id = id
        self.full_name = full_name
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
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._id = value

    @property
    def full_name(self) -> str:
        return self._full_name
    
    @full_name.setter
    def full_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
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
            raise TypeError(f"The type of {value} is not date.")
        
        self._birth_date = value

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        value = value.strip()
        
        if not value:
            raise ValueError("The email can not be empty.")
        
        if len(value) > 100:
            raise ValueError("The full name must be 100 characters long or less.")
        
        self._email = value

    @property
    def phone_number(self) -> int:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not str.")
        
        if not value:
            raise ValueError("The phone number can not be empty.")
        
        if len(value) > 20:
            raise ValueError("The full name must be 20 characters long or less.")
        
        self._phone_number = value
    
    @property
    def is_blacklisted(self) -> bool:
        return self._is_blacklisted
    
    @is_blacklisted.setter
    def is_blacklisted(self, value: bool) -> None:
        if value not in [True, False, 1, 0]:
            raise TypeError(f"The type of {value} is not bool.")
        
        self._is_blacklisted = bool(value)

    @property
    def is_vip(self) -> bool:
        return self._is_vip
    
    @is_vip.setter
    def is_vip(self, value: bool) -> None:
        if value not in [True, False, 1, 0]:
            raise TypeError(f"The type of {value} is not bool.")
        
        self._is_vip = value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "is_blacklisted": self.is_blacklisted,
            "is_vip": self.is_vip
        }
    
    @classmethod
    def new_passenger(cls, values: dict) -> "Passenger":
        return cls(
            id=uuid6.uuid7(), 
            full_name=values["full_name"],
            birth_date=values["birth_date"],
            email=values["email"],
            phone_number=values["phone_number"],
            is_blacklisted=values.get("is_blacklisted", False), 
            is_vip=values.get("is_vip", False)
        )