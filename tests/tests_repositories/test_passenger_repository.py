from factory.declarations import Iterator

from src.common.types import DocumentIdentityKey, PassengerId
from src.core.repositories import DocumentRepository, PassengerRepository
from src.entities import Document, Passenger
from tests.factories import DocumentFactory, PassengerFactory


def test_passenger_repository_retrieve_by_documents(
    passenger_repository: PassengerRepository,
    document_repository: DocumentRepository,
) -> None:
    passengers: list[Passenger] = PassengerFactory.build_batch(50)
    passenger_ids: list[PassengerId] = [passenger.id for passenger in passengers]
    documents: list[Document] = DocumentFactory.build_batch(
        50, passenger_id=Iterator(passenger_ids)
    )

    passenger_repository.insert(passengers)
    document_repository.insert(documents)

    document_identity_keys: list[DocumentIdentityKey] = [
        document.identity_key for document in documents
    ]

    passengers_retrieved: list[Passenger] = passenger_repository.retrieve_by_documents(
        document_identity_keys
    )

    assert set(passengers) == set(passengers_retrieved)
