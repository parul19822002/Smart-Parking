import time, sys, paho.mqtt.client as mqttClient

#10 ground sensors are assumed 
ground_sensor_count = 10
parking_slot_occupancy = [0] * ground_sensor_count
Connected = False
hq_address = "127.0.0.1"
port = 1883
request_topic = f'smartparking/findcarbyplatedetails/request'
response_topic = f'smartparking/findcarbyplatedetails/response'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")


def getPlateNumber(message):
    return message.payload.decode('utf-8').strip("\n").strip()


def getAllMatchingVehicle(plate_number):
    global plate_number_list
    result_dict = {}
    for x in plate_number_list:
        if plate_number in x:
            result_dict["Slot-" + str(plate_number_list.index(x))]= "Vehicle number - " + str(x)
    if (len(result_dict) ==0):
        return "Car not available"
    else:
        return result_dict


def on_message(client, userdata, message):
    if message.topic == request_topic:
        plate_number = getPlateNumber(message)
        plate_numbers = getAllMatchingVehicle(plate_number)
        client.publish(response_topic, str(plate_numbers))

#camera_sensor.txt contains car number plate details parked in the parking slot
#stepped through after every 5 sec
 
camera_name_client = "camera_sensor"
fp = open(sys.argv[1], 'r')  # open(f'../data/camera_sensor.txt',r)
client = mqttClient.Client(camera_name_client)  # create new instance
client.username_pw_set(username="arnot", password="arnot1");
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.connect(hq_address, port=port)  # connect to HQ
client.loop_start()  # start the loop
client.subscribe(request_topic)
try:
    while fp:
        line = fp.readline().strip("\n").strip()
        plate_number_list = line.split(' ')
        print(plate_number_list)
        time.sleep(5)
        if line == "":
            break
    fp.close()
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()

