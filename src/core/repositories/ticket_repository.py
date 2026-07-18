from src.common import DBManager
from src.common.types import TicketRow
from src.entities import Ticket


class TicketRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_tickets(self, tickets: list[Ticket]) -> None:
        self.db_manager.insert_rows("tickets", tickets)

    def retrieve_tickets(self, limit: int = 5) -> list[Ticket]:
        query = "SELECT * FROM tickets ORDER BY id DESC LIMIT %s"

        results: list[TicketRow] = self.db_manager.retrieve_many_columns(
            query, (limit,)
        )

        if results:
            return [Ticket(*result) for result in results]

        return []
