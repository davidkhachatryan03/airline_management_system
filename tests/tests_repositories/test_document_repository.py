from src.common.types import DocumentIdentityKey
from src.core.repositories import DocumentRepository, PassengerRepository
from src.entities import Document, Passenger


def test_insert_documents(
    document_repository: DocumentRepository,
    passenger_repository: PassengerRepository,
    documents: list[Document],
    passengers: list[Passenger],
) -> None:
    passenger_repository.insert_passengers(passengers)
    document_repository.insert_documents(documents)

    last_inserted_documents: list[Document] = document_repository.retrieve_documents(
        limit=5
    )

    assert set(last_inserted_documents) == set(documents)


def test_retrieve_all_documents(
    document_repository: DocumentRepository,
    passenger_repository: PassengerRepository,
    documents: list[Document],
    passengers: list[Passenger],
) -> None:
    passenger_repository.insert_passengers(passengers)
    document_repository.insert_documents(documents)

    all_inserted_documents: list[Document] = document_repository.retrieve_documents(
        limit=3
    )

    assert len(all_inserted_documents) == len(documents)


def test_retrieve_documents_by_identity_key(
    document_repository: DocumentRepository,
    passenger_repository: PassengerRepository,
    documents: list[Document],
    passengers: list[Passenger],
) -> None:
    passenger_repository.insert_passengers(passengers)
    document_repository.insert_documents(documents)

    document_identity_keys: list[DocumentIdentityKey] = [
        document.identity_key for document in documents
    ]

    documents_retrieved: list[Document] = (
        document_repository.retrieve_documents_by_identity_keys(document_identity_keys)
    )

    assert set(documents) == set(documents_retrieved)
