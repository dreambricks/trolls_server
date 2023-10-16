from singleton import Singleton
from mongo_setup import db


class ServerData(metaclass=Singleton):

    def __init__(self):
        self.dispense = False
        self.button_light = False
        self.button_pressed = False
        self.is_machine_on = True
        self.running = True
        self.num_dispensed_gifts = self.get_counter()

    def reset(self):
        self.dispense = False
        self.button_light = False
        self.button_pressed = False
        self.is_machine_on = True
        self.running = True
        self.num_dispensed_gifts = 0

    def get_counter(self):
        collection = db['data']
        first_document = collection.find_one()
        if first_document and 'counter' in first_document:
            return first_document['counter']
        else:
            return 0

