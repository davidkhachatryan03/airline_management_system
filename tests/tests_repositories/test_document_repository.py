from src.common.types import DocumentIdentityKey
from src.core.repositories import DocumentRepository, PassengerRepository
from src.entities import Document, Passenger


def test_insert_document(
    document_repository: DocumentRepository,
    passenger_repository: PassengerRepository,
    document: Document,
    passenger: Passenger,
) -> None:
    passenger_repository.insert_passengers([passenger])
    document_repository.insert_documents([document])

    last_inserted_document: Document = document_repository.retrieve_documents(limit=1)[
        0
    ]

    assert last_inserted_document.id == document.id
    assert last_inserted_document.document_number == document.document_number
    assert last_inserted_document.valid_from == document.valid_from
    assert last_inserted_document.valid_until == document.valid_until
    assert last_inserted_document.issue_country == document.issue_country
    assert last_inserted_document.passenger_id == document.passenger_id
    assert last_inserted_document.document_type_id == document.document_type_id


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

    document_identity_keys: list[DocumentIdentityKey] = [document.identity_key for document in documents]

    documents_retrieved: list[Document] = document_repository.retrieve_documents_by_identity_key(
        document_identity_keys
    )

    assert set(documents) == set(documents_retrieved)