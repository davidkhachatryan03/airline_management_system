import random
from datetime import date, datetime, timedelta
from decimal import Decimal

from faker import Faker

from src.common.types import (
    AirplaneId,
    BookingId,
    DocumentId,
    DocumentTypeId,
    FlightId,
    PassengerId,
    RouteId,
    TicketId,
)
from src.entities import Airplane, Booking, Document, Flight, Passenger, Route, Ticket

AIRPLANE_MODELS = [
    {
        "manufacturer": "Gulfstream",
        "model": "G650ER",
        "capacity": 18,
        "range_km": 13890,
        "flight_hour_cost_usd": Decimal("15500.00"),
    },
    {
        "manufacturer": "Bombardier",
        "model": "Global 7500",
        "capacity": 19,
        "range_km": 14260,
        "flight_hour_cost_usd": Decimal("16200.00"),
    },
    {
        "manufacturer": "Dassault",
        "model": "Falcon 8X",
        "capacity": 14,
        "range_km": 11945,
        "flight_hour_cost_usd": Decimal("14800.50"),
    },
    {
        "manufacturer": "Cessna",
        "model": "Citation X+",
        "capacity": 12,
        "range_km": 6400,
        "flight_hour_cost_usd": Decimal("9500.00"),
    },
    {
        "manufacturer": "Bombardier",
        "model": "Challenger 350",
        "capacity": 9,
        "range_km": 5900,
        "flight_hour_cost_usd": Decimal("8700.00"),
    },
    {
        "manufacturer": "Cessna",
        "model": "Citation CJ4",
        "capacity": 10,
        "range_km": 4010,
        "flight_hour_cost_usd": Decimal("5600.00"),
    },
    {
        "manufacturer": "Embraer",
        "model": "Phenom 300E",
        "capacity": 10,
        "range_km": 3650,
        "flight_hour_cost_usd": Decimal("5200.00"),
    },
    {
        "manufacturer": "Learjet",
        "model": "75 Liberty",
        "capacity": 8,
        "range_km": 3850,
        "flight_hour_cost_usd": Decimal("5100.00"),
    },
    {
        "manufacturer": "Pilatus",
        "model": "PC-24",
        "capacity": 11,
        "range_km": 3704,
        "flight_hour_cost_usd": Decimal("4900.00"),
    },
    {
        "manufacturer": "Honda Aircraft",
        "model": "HondaJet Elite",
        "capacity": 5,
        "range_km": 2661,
        "flight_hour_cost_usd": Decimal("3800.00"),
    },
]


