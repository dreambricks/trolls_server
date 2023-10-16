from flask import Blueprint
from udp_sender import UDPSender
from server_data import ServerData
from mongo_setup import db

machine = Blueprint('machine', __name__)

udp_sender = UDPSender()


@machine.route('/bt_light/<string:is_on>', methods=['GET'])
def turn_light(is_on):

    # is_on = true / false
    sd = ServerData()
    sd.button_light = (is_on == "true")
    sd.button_pressed = False

    return is_on


@machine.route('/bt_pressed')
def bt_pressed():
    sd = ServerData()
    if sd.button_pressed:
        sd.button_pressed = False
        udp_sender.send("bt_pressed")

        return 'button_pressed'

    return 'button_not_pressed'


@machine.route('/dispensegift')
def dispense_gift():
    sd = ServerData()
    sd.num_dispensed_gifts += 1
    collection = db['data']

    first_document = collection.find_one()
    if first_document:
        query = {"_id": first_document["_id"]}
        entry = {"$set": {"counter": sd.num_dispensed_gifts}}
        collection.update_one(query, entry)
    else:
        entry = {"counter": sd.num_dispensed_gifts}
        collection.insert_one(entry)


    sd.dispense = True
    return f"gifts_dispensed: {sd.num_dispensed_gifts}"


@machine.route('/refill')
def refill():
    sd = ServerData()
    sd.num_dispensed_gifts = 0
    collection = db['data']

    first_document = collection.find_one()

    if first_document:
        query = {"_id": first_document["_id"]}
        entry = {"$set": {"counter": sd.num_dispensed_gifts}}
        collection.update_one(query, entry)
    else:
        entry = {"counter": sd.num_dispensed_gifts}
        collection.insert_one(entry)

    return f"{sd.num_dispensed_gifts}"


@machine.route('/gifts')
def gift_dispensed():
    sd = ServerData()
    return f"{sd.num_dispensed_gifts}"


@machine.route('/turn_on')
def turn_on():
    sd = ServerData()
    sd.button_light = True
    return 'turned_on'


@machine.route('/turn_off')
def turn_off():
    sd = ServerData()
    sd.button_light = False
    return 'turned_off'


@machine.route('/working')
def working():
    sd = ServerData()
    return "yes" if sd.is_machine_on else "no"
