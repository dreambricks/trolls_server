import time
import serial
from parameters import *
import threading
from server_data import ServerData

from singleton import Singleton
from udp_sender import UDPSender


class ArduinoControllerThreadObject(metaclass=Singleton):

    def __init__(self):
        self.thread = None

    def start_arduino_thread(self):
        # start the arduino thread
        print("Starting Arduino Thread")
        self.thread = ArduinoControllerThread(1, "ArduinoController")
        self.thread.start()

    def get_thread(self):
        if self.thread is None:
            self.start_arduino_thread()
        return self.thread

class ArduinoControllerThread(threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.arduino = serial.Serial(port=ARDUINO_PORT, baudrate=ARDUINO_SPEED, timeout=.5)
        sd = ServerData()
        self.prev_light_state = not sd.button_light

    def run(self):
        print("Starting " + self.name)
        self.pool_arduino()
        print("Exiting " + self.name)

    def pool_arduino(self):
        sd = ServerData()
        while sd.running:
            if sd.dispense:
                print('dispense!')
                sd.dispense = False
                self.dispense()

            if self.prev_light_state != sd.button_light:
                self.prev_light_state = sd.button_light
                if sd.button_light:
                    print('turn button light on!')
                    self.turn_button_light_on()
                else:
                    print('turn button light off!')
                    self.turn_button_light_off()

            if self.arduino.in_waiting > 0:
                data = self.arduino.readline()
                if len(data) > 0:
                    if data == b'pressed\r\n':
                        print(f"received from arduino: <{data}>")
                        #sd.button_pressed = True
                        udp_sender = UDPSender()
                        udp_sender.send("bt_pressed")

            time.sleep(.05)
            #print('pool arduino', sd.dispense)

    def dispense(self):
        self.send_vending_command(1)

    def turn_button_light_on(self):
        self.send_vending_command(2)

    def turn_button_light_off(self):
        self.send_vending_command(3)

    def send_vending_command(self, cmd):
        cmd_str = f"{cmd}\n"
        print(cmd_str)
        self.arduino.write(bytes(cmd_str, 'utf-8'))
        time.sleep(0.05)
        #data = self.arduino.readline()
        #print(f"received from arduino: <{data}>")


def test_arduino():
    arduino = serial.Serial(port='COM13', baudrate=9600, timeout=.1)

    def write_read(x):
        arduino.write(bytes(f"{x}\n", 'utf-8'))
        time.sleep(0.05)
        data = arduino.readline()
        return data

    while True:
        num = input("Enter a number: ")  # Taking input from user
        value = write_read(num)
        print(value)  # printing the value


if __name__ == "__main__":
    sd = ServerData()

    #test_arduino()
    thread1 = ArduinoControllerThread(1, "ArduinoController")
    thread1.start()

    while True:
        num = input("Digite Enter")
        sd.dispense = True
        time.sleep(0.5)
        #print(sd.dispense)

