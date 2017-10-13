#### need to put your deviceID here
version = 0.1
deviceID = "energymon"
mqttclient = "mqtt.home.local"
import paho.mqtt.client as mqtt
import time
import MySQLdb
import mysqlinit


def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("particle/" + deviceID + "/#")
    client.publish("particle/status","energymon is alive, version" + str(version))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = str(msg.payload)
    topic = msg.topic
    if str(msg.topic) == "particle/" + str(deviceID) + "/sensors/watts":
        watts = float(msg.payload)
        print watts
        cursor.execute("""INSERT INTO energymon (watts) VALUES('%s')""" % (round(watts,2)))
        cnx.commit()
user = mysqlinit.user()
password = mysqlinit.password()
ipaddress = mysqlinit.get_lan_ip()
cnx = MySQLdb.connect(user=user, passwd=password, host='127.0.0.1', db='automation')
cursor=cnx.cursor()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttclient, 1883, 60)
client.loop_forever()
