import uuid6, random
from src.entities import Passenger, Document
from src.common.data_generator.data_generator import DataGenerator

class DocumentsGenerator(DataGenerator):

    def __init__(self) -> None:
        super().__init__()
    
    def generate_documents(self, passengers: list[Passenger]) -> list[Document]:
        documents: list[Document] = []

        for passenger in passengers:
            document = Document(
                id=uuid6.uuid7(),
                document_number=self.fake.bothify("??######"),
                valid_from=self.fake.date_between(start_date="-5y", end_date="-4y"),
                valid_until=self.fake.date_between(start_date="+5y", end_date="+10y"),
                issue_country=random.choices(["ARG","USA","ESP","BRA","CHL"], weights=[80,10,3,3,4])[0],
                passenger_id=passenger.id,
                document_type_id=random.choices([1,2,3], weights=[10,85,5])[0]
            )

            documents.append(document)
        
        return documents