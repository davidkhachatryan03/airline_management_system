from decimal import Decimal

import pytest, uuid6
from pydantic import ValidationError

from src.api.schemas import BookingRequest, BookingResponse, PassengerRequest

def test_booking_request_valid_data(passenger_request: PassengerRequest) -> None:
    data = {
        "flights_id": [uuid6.uuid7(), uuid6.uuid7()],
        "passengers": [passenger_request.model_dump(mode="json")]
    }
    
    request = BookingRequest(**data)
    
    assert len(request.flights_id) == 2
    assert len(request.passengers) == 1

def test_booking_request_duplicate_flights_raises_error(passenger_request: PassengerRequest) -> None:
    flight_id = uuid6.uuid7()
    data = {
        "flights_id": [flight_id, flight_id], 
        "passengers": [passenger_request.model_dump(mode="json")]
    }
    
    with pytest.raises(ValidationError) as exc_info:
        BookingRequest(**data)
    
    assert "The flights must be unique" in str(exc_info.value)

def test_booking_request_empty_lists_raises_error() -> None:
    data = {
        "flights_id": [],
        "passengers": []
    }
    
    with pytest.raises(ValidationError) as exc_info:
        BookingRequest(**data)
        
    assert "flights_id" in str(exc_info.value)
    assert "passengers" in str(exc_info.value)

def test_booking_response_valid_data() -> None:
    data = {
        "booking_reference": "FL-998877",
        "tickets": ["TKT-1", "TKT-2"],
        "paid_amount_usd": Decimal("250.50")
    }
    
    response = BookingResponse(**data)
    
    assert response.booking_reference == "FL-998877"
    assert len(response.tickets) == 2
    assert response.booking_datetime is not None 

def test_booking_response_negative_amount_raises_error() -> None:
    data = {
        "booking_reference": "FL-998877",
        "tickets": ["TKT-1"],
        "paid_amount_usd": Decimal("-5.00") 
    }
    
    with pytest.raises(ValidationError) as exc_info:
        BookingResponse(**data)
        
    assert "Input should be greater than 0" in str(exc_info.value)

def test_booking_response_invalid_decimals_raises_error() -> None:
    data = {
        "booking_reference": "FL-998877",
        "tickets": ["TKT-1"],
        "paid_amount_usd": Decimal("100.555")
    }
    
    with pytest.raises(ValidationError):
        BookingResponse(**data)