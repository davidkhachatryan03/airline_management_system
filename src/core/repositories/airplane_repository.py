from datetime import datetime
from uuid import UUID

from src.common import DBManager
from src.common.exceptions import UnavailableAirplane
from src.entities import Airplane

class AirplaneRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def retrieve_airplanes(self, limit: int = 5) -> list[Airplane]:
        query = "SELECT * FROM airplanes ORDER BY id DESC LIMIT %s"

        results: list[tuple] = self.db_manager.retrieve(query, (limit,))
        
        if results:
            return [Airplane(*result) for result in results]
        
        return []
    
    def retrieve_airplane_range_km_by_id(self, airplane_id: UUID) -> int:
        query = "SELECT range_km from airplanes WHERE id = %s"

        values = (airplane_id,)

        
    
    def retrieve_available_airplanes_id(self, scheduled_departure_datetime: datetime, scheduled_arrival_datetime: datetime) -> list[UUID]:
        query = """
                SELECT  a.id
                FROM    airplanes a
                JOIN    airplane_statuses ast 
                ON      a.current_status_id = ast.id
                WHERE   ast.description = 'Active' 
                AND     a.range_km >= %s 
                
                AND NOT EXISTS (
                    SELECT  1 
                    FROM    flights f
                    JOIN    flight_statuses fs 
                    ON      f.current_status_id = fs.id
                    WHERE   f.airplane_id = a.id
                    AND     fs.description != 'Cancelled'
                    AND     %s < f.scheduled_arrival_datetime
                    AND     %s > f.scheduled_departure_datetime
                )
                    
                AND NOT EXISTS (
                    SELECT  1 
                    FROM    scheduled_maintenances sm
                    WHERE   sm.airplane_id = a.id
                    AND     %s < sm.scheduled_end_datetime
                    AND     %s > sm.scheduled_start_datetime
                );
                """
        
        values = (scheduled_departure_datetime, scheduled_arrival_datetime)

        results: list[UUID] = self.db_manager.retrieve(query, values)

        return results