class FakeStorage:

    def __init__(self) -> None:
        self.airplanes: dict[AirplaneId, Airplane] = {}
        self.bookings: dict[BookingId, Booking] = {}
        self.documents: dict[DocumentId, Document] = {}
        self.passengers: dict[PassengerId, Passenger] = {}
        self.flights: dict[FlightId, Flight] = {}
        self.tickets: dict[TicketId, Ticket] = {}
        self.routes: dict[RouteId, Route] = {
            1: Route(
                id=1,
                flight_number="AR1240",
                origin="AEP",
                destination="COR",
                distance_km=646,
                duration_min=85,
            ),
            2: Route(
                id=2,
                flight_number="AR1241",
                origin="COR",
                destination="AEP",
                distance_km=646,
                duration_min=85,
            ),
            3: Route(
                id=3,
                flight_number="AR1432",
                origin="AEP",
                destination="MDZ",
                distance_km=984,
                duration_min=110,
            ),
            4: Route(
                id=4,
                flight_number="AR1433",
                origin="MDZ",
                destination="AEP",
                distance_km=984,
                duration_min=110,
            ),
            5: Route(
                id=5,
                flight_number="AR1870",
                origin="AEP",
                destination="BRC",
                distance_km=1316,
                duration_min=140,
            ),
            6: Route(
                id=6,
                flight_number="AR1871",
                origin="BRC",
                destination="AEP",
                distance_km=1316,
                duration_min=140,
            ),
            7: Route(
                id=7,
                flight_number="AR2840",
                origin="AEP",
                destination="USH",
                distance_km=2380,
                duration_min=215,
            ),
            8: Route(
                id=8,
                flight_number="AR2841",
                origin="USH",
                destination="AEP",
                distance_km=2380,
                duration_min=215,
            ),
            9: Route(
                id=9,
                flight_number="AR1530",
                origin="AEP",
                destination="IGR",
                distance_km=1050,
                duration_min=105,
            ),
            10: Route(
                id=10,
                flight_number="AR1531",
                origin="IGR",
                destination="AEP",
                distance_km=1050,
                duration_min=105,
            ),
            11: Route(
                id=11,
                flight_number="LA2350",
                origin="SCL",
                destination="AEP",
                distance_km=1140,
                duration_min=130,
            ),
            12: Route(
                id=12,
                flight_number="LA2351",
                origin="AEP",
                destination="SCL",
                distance_km=1140,
                duration_min=130,
            ),
            13: Route(
                id=13,
                flight_number="LA3122",
                origin="AEP",
                destination="GRU",
                distance_km=1700,
                duration_min=165,
            ),
            14: Route(
                id=14,
                flight_number="LA3123",
                origin="GRU",
                destination="AEP",
                distance_km=1700,
                duration_min=165,
            ),
            15: Route(
                id=15,
                flight_number="LA4500",
                origin="LIM",
                destination="AEP",
                distance_km=3150,
                duration_min=245,
            ),
            16: Route(
                id=16,
                flight_number="LA4501",
                origin="AEP",
                destination="LIM",
                distance_km=3150,
                duration_min=245,
            ),
            17: Route(
                id=17,
                flight_number="AV9340",
                origin="BOG",
                destination="AEP",
                distance_km=4600,
                duration_min=370,
            ),
            18: Route(
                id=18,
                flight_number="AV9341",
                origin="AEP",
                destination="BOG",
                distance_km=4600,
                duration_min=370,
            ),
            19: Route(
                id=19,
                flight_number="AF7652",
                origin="GIG",
                destination="AEP",
                distance_km=1980,
                duration_min=190,
            ),
            20: Route(
                id=20,
                flight_number="AF7653",
                origin="AEP",
                destination="GIG",
                distance_km=1980,
                duration_min=190,
            ),
            21: Route(
                id=21,
                flight_number="AA1142",
                origin="MIA",
                destination="AEP",
                distance_km=7100,
                duration_min=540,
            ),
            22: Route(
                id=22,
                flight_number="AA1143",
                origin="AEP",
                destination="MIA",
                distance_km=7100,
                duration_min=540,
            ),
            23: Route(
                id=23,
                flight_number="IB3106",
                origin="AEP",
                destination="MAD",
                distance_km=10050,
                duration_min=750,
            ),
            24: Route(
                id=24,
                flight_number="IB3107",
                origin="MAD",
                destination="AEP",
                distance_km=10050,
                duration_min=750,
            ),
            25: Route(
                id=25,
                flight_number="LH0120",
                origin="FRA",
                destination="AEP",
                distance_km=11500,
                duration_min=820,
            ),
            26: Route(
                id=26,
                flight_number="LH0121",
                origin="AEP",
                destination="FRA",
                distance_km=11500,
                duration_min=820,
            ),
            27: Route(
                id=27,
                flight_number="AM0120",
                origin="MEX",
                destination="AEP",
                distance_km=7400,
                duration_min=580,
            ),
            28: Route(
                id=28,
                flight_number="AM0121",
                origin="AEP",
                destination="MEX",
                distance_km=7400,
                duration_min=580,
            ),
            29: Route(
                id=29,
                flight_number="AF0412",
                origin="AEP",
                destination="CDG",
                distance_km=11100,
                duration_min=790,
            ),
            30: Route(
                id=30,
                flight_number="AF0413",
                origin="CDG",
                destination="AEP",
                distance_km=11100,
                duration_min=790,
            ),
        }


