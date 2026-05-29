from src.core.repositories import TicketRepository
from src.core.validators import TicketValidator

class TicketManager:

    def __init__(self, ticket_validator: TicketValidator) -> None:
        self.ticket_validator = ticket_validator