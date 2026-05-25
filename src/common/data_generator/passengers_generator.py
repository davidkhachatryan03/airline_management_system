from src.common.data_generator.data_generator import DataGenerator
import uuid6, random
from src.entities import Passenger

class PassengersGenerator(DataGenerator):
    
    def __init__(self) -> None:
        super().__init__()

    def generate_passengers(self, n=100) -> list[Passenger]:
        passengers: list[Passenger] = []

        for _ in range(n):
            passenger = Passenger(
                id=uuid6.uuid7(),
                full_name=self.fake.full_name(),
                email=self.fake.email(),
                phone_number=int(self.fake.numerify("11%#######")),
                is_blacklisted=random.choices([True,False], weights=[10, 90])[0],
                is_vip=random.choices([True,False], weights=[10, 90])[0]
            )

            passengers.append(passenger)
        
        return passengers