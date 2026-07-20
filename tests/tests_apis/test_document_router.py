from uuid import UUID

from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from src.api.main import app
from src.api.routers.document_router import create_register_document
from src.api.schemas import DocumentRequest, DocumentResponse
from src.common.exceptions import (
    DuplicatedDocument,
    InexistentPassenger,
    MultipleExceptionsError,
)


def test_document_router_no_exceptions(
    mocker: MockerFixture,
    client: TestClient,
    document_request: DocumentRequest,
    document_response: DocumentResponse,
) -> None:
    mock_use_case = mocker.Mock()
    mock_use_case.execute.return_value = document_response

    app.dependency_overrides[create_register_document] = lambda: mock_use_case

    response = client.post(
        "/api/documents", json=document_request.model_dump(mode="json")
    )

    assert response.status_code == 200
    assert response.json() == document_response.model_dump(mode="json")


def test_document_router_multiple_exceptions(
    mocker: MockerFixture, client: TestClient, document_request: DocumentRequest
) -> None:
    mock_use_case = mocker.Mock()
    mock_use_case.execute.side_effect = MultipleExceptionsError(
        [
            InexistentPassenger(id=UUID("019f75c1-ab3f-7a29-a624-9da6c04e5a70")),
            DuplicatedDocument(identity_key=document_request.identity_key),
        ]
    )

    app.dependency_overrides[create_register_document] = lambda: mock_use_case

    response = client.post(
        "/api/documents", json=document_request.model_dump(mode="json")
    )

    expected_response = {
        "total_errors": 2,
        "details": [
            {
                "error": "InexistentPassenger",
                "message": "The passenger with id 019f75c1-ab3f-7a29-a624-9da6c04e5a70 is not registered.",
                "internal_code": 404,
            },
            {
                "error": "DuplicatedDocument",
                "message": f"The document with id {document_request.identity_key} is already registered.",
                "internal_code": 409,
            },
        ],
    }

    assert response.status_code == 422
    assert response.json() == expected_response
