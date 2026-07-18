from src.entities import Ticket


class FakeTicketRepository:

    def __init__(self) -> None:
        self.tickets: list[Ticket] = []

    def insert_tickets(self, tickets: list[Ticket]) -> None:
        self.tickets.extend(tickets)