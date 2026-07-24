from datetime import datetime

from src.common import DBManager
from src.common.types import AirplaneId, FlightHourCostUsd, RangeKm
from src.core.repositories.base_repository import BaseRepository
from src.entities import Airplane


class AirplaneRepository(BaseRepository[Airplane]):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__(
            db_manager,
            "airplanes",
            (
                "id",
                "tail_number",
                "manufacturer",
                "model",
                "capacity",
                "range_km",
                "flight_hour_cost_usd",
                "current_status_id",
            ),
            Airplane,
        )

    def retrieve_ranges_km_by_ids(
        self, airplane_ids: list[AirplaneId]
    ) -> list[RangeKm]:
        if not airplane_ids:
            return []

        placeholders = ",".join(["%s"] * len(airplane_ids))

        query = "SELECT range_km FROM airplanes WHERE id IN ({})".format(placeholders)

        results: list[RangeKm] = self.db_manager.retrieve_single_column(
            query, airplane_ids
        )

        return results

    def retrieve_flight_hour_costs_usd_by_ids(
        self, airplane_ids: list[AirplaneId]
    ) -> list[FlightHourCostUsd]:
        if not airplane_ids:
            return []

        placeholders = ",".join(["%s"] * len(airplane_ids))

        query = "SELECT flight_hour_cost_usd FROM airplanes WHERE id IN ({})".format(
            placeholders
        )

        results: list[FlightHourCostUsd] = self.db_manager.retrieve_single_column(
            query, airplane_ids
        )

        return results

    def retrieve_available_airplanes_ids(
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
