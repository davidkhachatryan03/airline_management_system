from datetime import date

from pydantic import BaseModel, EmailStr, Field, model_validator


class PassengerRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    birth_date: date
    email: EmailStr
    phone_number: str = Field(min_length=3, max_length=20, pattern=r"^[1-9]\d{1,14}$")
    document_number: str = Field(min_length=3, max_length=20)
    valid_from: date
    valid_until: date
    issue_country: str = Field(min_length=3, max_length=3)
    document_type_id: int = Field(gt=0)

    @property
    def identity_key(self) -> tuple:
        return (self.document_number, self.issue_country)

@model_validator(mode='after')
def validate_document_dates(self) -> PassengerRequest:
    if self.valid_from >= self.valid_until:
        raise ValueError("The issue date can not be greater than the expiration date.")

    if self.valid_until <= date.today():
        raise ValueError("The document is expired.")
        
    if self.valid_from > date.today():
        raise ValueError("The issue date is invalid.")

    return self