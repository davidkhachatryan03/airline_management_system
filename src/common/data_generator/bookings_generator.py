from src.common.data_generator.data_generator import DataGenerator
from src.entities import Ticket, Flight, Booking
import string, random

class BookingsGenerator(DataGenerator):

    def __init__(self) -> None:
        super().__init__()
