from pydantic import BaseModel, Field

from src.common.types import ScheduledDepartureDatetime, ScheduledArrivalDatetime, RouteId, AirplaneId, FlightIdentityKey, FlightId


class FlightRequest(BaseModel):
    scheduled_departure_datetime: ScheduledDepartureDatetime
    scheduled_arrival_datetime: ScheduledArrivalDatetime
    route_id: RouteId = Field(gt=0)
    airplane_id: AirplaneId = Field(gt=0)

    @property
    def identity_key(self) -> FlightIdentityKey:
        return (self.scheduled_departure_datetime, self.route_id)


class FlightResponse(BaseModel):
    id: FlightId
