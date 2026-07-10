from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

class FlightRequest(BaseModel):
    scheduled_departure_datetime: datetime
    scheduled_arrival_datetime: datetime
    route_id: int = Field(gt=0)
    airplane_id: int = Field(gt=0)

    @property
    def identity_key(self) -> tuple[datetime, int]:
        return (self.scheduled_departure_datetime, self.route_id)

class FlightResponse(BaseModel):
    id: UUID