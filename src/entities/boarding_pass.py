from datetime import datetime
from uuid import UUID

from src.entities.base_entity import BaseEntity


class BoardingPass(BaseEntity):

    def __init__(self,
                id: UUID,
                issue_datetime: datetime,
                boarding_datetime: datetime | None,
                current_status_id: int,
                ticket_id: UUID) -> None:
        
        self.id = id
        self.issue_datetime = issue_datetime
        self.boarding_datetime = boarding_datetime
        self.current_status_id = current_status_id
        self.ticket_id = ticket_id

    @property
    def id(self) -> UUID:
        return self._id
    
    @id.setter
    def id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._id = value

    @property
    def issue_datetime(self) -> datetime:
        return self._issue_datetime
    
    @issue_datetime.setter
    def issue_datetime(self, value: datetime | None) -> None:
        if not isinstance(value, datetime):
            raise TypeError(f"The type of {value} is not datetime.")
        
        self._issue_datetime = value

    @property
    def boarding_datetime(self) -> datetime:
        return self._boarding_datetime
    
    @boarding_datetime.setter
    def boarding_datetime(self, value: datetime | None) -> None:
        if not isinstance(value, datetime) or value is not None:
            raise TypeError(f"The type of {value} must be datetime or none.")
        
        self._boarding_datetime = value

    @property
    def current_status_id(self) -> int:
        return self._current_status_id

    @current_status_id.setter
    def current_status_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value <= 0:
            raise ValueError(f"The current status id can not be negative or zero.")
        
        self._current_status_id = value

    @property
    def ticket_id(self) -> UUID:
        return self._ticket_id

    @ticket_id.setter
    def ticket_id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._ticket_id = value