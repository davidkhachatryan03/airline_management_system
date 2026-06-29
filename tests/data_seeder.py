import os, random
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from faker import Faker

from src.common import DBManager
from src.entities import AirplaneRetrieved, Booking, Document, Flight, Passenger, RouteRetrieved, Ticket

class DataSeeder:

    def __init__(self) -> None:
        self.faker = Faker()
    
    def execute(self, db_manager: DBManager) -> None:
        db_manager.cursor.execute("SET @user = 999")
        db_manager.execute_sql_file(os.path.join(os.getcwd(), "sql", "delete_data.sql"))
        self._execute_sql_files(db_manager)

        passengers: list[Passenger]
        document: list[Document]
        flights: list[Flight]

        passengers, documents = self._insert_passengers_and_documents(db_manager)
        flights = self._insert_flights(db_manager)

        query = """
                SELECT  a.capacity
                FROM    flights f
                JOIN    airplanes a
                ON      f.airplane_id = a.id
                WHERE   f.id = %s
                """
        
        bookings: list[Booking] 
        tickets: list[Ticket]
        
        bookings, tickets = self._insert_bookings_and_tickets(passengers, flights, db_manager)

    def _execute_sql_files(self, db_manager: DBManager) -> None:
        cwd: str = os.getcwd()
        sql_insert_files_route: str = os.path.join(cwd, "sql", "inserts")
        sql_insert_files: list[str] = sorted(os.listdir(sql_insert_files_route))

        for file in sql_insert_files:
            file_route: str = os.path.join(sql_insert_files_route, file)
            db_manager.execute_sql_file(file_route)

    def _insert_passengers_and_documents(self, db_manager: DBManager, cant=100) -> tuple[list[Passenger], list[Document]]:
        passengers: list[Passenger] = []
        documents: list[Document] = []
        
        for _ in range(cant):
            passenger = Passenger.new_passenger(
                full_name=self.faker.name(),
                birth_date=self.faker.date_between(start_date="-50y", end_date="-5y"),
                email=self.faker.email(),
                phone_number=str(self.faker.numerify(text="%#########"))
            )

            valid_from = self.faker.date_between(start_date=passenger.birth_date + timedelta(days=365))
            valid_until = valid_from + timedelta(days=1825)

            document = Document.new_document(
                document_number=self.faker.bothify(text="??########", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                valid_from=valid_from,
                valid_until=valid_until,
                issue_country=random.choices(["ARG", "ESP", "BRA", "ITA", "URY", "CHL", "USA"], weights=[40, 15, 15, 10, 10, 5, 5])[0],
                passenger_id=passenger.id,
                document_type_id=1
            )

            passengers.append(passenger)
            documents.append(document)
        
        db_manager.insert_rows("passengers", passengers)
        db_manager.insert_rows("documents", documents)

        return passengers, documents
    
    def _insert_flights(self, db_manager: DBManager, cant=100) -> list[Flight]:
        flights: list[Flight] = []
        routes: list[RouteRetrieved] = [RouteRetrieved(*route) for route in db_manager.retrieve("SELECT * FROM routes")]
        airplanes: list[AirplaneRetrieved] = [AirplaneRetrieved(*airplane) for airplane in db_manager.retrieve("SELECT * FROM airplanes")]

        for _ in range(cant):
            flag = True

            while flag:
                route: RouteRetrieved = random.choice(routes)
                airplane: AirplaneRetrieved = random.choice(airplanes)

                if route.distance_km < airplane.range_km:
                    flag = False

            scheduled_departure_datetime: datetime = self.faker.date_time_between(start_date="+30d", end_date="+180d")
            scheduled_arrival_datetime: datetime = scheduled_departure_datetime + timedelta(minutes=route.duration_min)

            operating_cost_usd: Decimal = airplane.flight_hour_cost_usd * (Decimal(route.duration_min) / Decimal("60")).quantize(Decimal("0.01"), ROUND_HALF_UP)

            flight = Flight.new_flight(
                scheduled_departure_datetime=scheduled_departure_datetime,
                scheduled_arrival_datetime=scheduled_arrival_datetime,
                operating_cost_usd=operating_cost_usd,
                route_id=route.id,
                airplane_id=airplane.id
            )

            flights.append(flight)
        
        db_manager.insert_rows("flights", flights)

        return flights

    def _insert_bookings_and_tickets(self, passengers: list[Passenger], flights: list[Flight], db_manager: DBManager) -> tuple[list[Booking], list[Ticket]]:
        bookings: list[Booking] = []
        tickets: list[Ticket] = []

        query = """
                SELECT  a.capacity
                FROM    flights f
                JOIN    airplanes a
                ON      f.airplane_id = a.id
                WHERE   f.id = %s
                """
        
        capacity_per_flight: dict[UUID, int] = {flight.id: db_manager.retrieve(query, (flight.id,))[0] for flight in flights}
        
        for passenger in passengers:
            flight: Flight = random.choice(flights)

            if capacity_per_flight[flight.id] > 0:
                booking = Booking.new_booking(flights, len(passengers))
                ticket = Ticket.new_ticket(
                    paid_amount_usd=flight.base_price_usd,
                    booking_id=booking.id,
                    flight_id=flight.id,
                    passenger_id=passenger.id
                )

                bookings.append(booking)
                tickets.append(ticket)
        
        db_manager.insert_rows("bookings", bookings)
        db_manager.insert_rows("tickets", tickets)

        return bookings, tickets