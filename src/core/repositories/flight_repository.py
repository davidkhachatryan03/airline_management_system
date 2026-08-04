from src.common import DBManager
from src.common.types import FlightId
from src.core.repositories.base_repository import BaseRepository
from src.entities import Flight


class FlightRepository(BaseRepository[Flight]):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__(
            db_manager=db_manager,
            table_name="flights",
            columns=(
                "id",
                "scheduled_departure_datetime",
                "scheduled_arrival_datetime",
                "actual_departure_datetime",
                "actual_arrival_datetime",
                "operating_cost_usd",
                "base_price_usd",
                "current_status_id",
                "route_id",
                "airplane_id",
            ),
            entity=Flight,
            identity_key=("scheduled_departure_datetime", "route_id"),
            uuid_columns=tuple("id"),
        )

    def retrieve_seats_available_per_flight(
        self, flights_id: list[FlightId]
    ) -> dict[FlightId, int]:
        if not flights_id:
            return {}

        placeholders = ",".join(["%s"] * len(flights_id))

        query = """
                SELECT      f.id, 
                            (a.capacity - COUNT(t.id)) AS asientos_disponibles
                FROM        flights f
                JOIN        airplanes a 
                ON          f.airplane_id = a.id
                LEFT JOIN   tickets t 
                ON          t.flight_id = f.id 
                AND         t.current_status_id = 1 
                WHERE       f.id 
                IN          ({}) 
                AND         f.current_status_id = 1
                GROUP BY    f.id, 
                            a.capacity;
                """.format(placeholders)

        values: list[FlightId] = [self._to_db_value(id) for id in flights_id]

        results: list[tuple[FlightId, int]] = self.db_manager.execute_read(
            query, values
        )

        parsed_results = [
            (self._from_db_value(flight_id), seats_count)
            for flight_id, seats_count in results
        ]

        result_dict: dict[FlightId, int] = {}
        for row in parsed_results:
            result_dict[row[0]] = row[1]

        return result_dict
