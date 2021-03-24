import paho.mqtt.client as mqtt
import csv
import argparse
from datetime import datetime

# Define some defaults
defaults = {
    "broker": "localhost",
    "port": 1883,
    "keepalive": 60,
    "topic": "#",
    "logFile": "logFile.csv",
    "username": "",
    "password": ""
}

# Handle user arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", help="MQTT-Broker Port")
ap.add_argument("-b", "--broker", help="MQTT-Broker IP-Address")
ap.add_argument("-t", "--topic", help="MQTT topic")
ap.add_argument("-k", "--keepalive", help="Connection keepalive")
ap.add_argument("-l", "--logFile", help="CSV filename")
ap.add_argument("-u", "--username", help="username")
ap.add_argument("-P", "--password", help="password")

args = vars(ap.parse_args())

# Merge user args and defaults
for arg in args:
    if args[arg] != None:
        defaults[arg] = args[arg]


# Define MQTT functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker " + defaults["broker"] + ":" + str(defaults["port"])
            + " on topic \"" + defaults["topic"] + "\" with code:" + str(rc))
    else:
        print("Could not connect to to broker, code: " + str(rc))
    client.subscribe(str(defaults["topic"]))


def on_message(client, userdate, msg):
    data = [datetime.now(), msg.topic, msg.payload.decode("utf-8")]
    print(data)
    with open(defaults["logFile"], "a", newline="") as file:
        writer = csv.writer(file, quotechar="|", delimiter=";")
        writer.writerow(data)

# Init MQTT-Connection
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(str(defaults["broker"]), int(defaults["port"]), int(defaults["keepalive"]))

if defaults["username"] != None or defaults["password"]!= None:
    mqttc.username_pw_set(str(defaults["username"]), str(defaults["password"]))

print("Starting MQTT logging...")
mqttc.loop_forever()
