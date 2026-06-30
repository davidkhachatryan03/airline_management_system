from fastapi.testclient import TestClient
import pytest

from src.api.main import app
from src.api.routers.document_router import get_document_registrar
from src.api.schemas import DocumentResponse
from src.common.exceptions import *

client = TestClient(app)

def test_read_main() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "The server is working."}

def test_register_document_api_valid_input_and_output(mocker, document_request: dict) -> None:
    mocker_use_case = mocker.Mock()

    mocker_use_case.execute.return_value = DocumentResponse(
        document_number=document_request["document_number"],
        document_type_id=document_request["document_type_id"]
    )

    app.dependency_overrides[get_document_registrar] = lambda: mocker_use_case

    response = client.post("/api/documents", json=document_request)
    response_data = response.json()

    app.dependency_overrides.clear()

    assert len(response_data) == 2
    assert response.status_code == 200
    assert response_data["document_number"] == document_request["document_number"]
    assert response_data["document_type_id"] == document_request["document_type_id"]

@pytest.mark.parametrize("expected_exception, status_code", [
    (InexistentPassenger, 404),
    (DuplicatedDocument, 409)
])

def test_register_document_api_invalid_input(mocker, document_request: dict, expected_exception, status_code) -> None:
    mocker_use_case = mocker.Mock()

    mocker_use_case.execute.side_effect = expected_exception

    app.dependency_overrides[get_document_registrar] = lambda: mocker_use_case

    response = client.post("/api/documents", json=document_request)
    response_data = response.json()

    app.dependency_overrides.clear()

    assert len(response_data) == 2
    assert response.status_code == status_code
    assert response_data["error"] == expected_exception.__name__
    assert response_data["message"] == str(expected_exception())