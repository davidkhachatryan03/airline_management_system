from datetime import date
from uuid import UUID

class Document:

    def __init__(self,
                id: UUID,
                document_number: str,
                valid_from: date,
                valid_until: date,
                issue_country: str,
                passenger_id: UUID,
                document_type_id: int) -> None:
        
        self.id = id
        self.document_number = document_number
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.issue_country = issue_country
        self.passenger_id = passenger_id
        self.document_type_id = document_type_id
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @id.setter
    def id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._id = value

    @property
    def document_number(self) -> str:
        return self._document_number
    
    @document_number.setter
    def document_number(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        value = value.strip()
        
        if not value:
            raise ValueError("The document number can not be empty.")
        
        if len(value) > 20:
            raise ValueError("The document number mut be 20 characters or less.")
        
        self._document_number = value
        
    @property
    def valid_from(self) -> date:
        return self._valid_from
    
    @valid_from.setter
    def valid_from(self, value: date) -> None:
        if not isinstance(value, date):
            raise TypeError(f"The type of {value} is not date.")
        
        self._valid_from = value

    @property
    def valid_until(self) -> date:
        return self._valid_until
    
    @valid_until.setter
    def valid_until(self, value: date) -> None:
        if not isinstance(value, date):
            raise TypeError(f"The type of {value} is not date.")
        
        self._valid_until = value

    @property
    def issue_country(self) -> str:
        return self._issue_country
    
    @issue_country.setter
    def issue_country(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        if not value.strip():
            raise ValueError("The issue country can not be empty.")
        
        if len(value.strip()) != 3:
            raise ValueError("The issue country must be 3 characters long.")
        
        self._issue_country = value

    @property
    def passenger_id(self) -> UUID:
        return self._passenger_id
    
    @passenger_id.setter
    def passenger_id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._passenger_id = value
    
    @property
    def document_type_id(self) -> int:
        return self._document_type_id
    
    @document_type_id.setter
    def document_type_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value <= 0:
            raise ValueError("The passenger id can not be negative or zero.")
        
        self._document_type_id = value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "document_number": self.document_number,
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "issue_country": self.issue_country,
            "passenger_id": self.passenger_id,
            "document_type_id": self.document_type_id
        }