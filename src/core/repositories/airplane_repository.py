from datetime import datetime

from src.common import DBManager
from src.common.types import (AirplaneId, AirplaneRow, FlightHourCostUsd,
                              RangeKm)
from src.entities import Airplane


class AirplaneRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def retrieve_airplanes(self, limit: int = 5) -> list[Airplane]:
        query = "SELECT id, tail_number, manufacturer, model, capacity, range_km, flight_hour_cost_usd, current_status_id FROM airplanes ORDER BY id DESC LIMIT %s"

        results: list[AirplaneRow] = self.db_manager.retrieve_many_columns(
            query, (limit,)
        )

        if results:
            return [Airplane(*result) for result in results]

        return []

    def retrieve_airplanes_by_id(self, airplanes_id: list[AirplaneId]) -> list[AirplaneId]:
        if not airplanes_id:
            return []
        
        placeholders = ",".join(["%s" * len(airplanes_id)])
        
        query = "SELECT id FROM airplanes WHERE id IN ({})".format(
            placeholders
        )

        results: list[AirplaneId] = self.db_manager.retrieve_single_column(
            query, airplanes_id
        )

        if results:
            return results

        return []

    def retrieve_range_km_by_id(self, airplanes_id: list[AirplaneId]) -> list[RangeKm]:
        if not airplanes_id:
            return []
        
        placeholders = ",".join(["%s" * len(airplanes_id)])

        query = "SELECT range_km FROM airplanes WHERE id IN ({})".format(
            placeholders
        )

        results: list[RangeKm] = self.db_manager.retrieve_single_column(
            query, airplanes_id
        )

        if results:
            return results

        return []

    def retrieve_flight_hour_cost_usd_by_id(
        self, airplanes_id: list[AirplaneId]
    ) -> list[FlightHourCostUsd]:
        if not airplanes_id:
            return []
        
        placeholders = ",".join(["%s" * len(airplanes_id)])

        query = "SELECT flight_hour_cost_usd FROM airplanes WHERE id IN ({})".format(
            placeholders
        )

        results: list[FlightHourCostUsd] = self.db_manager.retrieve_single_column(
            query, airplanes_id
        )

        if results:
            return results

        return []

    def retrieve_available_airplanes_id(
        self,
        range_km: RangeKm,
        scheduled_departure_datetime: datetime,
        scheduled_arrival_datetime: datetime,
    ) -> list[AirplaneId]:
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
                )
                """

        values = (
            range_km,
            scheduled_departure_datetime,
            scheduled_arrival_datetime,
            scheduled_departure_datetime,
            scheduled_arrival_datetime,
        )

        results: list[AirplaneId] = self.db_manager.retrieve_single_column(
            query, values
        )

        return results
