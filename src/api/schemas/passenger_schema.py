from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import date

class PassengerRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    birth_date: date
    email: EmailStr
    phone_number: str = Field(min_length=3, max_length=20, pattern=r"^\+[1-9]\d{1,14}$")
    document_number: str = Field(min_length=3, max_length=20)
    valid_from: date
    valid_until: date
    issue_country: str = Field(min_length=3, max_length=3)
    document_type_id: int