from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_repositories import (FakeDocumentRepository,
                                           FakePassengerRepository)


class FakeRegisterDocumentUoW:

    def __init__(self, db_manager: FakeDBManager) -> None:
        self.db_manager = db_manager
        self.passenger_repository = FakePassengerRepository()
        self.document_repository = FakeDocumentRepository()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        pass
