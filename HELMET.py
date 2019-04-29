#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Python example script showing proper use of the Cisco Sample Code header.
Copyright (c) {{current_year}} Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


from __future__ import absolute_import, division, print_function

__author__ = "Iván Santa <isantara@cisco.com>"
__contributors__ = [
    "Daniel Tobar <dtobar@cisco.com>",
    "Alejandro Ortiz <aleortiz@cisco.com>",
]
__copyright__ = "Copyright (c) {{current_year}} Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


#Libraries
import requests
import RPi.GPIO as GPIO
import Adafruit_DHT
from time import sleep
import serial
import json
import urllib3


#RASPBERRY PI PINOUT CONFIGURATION
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Gas Sensor
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Panic Button
GPIO.setup(18, GPIO.OUT)						   #Gas Alerting Led
GPIO.setup(25, GPIO.OUT)						   #Gas Alerting Buzzer
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #LDR Sensor (check if helmet is used)
GPIO.output(18,0)								  #Gas Alerting Led Off
GPIO.output(25,0)								  #Gas Alerting Buzzer Off

#IOX VARIABLES
iox_ip = "10.42.2.2"
iox_port = "8443"
iox_token = "26a5c87c-c86a-433a-a440-72ba807ff426"
iox_app_id = "helmet"
urllib3.disable_warnings()

#WEBEX TEAMS INFORMATION
ACCESS_TOKEN	= 'ZGQ4NTRkMmQtNjE3Mi00ZDJiLWJhMDEtMmQxZmM1MWU0YzRlNGJhYWFlOTktNWFi_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
ROOM_NAME_GASES	   = 'Gases Alerts'
ROOM_NAME_PULSE	   = 'Pulse Alerts'
ROOM_NAME_HELMET	  = 'Not Using Helmet Alerts'
ROOM_NAME_PANIC	   = 'Panic Alerts'
ROOM_NAME_TEMP_HUM	= 'Temp and Humidity Alerts'

#Tresholds
maxPulse = 150
minPulse = 60
maxTemp = 50.0
maxHum = 90

#sets the header to be used for authentication and data format to be sent to webex teams
def setHeaders():		 
	accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
	return (spark_header)

#check if spark room already exists.  If so return the room id
def findRoom(the_header,room_name):
	roomId=None
	uri = 'https://api.ciscospark.com/v1/rooms'
	resp = requests.get(uri, headers=the_header)
	resp = resp.json()
	for room in resp["items"]:
		if room["title"] == room_name:
			roomId=room["id"]
			break   
	return(roomId)

#posts a message to the room
def postMsg(the_header,roomId,message):
	message = {"roomId":roomId,"markdown":message}
	uri = 'https://api.ciscospark.com/v1/messages'
	resp = requests.post(uri, json=message, headers=the_header)

def sendToIOX(key,value):
	datapoints_payload = {key:[{"value":value}]}
	headers = {"Content-Type": "application/json", "X-Token-Id": iox_token, "X-App-Id": iox_app_id}
	url = "https://"+iox_ip+":"+iox_port+"/iox/api/v2/hosting/apps/" + iox_app_id + "/ioxv/datapoints"
	response = requests.put(url, json=datapoints_payload, headers=headers, verify=False)

if __name__ == '__main__':
	header=setHeaders()
	room_id_gases=findRoom(header,ROOM_NAME_GASES) 
	room_id_pulse=findRoom(header,ROOM_NAME_PULSE)
	room_id_panic=findRoom(header,ROOM_NAME_PANIC)
	room_id_helmet=findRoom(header,ROOM_NAME_HELMET)
	room_id_temp_hum=findRoom(header,ROOM_NAME_TEMP_HUM)
	print("Running...")
	
	#Main Loop
	while True:

		#Getting the pulse data from arduino connected to serial
		ser= serial.Serial('/dev/ttyACM0',9600,8,'N',1,timeout=5)
		pulse = str(ser.readline())
		pulse = pulse.split("'")[1]
		pulse = pulse.split('\\')[0]
		
		#Reset dashboard alerts
		sendToIOX("gas","0")
		sendToIOX("panic","0")
		sendToIOX("helmetUse","0")
		
		#Getting the temperature and humidity od the helmet sensor
		try:
			humidity, temperature = Adafruit_DHT.read_retry(11, 8)
			sendToIOX("temp",str(temperature))
			sendToIOX("humidity",str(humidity))
			if temperature > maxTemp:
				sendToIOX("logs","ALERT, TEMPERATURE EXCEEDED THRESHOLD")
				postMsg(header,room_id_temp_hum,"##ALERT, TEMPERATURE EXCEEDED MAXIMUM: "+ str(temperature))
			if humidity > maxHum:
				sendToIOX("logs","ALERT, HUMIDITY EXCEEDED THRESHOLD")
				postMsg(header,room_id_temp_hum,"##ALERT, HUMIDITY PULSE EXCEEDED MAXIMUM: "+ str(humidity))
		except:
			None
			
		if not GPIO.input(15):		#Check Gas sensor
			postMsg(header,room_id_gases,"##ALERT, DANGEROUS GAS LEVEL DETECTED ON IVAN SANTA'S HELMET##")
			print("Dangerous gas level detected, messege sent")
			sendToIOX("gas","1")
			sendToIOX("logs","ALERT, DANGEROUS GAS LEVEL DETECTED ON IVAN SANTA'S HELMET")
			for x in range(0, 5):
				GPIO.output(18,1)
				GPIO.output(25,1)
				sleep(0.2)
				GPIO.output(18,0)
				GPIO.output(25,0)
				sleep(0.2)
				
		if not GPIO.input(14):	#Check Pannic Button
			sendToIOX("panic","1")
			sendToIOX("logs","ALERT, PANIC BUTTON DETECTED ON IVAN SANTA'S HELMET")
			postMsg(header,room_id_panic,"##ALERT, PANIC BUTTON DETECTED ON IVAN SANTA'S HELMET##")
			print("Panic Button detected, messege sent.")

		if not GPIO.input(24):		#Check LDR sensor
			try:
				int(pulse)
				sendToIOX("pulseHist",pulse)
				sendToIOX("pulse",pulse)
				if int(pulse) > maxPulse:
					sendToIOX("logs","ALERT, IVAN SANTA'S PULSE EXCEEDED MAXIMUM THRESHOLD")
					postMsg(header,room_id_pulse,"##ALERT, IVAN SANTA'S PULSE EXCEEDED MAXIMUM: "+ pulse)
					print("Pulse exceeded maximum threshold: " + pulse)
				elif int(pulse) < minPulse:
					sendToIOX("logs","ALERT, IVAN SANTA'S PULSE LESS THAN MINIMUM THRESHOLD")
					postMsg(header,room_id_pulse,"##ALERT, IVAN SANTA'S PULSE LESS THAN MINIMUM: "+ pulse)
					print("Pulse less than minimum threshold: " + pulse)
			except:
				None
		else:
			sendToIOX("helmetUse","1")
			sendToIOX("logs","ALERT, IVAN SANTA'S IS NOT USING HIS HELMET")
			postMsg(header,room_id_helmet,"#ALERT, IVAN SANTA'S IS NOT USING HIS HELMET#")
			print("Helmet is not being used, message sent.")
			
		sleep(0.5)
		

indent = 4
print(
    __doc__,
    "Author:",
    " " * indent + __author__,
    "Contributors:",
    "\n".join([" " * indent + name for name in __contributors__]),
    "",
    __copyright__,
    "Licensed Under: " + __license__,
    sep="\n"
)


