import pytest, uuid6
from datetime import date
from pydantic import ValidationError

from src.api.schemas import DocumentRequest, DocumentResponse

def test_document_request_valid_data() -> None:
    data = {
        "document_number": "ABC12345",
        "valid_from": date(2023, 1, 1),
        "valid_until": date(2033, 1, 1),
        "issue_country": "ARG",
        "passenger_id": uuid6.uuid7(),
        "document_type_id": 1
    }
    
    request = DocumentRequest(**data)
    
    assert request.document_number == "ABC12345"
    assert request.issue_country == "ARG"
    
    assert request.identity_key == ("ABC12345", "ARG")

def test_document_request_short_document_number_raises_error() -> None:
    data = {
        "document_number": "1234",
        "valid_from": date(2023, 1, 1),
        "valid_until": date(2033, 1, 1),
        "issue_country": "ARG",
        "passenger_id": uuid6.uuid7(),
        "document_type_id": 1
    }
    
    with pytest.raises(ValidationError) as exc_info:
        DocumentRequest(**data)
        
    assert "String should have at least 5 characters" in str(exc_info.value)

def test_document_request_invalid_country_length_raises_error() -> None:
    base_data = {
        "document_number": "ABC12345",
        "valid_from": date(2023, 1, 1),
        "valid_until": date(2033, 1, 1),
        "passenger_id": uuid6.uuid7(),
        "document_type_id": 1
    }
    
    with pytest.raises(ValidationError) as exc_info_short:
        DocumentRequest(**base_data, issue_country="AR")
    assert "String should have at least 3 characters" in str(exc_info_short.value)

    with pytest.raises(ValidationError) as exc_info_long:
        DocumentRequest(**base_data, issue_country="ARGN")
    assert "String should have at most 3 characters" in str(exc_info_long.value)

def test_document_request_invalid_type_id_raises_error() -> None:
    data = {
        "document_number": "ABC12345",
        "valid_from": date(2023, 1, 1),
        "valid_until": date(2033, 1, 1),
        "issue_country": "ARG",
        "passenger_id": uuid6.uuid7(),
        "document_type_id": 0 
    }
    
    with pytest.raises(ValidationError) as exc_info:
        DocumentRequest(**data)
        
    assert "Input should be greater than 0" in str(exc_info.value)

def test_document_response_valid_data() -> None:
    data = {
        "document_number": "ABC12345",
        "document_type_id": 2
    }
    
    response = DocumentResponse(**data)
    
    assert response.document_number == "ABC12345"
    assert response.document_type_id == 2

def test_document_response_invalid_data_raises_error() -> None:
    data = {
        "document_number": "123", 
        "document_type_id": -1  
    }
    
    with pytest.raises(ValidationError) as exc_info:
        DocumentResponse(**data)
        
    error_msg = str(exc_info.value)
    assert "document_number" in error_msg
    assert "document_type_id" in error_msg