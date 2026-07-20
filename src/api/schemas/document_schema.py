from pydantic import BaseModel, Field

from src.common.types import DocumentNumber, ValidFrom, ValidUntil, IssueCountry, PassengerId, DocumentTypeId, DocumentIdentityKey

class DocumentRequest(BaseModel):
    document_number: DocumentNumber = Field(min_length=5)
    valid_from: ValidFrom
    valid_until: ValidUntil
    issue_country: IssueCountry = Field(min_length=3, max_length=3)
    passenger_id: PassengerId
    document_type_id: DocumentTypeId = Field(gt=0)

    @property
    def identity_key(self) -> DocumentIdentityKey:
        return (self.document_number, self.issue_country)


class DocumentResponse(BaseModel):
    document_number: DocumentNumber = Field(min_length=5)
    document_type_id: DocumentTypeId = Field(gt=0)
