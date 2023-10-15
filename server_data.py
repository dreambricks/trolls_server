from singleton import Singleton


class ServerData(metaclass=Singleton):

    def __init__(self):
        self.dispense = False
        self.button_light = False
        self.button_pressed = False
        self.is_machine_on = True
        self.running = True
        self.num_dispensed_gifts = 0

    def reset(self):
        self.dispense = False
        self.button_light = False
        self.button_pressed = False
        self.is_machine_on = True
        self.running = True
        self.num_dispensed_gifts = 0

