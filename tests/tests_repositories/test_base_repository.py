from src.common.types import DocumentId, DocumentIdentityKey, PassengerId
from src.core.repositories import DocumentRepository, PassengerRepository
from src.entities import Document, Passenger
from tests.factories import DocumentFactory, PassengerFactory


def test_base_repository_insert_and_retrieve(
    passenger_repository: PassengerRepository,
    document_repository: DocumentRepository,
) -> None:
    passengers: list[Passenger] = PassengerFactory.build_batch(50)
    documents: list[Document] = [
        DocumentFactory(passenger_id=passenger.id) for passenger in passengers
    ]

    passenger_repository.insert(passengers)
    document_repository.insert(documents)

    passenger_ids: list[PassengerId] = [passenger.id for passenger in passengers]
    document_ids: list[DocumentId] = [document.id for document in documents]

    passengers_set = set(passengers)
    documents_set = set(documents)

    document_identity_keys: list[DocumentIdentityKey] = [
        document.identity_key for document in documents
    ]

    passengers_retrieved: list[Passenger] = passenger_repository.retrieve(
        limit=len(passengers)
    )
    documents_retrieved: list[Document] = document_repository.retrieve(
        limit=len(documents)
    )

    assert set(passengers_retrieved) == passengers_set
    assert set(documents_retrieved) == documents_set

    passengers_retrieved: list[Passenger] = passenger_repository.retrieve_by_ids(
        passenger_ids
    )
    documents_retrieved: list[Document] = document_repository.retrieve_by_ids(
        document_ids
    )

    assert set(passengers_retrieved) == passengers_set
    assert set(documents_retrieved) == documents_set

    documents_retrieved: list[Document] = document_repository.retrieve_by_identity_keys(
        document_identity_keys
    )

    assert set(documents_retrieved) == documents_set
