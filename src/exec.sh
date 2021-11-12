#!/bin/bash
# Start ground sensors


max=10

for (( i=1; i <= $max; ++i ))
do
	nohup python3 ground_sensor.py $i ../data/ground_sensor.txt & 
done

# Start camera sensor
nohup python3 camera_sensor.py ../data/camera_sensor.txt &
sleep 2
# Start Interface File
python3 interface.py