class DataSeeder:

    def __init__(self, storage: FakeStorage) -> None:
        self.faker = Faker("es_AR")
        self.storage = storage
        self.countries = ["ARG", "BRA", "CHL", "COL", "FRA", "MEX", "URY", "USA"]

    def passengers(self, cant: int = 100) -> list[Passenger]:
        passengers_created: list[Passenger] = []

        for _ in range(cant):
            passengers_created.append(
                Passenger.new_passenger(
                    full_name=self.faker.full_name(),
                    birth_date=self.faker.date_this_century(),
                    email=self.faker.email(),
                    phone_number=self.faker.phone_number(),
                )
            )

        for passenger in passengers_created:
            self.storage.passengers[passenger.id] = passenger

        return passengers_created

    def documents(
        self, passenger_ids: list[PassengerId], document_type_id: DocumentTypeId
    ) -> list[Document]:
        documents_created: list[Document] = []

        passengers_requested: list[Passenger] = [
            self.storage.passengers[passenger_id] for passenger_id in passenger_ids
        ]

        for passenger in passengers_requested:
            birth_date, valid_from, valid_until = self.faker.passport_dates(
                birthday=passenger.birth_date
            )
            documents_created.append(
                Document.new_document(
                    document_number=self.faker.passport_number(),
                    valid_from=date.fromisoformat(valid_from),
                    valid_until=date.fromisoformat(valid_until),
                    issue_country=random.choice(self.countries),
                    passenger_id=passenger.id,
                    document_type_id=document_type_id,
                )
            )

        for document in documents_created:
            self.storage.documents[document.id] = document

        return documents_created

    def airplanes(self, cant: int = 10) -> list[Airplane]:
        airplanes_created: list[Airplane] = []

        try:
            starting_id: int = max(self.storage.airplanes.keys()) + 1
        except:
            starting_id = 1

        for _ in range(cant):
            base_model = random.choice(AIRPLANE_MODELS)

            prefix = random.choice(["LV-", "N-"])
            if prefix == "LV-":
                tail_number = f"LV-{self.faker.lexify(text='???').upper()}"
            else:
                tail_number = f"N-{self.faker.numerify(text='###')}{self.faker.lexify(text='??').upper()}"

            status_id = random.choices([1, 2], weights=[0.9, 0.1])[0]

            airplanes_created.append(
                Airplane(
                    id=starting_id,
                    tail_number=tail_number,
                    manufacturer=base_model["manufacturer"],
                    model=base_model["model"],
                    capacity=base_model["capacity"],
                    range_km=base_model["range_km"],
                    flight_hour_cost_usd=base_model["flight_hour_cost_usd"],
                    current_status_id=status_id,
                )
            )

            starting_id += 1

        for airplane in airplanes_created:
            self.storage.airplanes[airplane.id] = airplane

        return airplanes_created

    def flights(
        self, route_ids: list[RouteId], airplane_id: AirplaneId, cant: int = 10
    ) -> list[Flight]:
        flights_created: list[Flight] = []

        airplane: Airplane = self.storage.airplanes[airplane_id]
        routes: list[Route] = [self.storage.routes[route_id] for route_id in route_ids]

        for _ in range(cant):
            route = random.choice(routes)
            start_datetime: datetime = self.faker.date_time_between(
                start_date=datetime(2025, 1, 1), end_date=datetime.today()
            )
            flights_created.append(
                Flight.new_flight(
                    scheduled_departure_datetime=start_datetime,
                    scheduled_arrival_datetime=start_datetime
                    + timedelta(minutes=route.duration_min),
                    operating_cost_usd=Flight._calculate_operating_cost_usd(
                        flight_hour_cost_usd=airplane.flight_hour_cost_usd,
                        duration_min=route.duration_min,
                    ),
                    route_id=route.id,
                    airplane_id=airplane_id,
                )
            )

        for flight in flights_created:
            self.storage.flights[flight.id] = flight

        return flights_created

    def booking_and_tickets(
        self, flight_ids: list[FlightId], passenger_ids: list[PassengerId]
    ) -> tuple[Booking, list[Ticket]]:
        tickets_created: list[Ticket] = []

        flights: list[Flight] = [
            self.storage.flights[flight_id] for flight_id in flight_ids
        ]
        passengers: list[Passenger] = [
            self.storage.passengers[passenger_id] for passenger_id in passenger_ids
        ]

        booking_created = Booking.new_booking(
            flights_base_prices=[flight.base_price_usd for flight in flights],
            number_of_passengers=len(passengers),
        )

        for flight in flights:
            for passenger in passengers:
                tickets_created.append(
                    Ticket.new_ticket(
                        paid_amount_usd=flight.base_price_usd,
                        booking_id=booking_created.id,
                        flight_id=flight.id,
                        passenger_id=passenger.id,
                    )
                )

        self.storage.bookings[booking_created.id] = booking_created

        for ticket in tickets_created:
            self.storage.tickets[ticket.id] = ticket

        return booking_created, tickets_created
