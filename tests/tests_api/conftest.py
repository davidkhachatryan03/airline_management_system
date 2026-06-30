import pytest

@pytest.fixture
def booking_request() -> dict:
    return {
        "flights_id": ["019ef4a6-dc54-7d5f-b3ba-df1acea2d9c7", "019ef4a7-2505-77c0-ab0a-dd9185248a1a"],
        "passengers": [
            {
                "full_name": "David Khachatryan",
                "birth_date": "2000-01-01",
                "email": "email@example.com",
                "phone_number": "5491123456789",
                "national_identity_number": "40123456",
                "valid_from": "2010-01-01",
                "valid_until": "2020-01-01",
                "issue_country": "ARG"
            }
        ]
    }

@pytest.fixture
def document_request() -> dict:
    return {
        "document_number": "ABC12345",
        "valid_from": "2010-01-01",
        "valid_until": "2020-01-01",
        "issue_country": "ARG",
        "passenger_id": "019ef4a6-dc54-7d5f-b3ba-df1acea2d9c7",
        "document_type_id": 1
    }