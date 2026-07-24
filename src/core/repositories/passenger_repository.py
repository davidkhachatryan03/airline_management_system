from src.common import DBManager
from src.common.types import DocumentIdentityKey, PassengerId, PassengerRow
from src.core.repositories.base_repository import BaseRepository
from src.entities import Passenger


class PassengerRepository(BaseRepository[Passenger]):

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
        super().__init__(
            db_manager,
            "passengers",
            (
                "id",
                "full_name",
                "birth_date",
                "email",
                "phone_number",
                "is_blacklisted",
                "is_vip",
            ),
            Passenger,
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

        results: list[PassengerRow] = self.db_manager.retrieve_many_columns(
            query, document_identity_keys_plain
        )

        return [Passenger(*row) for row in results]
