from faker import Faker
from src.common import DBManager

class DataGenerator:
    
    def __init__(self) -> None:
        self.fake = Faker("es_AR")
        self.db_manager = DBManager()
