from src.common.types import DocumentIdentityKey
from src.core.repositories import DocumentRepository, PassengerRepository
from src.entities import Document, Passenger


def test_passenger_repository_retrieve_by_documents(
    passenger_repository: PassengerRepository,
    document_repository: DocumentRepository,
    passengers: list[Passenger],
    documents: list[Document],
) -> None:
    passenger_repository.insert(passengers)
    document_repository.insert(documents)

    document_identity_keys: list[DocumentIdentityKey] = [
        document.identity_key for document in documents
    ]

    passengers_retrieved: list[Passenger] = passenger_repository.retrieve_by_documents(
        document_identity_keys
    )

    assert set(passengers) == set(passengers_retrieved)
