from src.common.types import IssueDatetime, BoardingPassId, TicketId, BoardingDatetime, CurrentStatusId
from src.entities.base_entity import BaseEntity


class BoardingPass(BaseEntity):

    def __init__(
        self,
        id: BoardingPassId,
        issue_datetime: IssueDatetime,
        boarding_datetime: BoardingDatetime | None,
        current_status_id: CurrentStatusId,
        ticket_id: TicketId,
    ) -> None:

        self.id = id
        self.issue_datetime = issue_datetime
        self.boarding_datetime = boarding_datetime
        self.current_status_id = current_status_id
        self.ticket_id = ticket_id

    @property
    def id(self) -> BoardingPassId:
        return self._id

    @id.setter
    def id(self, value: BoardingPassId) -> None:
        if not isinstance(value, BoardingPassId.__value__):
            raise TypeError(f"The type of {value} is not UUID.")

        self._id = value

    @property
    def issue_datetime(self) -> IssueDatetime | None:
        return self._issue_datetime

    @issue_datetime.setter
    def issue_datetime(self, value: IssueDatetime | None) -> None:
        if not isinstance(value, IssueDatetime.__value__):
            raise TypeError(f"The type of {value} is not datetime.")

        self._issue_datetime = value

    @property
    def boarding_datetime(self) -> BoardingDatetime | None:
        return self._boarding_datetime

    @boarding_datetime.setter
    def boarding_datetime(self, value: BoardingDatetime | None) -> None:
        if value is not None and not isinstance(value, BoardingDatetime.__value__):
            raise TypeError(f"The type of {value} must be datetime or none.")

        self._boarding_datetime = value

    @property
    def current_status_id(self) -> CurrentStatusId:
        return self._current_status_id

    @current_status_id.setter
    def current_status_id(self, value: CurrentStatusId) -> None:
        if not isinstance(value, CurrentStatusId.__value__):
            raise TypeError(f"The type of {value} is not int.")

        if value <= 0:
            raise ValueError(f"The current status id can not be negative or zero.")

        self._current_status_id = value

    @property
    def ticket_id(self) -> TicketId:
        return self._ticket_id

    @ticket_id.setter
    def ticket_id(self, value: TicketId) -> None:
        if not isinstance(value, TicketId.__value__):
            raise TypeError(f"The type of {value} is not UUID.")

        self._ticket_id = value
