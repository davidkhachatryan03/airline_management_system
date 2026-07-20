import uuid6

from src.common.types import (
    DocumentId,
    DocumentIdentityKey,
    DocumentNumber,
    DocumentTypeId,
    IssueCountry,
    PassengerId,
    ValidFrom,
    ValidUntil,
)
from src.entities.base_entity import BaseEntity


class Document(BaseEntity):

    def __init__(
        self,
        id: DocumentId,
        document_number: DocumentNumber,
        valid_from: ValidFrom,
        valid_until: ValidUntil,
        issue_country: IssueCountry,
        passenger_id: PassengerId,
        document_type_id: DocumentTypeId,
    ) -> None:

        self.id = id
        self.document_number = document_number
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.issue_country = issue_country
        self.passenger_id = passenger_id
        self.document_type_id = document_type_id

    @property
    def id(self) -> DocumentId:
        return self._id

    @id.setter
    def id(self, value: DocumentId) -> None:
        if not isinstance(value, DocumentId.__value__):
            raise TypeError("The type of the id is not UUID.")

        self._id = value

    @property
    def document_number(self) -> DocumentNumber:
        return self._document_number

    @document_number.setter
    def document_number(self, value: DocumentNumber) -> None:
        if not isinstance(value, DocumentNumber.__value__):
            raise TypeError("The type of the document number is not str.")

        value_formatted: DocumentNumber = value.strip()

        if not value_formatted:
            raise ValueError("The document number can not be empty.")

        if len(value_formatted) > 20:
            raise ValueError("The document number must be 20 characters or less.")

        self._document_number = value_formatted

    @property
    def valid_from(self) -> ValidFrom:
        return self._valid_from

    @valid_from.setter
    def valid_from(self, value: ValidFrom) -> None:
        if not isinstance(value, ValidFrom.__value__):
            raise TypeError("The type of the valid from date is not date.")

        self._valid_from = value

    @property
    def valid_until(self) -> ValidUntil:
        return self._valid_until

    @valid_until.setter
    def valid_until(self, value: ValidUntil) -> None:
        if not isinstance(value, ValidUntil.__value__):
            raise TypeError(f"The type of the valid until date is not date.")

        self._valid_until = value

    @property
    def issue_country(self) -> IssueCountry:
        return self._issue_country

    @issue_country.setter
    def issue_country(self, value: IssueCountry) -> None:
        if not isinstance(value, IssueCountry.__value__):
            raise TypeError(f"The type of the issue country is not str.")

        value_formatted: IssueCountry = value.strip()

        if not value_formatted:
            raise ValueError("The issue country can not be empty.")

        if len(value_formatted) != 3:
            raise ValueError("The issue country must be 3 characters long.")

        self._issue_country = value

    @property
    def passenger_id(self) -> PassengerId:
        return self._passenger_id

    @passenger_id.setter
    def passenger_id(self, value: PassengerId) -> None:
        if not isinstance(value, PassengerId.__value__):
            raise TypeError("The type of the passenger id is not UUID.")

        self._passenger_id = value

    @property
    def document_type_id(self) -> DocumentTypeId:
        return self._document_type_id

    @document_type_id.setter
    def document_type_id(self, value: DocumentTypeId) -> None:
        if not isinstance(value, DocumentTypeId.__value__):
            raise TypeError("The type of the document type id is not int.")

        if value <= 0:
            raise ValueError("The document type id can not be negative or zero.")

        self._document_type_id = value

    @property
    def identity_key(self) -> DocumentIdentityKey:
        return (self.document_number, self.issue_country)

    @classmethod
    def new_document(
        cls,
        document_number: DocumentNumber,
        valid_from: ValidFrom,
        valid_until: ValidUntil,
        issue_country: IssueCountry,
        passenger_id: PassengerId,
        document_type_id: DocumentTypeId,
    ) -> "Document":
        return cls(
            id=uuid6.uuid7(),
            document_number=document_number,
            valid_from=valid_from,
            valid_until=valid_until,
            issue_country=issue_country,
            passenger_id=passenger_id,
            document_type_id=document_type_id,
        )
