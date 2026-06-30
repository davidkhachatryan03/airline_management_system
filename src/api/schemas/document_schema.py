from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

class DocumentRequest(BaseModel):
    document_number: str = Field(min_length=5)
    valid_from: date
    valid_until: date
    issue_country: str = Field(min_length=3, max_length=3)
    passenger_id: UUID
    document_type_id: int = Field(gt=0)

    @property
    def identity_key(self) -> tuple:
        return (self.document_number, self.issue_country)

class DocumentResponse(BaseModel):
    document_number: str = Field(min_length=5)
    document_type_id: int = Field(gt=0)