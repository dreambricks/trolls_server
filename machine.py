from flask import Blueprint
from udp_sender import UDPSender

machine = Blueprint('machine', __name__)

udp_sender = UDPSender()

gifts = 0


@machine.route('/bt_light/<string:isOn>', methods=['GET'])
def is_light_on(isOn):

    # is_on = true / false
    is_on = isOn

    return is_on


@machine.route('/bt_pressed')
def bt_pressed():
    udp_sender.send("bt_pressed")
    return 'button_pressed'


@machine.route('/dispensegift')
def dispense_gift():
    return 'gift_dispensed'


@machine.route('/increment_gifts')
def increment_gifts():
    global gifts
    gifts += 1
    return f"{gifts}"


@machine.route('/gifts')
def gift_dispensed():
    global gifts
    return f"{gifts}"


@machine.route('/working')
def working():
    answer = "yes"
    return answer
