from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

class FlightRequest(BaseModel):
    scheduled_departure_datetime: datetime
    scheduled_arrival_datetime: datetime
    route_id: int = Field(gt=0)
    airplane_id: int = Field(gt=0)

class FlightResponse(BaseModel):
    id: UUID