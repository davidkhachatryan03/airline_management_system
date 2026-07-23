from src.common import DBManager
from src.common.types import DocumentIdentityKey, PassengerId, PassengerRow
from src.entities import Passenger


class PassengerRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_passengers(self, passengers: list[Passenger]) -> None:
        self.db_manager.insert_rows("passengers", passengers)

    def retrieve_passengers_by_ids(
        self, passenger_ids: list[PassengerId]
    ) -> list[Passenger]:
        if not passenger_ids:
            return []

        placeholders = ",".join(["%s"] * len(passenger_ids))

        query = """
                SELECT  id, 
                        full_name, 
                        birth_date, 
                        email,
                        phone_number,
                        is_blacklisted,
                        is_vip
                FROM    passengers
                WHERE   id IN ({})
                """.format(placeholders)

        results: list[PassengerRow] = self.db_manager.retrieve_many_columns(
            query, passenger_ids
        )

        if results:
            return [Passenger(*row) for row in results]

        return []

    def retrieve_passengers_by_documents(
        self, document_identity_keys: list[DocumentIdentityKey]
    ) -> list[Passenger]:
        if not document_identity_keys:
            return []

        placeholders = ",".join(
            ["(" + ",".join(["%s"] * len(document_identity_keys[0])) + ")"]
            * len(document_identity_keys)
        )

        query = """
                SELECT  p.id, 
                        p.full_name, 
                        p.birth_date, 
                        p.email,
                        p.phone_number,
                        p.is_blacklisted,
                        p.is_vip
                FROM    passengers p
                JOIN    documents d
                ON      p.id = d.passenger_id
                WHERE   (d.document_number, d.issue_country) IN ({})
                """.format(placeholders)

        document_identity_keys_plain = [
            value for identity_key in document_identity_keys for value in identity_key
        ]

        results: list[PassengerRow] = self.db_manager.retrieve_many_columns(
            query, document_identity_keys_plain
        )

        if results:
            return [Passenger(*row) for row in results]

        return []

    def retrieve_passengers(self, limit: int = 5) -> list[Passenger]:
        query = """
                SELECT      id, 
                            full_name, 
                            birth_date, 
                            email,
                            phone_number,
                            is_blacklisted,
                            is_vip
                FROM        passengers 
                ORDER BY    id DESC 
                LIMIT       %s
                """

        results: list[PassengerRow] = self.db_manager.retrieve_many_columns(
            query, (limit,)
        )

        if results:
            return [Passenger(*result) for result in results]

        return []
