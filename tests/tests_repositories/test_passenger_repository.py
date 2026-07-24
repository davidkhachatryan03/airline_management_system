from src.common.types import DocumentIdentityKey, PassengerId
from src.core.repositories import DocumentRepository, PassengerRepository
from src.entities import Document, Passenger


def test_insert_passenger(
    passenger_repository: PassengerRepository, passenger: Passenger
) -> None:
    passenger_repository.insert([passenger])

    last_inserted_passenger: Passenger = passenger_repository.retrieve(limit=1)[0]

    assert last_inserted_passenger == passenger


def test_retrieve_all_passengers(
    passenger_repository: PassengerRepository, passengers: list[Passenger]
) -> None:
    passenger_repository.insert(passengers)

    all_inserted_passengers: list[Passenger] = passenger_repository.retrieve(limit=3)

    assert len(all_inserted_passengers) == len(passengers)


def test_retrieve_passengers_by_id(
    passenger_repository: PassengerRepository, passengers: list[Passenger]
) -> None:
    passenger_repository.insert(passengers)

    passenger_ids: list[PassengerId] = [passenger.id for passenger in passengers]

    passengers_retrieved: list[Passenger] = passenger_repository.retrieve_by_ids(
        passenger_ids
    )

    assert set(passengers_retrieved) == set(passengers)


def test_retrieve_passengers_by_document(
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

    assert set(passengers_retrieved) == set(passengers)
