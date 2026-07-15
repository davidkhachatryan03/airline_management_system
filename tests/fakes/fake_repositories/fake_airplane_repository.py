from src.entities import Airplane

class FakeAirplaneRepository:

    def __init__(self) -> None:
        self.airplanes: list[Airplane] = []

    def insert_airplane(self, airplane: Airplane) -> None:
        self.airplanes.append(airplane)