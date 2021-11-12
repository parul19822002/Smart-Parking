import ast, math, sys, time, paho.mqtt.client as mqttClient
from datetime import datetime

IsSlotOccupied=0
Connected = False
ip_address = "127.0.0.1"
port = 1883

# on_connect method for the MQTT client
def on_connect(client, userdata, flags, rc):
    #if rc == 0 then connection is succesful
    if rc == 0:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Connected to broker")
        global Connected # Use global variable
        Connected = True # Signal connection
    else:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Connection failed Return Code : {rc}")


# the ground sensor id 1-10
parking_sensor_id = int(sys.argv[1]) 

slot_name = f"slot-{parking_sensor_id}"

sensor_data_file = sys.argv[2]

client = mqttClient.Client(slot_name)  # create new instance
client.username_pw_set(username="arnot", password="arnot1");
client.on_connect = on_connect  # attach function to callback
print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Connected Ground sensor ID is  ****{slot_name}****")

client.connect(ip_address, port=port)  # connect to mqtt 
client.loop_start()  # start the loop
slot_topic = f"smartparking/groundsensor/{slot_name}"
with open(sensor_data_file, 'r') as sensor_data:
    senser_file_data = sensor_data.readlines()


#Reads sensor file line by line.Taking a 5 second pause in between.
#Each line in the data file takes 10 ID's.
#Each numeral indicates the sensor status specific to that slot id
#<sensor-status1> <senssor-status2> <sensor-status-3>
#we just extract the sensor status of that specific slotID and publish it to 
#all the subscribers 

#while 1:
    for each_line in senser_file_data:
        sensor_status = int(each_line.split()[parking_sensor_id-1])
        client.publish(slot_topic, sensor_status)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {parking_sensor_id} is of status {sensor_status}")
        time.sleep(5)
print(f"exit id {parking_sensor_id}")


