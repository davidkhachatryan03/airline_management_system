from src.common import DBManager
from src.common.types import DocumentIdentityKey, PassengerRow
from src.core.repositories.base_repository import BaseRepository
from src.entities import Passenger


class PassengerRepository(BaseRepository[Passenger]):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__(
            db_manager=db_manager,
            table_name="passengers",
            columns=(
                "id",
                "full_name",
                "birth_date",
                "email",
                "phone_number",
                "is_blacklisted",
                "is_vip",
            ),
            entity=Passenger,
            uuid_columns=tuple("id"),
        )

    def retrieve_by_documents(
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

        results: list[PassengerRow] = self.db_manager.execute_read(
            query, document_identity_keys_plain
        )

        parsed_results: list[PassengerRow] = [
            (self._from_db_value(row[0]), *row[1:]) for row in results
        ]

        return [Passenger(*result) for result in parsed_results]
