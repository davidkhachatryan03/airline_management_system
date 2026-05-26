from src.core.repositories import TicketRepository

class TicketValidator:

    def __init__(self, ticket_repository: TicketRepository) -> None:
        self.ticket_repository = ticket_repository