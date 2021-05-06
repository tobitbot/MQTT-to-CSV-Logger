import paho.mqtt.client as mqtt
import csv
import sys
import argparse
import atexit
import time
from datetime import datetime

# Define some defaults
defaults = {
    "broker_IP": "localhost",
    "port": 1883,
    "keepalive": 60,
    "topic": "application/#",
    "logFile": "logFile.csv",
    "username": "",
    "password": ""
}

initialLog = False

# Handle user arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", help="MQTT-Broker Port")
ap.add_argument("-b", "--broker-IP", help="MQTT-Broker IP-Address")
ap.add_argument("-t", "--topic", help="MQTT topic")
ap.add_argument("-k", "--keepalive", help="Connection keepalive")
ap.add_argument("-l", "--logFile", help="CSV filename")
ap.add_argument("-u", "--username", help="username")
ap.add_argument("-P", "--password", help="password")

args = vars(ap.parse_args())


# If no arguments are given, guide the user thru them
if len(sys.argv) > 1 :
    # Merge user args and defaults
    for arg in args:
        if args[arg] != None:
            defaults[arg] = args[arg]
else :
    print("No arguments given, define them or use default by leaving the options empty")
    print("Defaults: " + str(defaults))

    # Merge user args and defaults
    for arg in defaults:
        value = input(arg + ": ")
        if len(value) == 0:
            continue
        else:
            defaults[arg] = value

print("Trying to connect with arguments: ")
print(str(defaults) + "\n")


def exit_handler():
    print("\nLogged MQTT traffic to log file: " + defaults["logFile"])
    print("Program exit in 3 seconds. Bye bye... \n")
    time.sleep(3)

atexit.register(exit_handler)

# Define MQTT functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker " + defaults["broker_IP"] + ":" + str(defaults["port"])
            + " on topic \"" + defaults["topic"] + "\" with code:" + str(rc))

        with open(defaults["logFile"], "a", newline="") as file:
            writer = csv.writer(file, quotechar="|", delimiter=";")
            writer.writerow([datetime.now(), defaults["topic"], "Connected to: " + defaults["broker_IP"] + ":" + str(defaults["port"]), ])
    else:
        print("Could not connect to to broker, code: " + str(rc))
    client.subscribe(str(defaults["topic"]))


def on_message(client, userdate, msg):
    data = [datetime.now(), msg.topic, msg.payload.decode("utf-8")]
    print(data)
    with open(defaults["logFile"], "a", newline="") as file:
        writer = csv.writer(file, quotechar="|", delimiter=";")
        writer.writerow(data)


def initConnection():
    try:
        # Init MQTT-Connection
        mqttc = mqtt.Client()
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        mqttc.connect(str(defaults["broker_IP"]), int(defaults["port"]), int(defaults["keepalive"]))

        if defaults["username"] != None or defaults["password"]!= None:
            mqttc.username_pw_set(str(defaults["username"]), str(defaults["password"]))

        print("Starting MQTT logging...")
        mqttc.loop_forever()

    except UnicodeDecodeError:
        print("Unicode Error. Connection again")
        initConnection()

    finally:
        print("Tschöö")

initConnection()
