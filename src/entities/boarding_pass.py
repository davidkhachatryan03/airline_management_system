from datetime import datetime

class BoardingPassCreated:

    def __init__(self,
                issue_datetime: datetime,
                boarding_datetime: datetime,
                current_status_id: int,
                ticket_id: int) -> None:
        
        self.issue_datetime = issue_datetime
        self.boarding_datetime = boarding_datetime
        self.current_status_id = current_status_id
        self.ticket_id = ticket_id

    @property
    def issue_datetime(self) -> datetime:
        return self._issue_datetime
    
    @issue_datetime.setter
    def issue_datetime(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError(f"The type of {value} is not datetime.")
        
        self._issue_datetime = value

    @property
    def boarding_datetime(self) -> datetime:
        return self._boarding_datetime
    
    @boarding_datetime.setter
    def boarding_datetime(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError(f"The type of {value} is not datetime.")
        
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
    def ticket_id(self) -> int:
        return self._ticket_id

    @ticket_id.setter
    def ticket_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value <= 0:
            raise ValueError(f"The ticket id can not be negative or zero.")
        
        self._ticket_id = value

    def to_dict(self) -> dict:
        return {
            "issue_datetime": self.issue_datetime,
            "boarding_datetime": self.boarding_datetime,
            "current_status_id": self.current_status_id,
            "ticket_id": self.ticket_id
        }

class BoardingPassRetrieved:

    def __init__(self,
                id: int,
                issue_datetime: datetime,
                boarding_datetime: datetime,
                current_status_id: int,
                ticket_id: int) -> None:
        
        self.id = id
        self.issue_datetime = issue_datetime
        self.boarding_datetime = boarding_datetime
        self.current_status_id = current_status_id
        self.ticket_id = ticket_id