from src.common import DBManager
from src.entities import Ticket

class TicketRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
    
    def retrieve_tickets(self, limit: int = 5) -> list[Ticket]:
        query = "SELECT * FROM passengers ORDER BY id DESC LIMIT %s"

        results: list[tuple] = self.db_manager.retrieve(query, (limit,))
        
        if results:
            return [Ticket(*result) for result in results]
        
        return []

    def insert_tickets(self, tickets: list[Ticket]) -> None:
        self.db_manager.insert_rows("tickets", tickets)