# Import the necessary libraries for the script.
import urllib2 as ul
import json
import time
import os
import psutil
import RPi.GPIO as GPIO
from datetime import datetime

# Pin Definitons:
radarSensorPin = 17 # Broadcom pin 17 (P1 pin 11)
irReceiverPin = 18 # Broadcom pin 18 (P1 pin 12)
irLedPin = 22 # Broadcom pin 22 (P1 pin 15)

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(radarSensorPin, GPIO.IN) # RadarSensor pin set as input
GPIO.setup(IRPin,GPIO.IN) # Infrared receiver pin set as input
GPIO.setup(irLedPin,GPIO.OUT)  # Infrared LED pin set as output

binaryIrSignalCode = 1111100000111000000100000010111111
#hexIrSignalCode = 0x3e0e040bfL
tvState = false


# Define global variables that track the last connection time and last update time. Also, define time intervals to update the data, and post the data to ThingSpeak.
lastConnectionTime = time.time() # Track the last connection time
lastUpdateTime = time.time() # Track the last update time
postingInterval = 120 # Post data once every 2 minutes
updateInterval = 5 # Update once every 5 seconds

# Define your ThingSpeak channel settings such as write API key and channel ID along with ThingSpeak server settings.
writeAPIkey = "" # Replace YOUR-CHANNEL1-WRITEAPIKEY with your channel write API key
writeChannelID = "" # Replace YOUR-CHANNEL1-ID with your channel ID
url1 = "https://api.thingspeak.com/channels/"+writeChannelID+"/bulk_update.json" # ThingSpeak server settings
messageBuffer = []

readAPIkey = "" # Replace YOUR-CHANNEL2-READAPIKEY with your channel read API key
readChannelID = "" # Replace YOUR-CHANNEL2-ID with your channel ID
url1 = "https://api.thingspeak.com/channels/"+writeChannelID+"/fields/1.json" # ThingSpeak server settings


# Define the function httpRequest to send data to ThingSpeak and to print the response code from the server. A response code 202 indicates that the server has accepted the request and will process it.
def httpRequest():
	'''Function to send the POST request to 
	ThingSpeak channel for bulk update.'''
	
	global messageBuffer
	data = json.dumps({'write_api_key':writeAPIkey,'updates':messageBuffer}) # Format the json data buffer
	req = ul.Request(url1 = url1)
	requestHeaders = {"User-Agent":"mw.doc.bulk-update (Raspberry Pi)","Content-Type":"application/json","Content-Length":str(len(data))}
	for key,val in requestHeaders.iteritems(): # Set the headers
		req.add_header(key,val)
	req.add_data(data) # Add the data to the request
    # Make the request to ThingSpeak
	try:
		response = ul.urlopen(req) # Make the request
		print response.getcode() # A 202 indicates that the server has accepted the request
	except ul.HTTPError as e:
		print e.code # Print the error code
	messageBuffer = [] # Reinitialize the message buffer
	global lastConnectionTime
	lastConnectionTime = time.time() # Update the connection time
	
# Define the function getRadarData that returns movement data
def getRadarData():
	'''Function that returns the radar data'''
	movement = GPIO.input(sensorPin)
	return movement

# Define the function updatesJson to continuously update the message buffer every 15 seconds.
def updatesJson():
	'''Function to update the message buffer
	every 15 seconds with data. And then call the httpRequest 
	function every 2 minutes. This examples uses the relative timestamp as it uses the "delta_t" parameter. 
	If your device has a real-time clock, you can also provide the absolute timestamp using the "created_at" parameter.
	'''

	global lastUpdateTime
	message = {}
	message['delta_t'] = int(round(time.time() - lastUpdateTime))
	movement = getRadarData()
	print("Movement: "+movement)
	message['field2'] = tvState
	message['field1'] = movement
	global messageBuffer
	messageBuffer.append(message)
    # If posting interval time has crossed 2 minutes update the ThingSpeak channel with your data
	if time.time() - lastConnectionTime >= postingInterval:
		httpRequest()
	lastUpdateTime = time.time()

def getIRData(): #Pulls data from infrared sensor
	if !GPIO.input(PinIn): #Waits until pin is pulled low
		num1s = 0 #Number of consecutive 1s
		command = [] #Pulses and their timings
		binary = 1 #Decoded binary command
		previousValue = 0 #The previous pin state
		value = GPIO.input(PinIn) #Current pin state
		
		startTime = datetime.now() #Sets start time
		
		while True:
			if value != previousValue: #Waits until change in state occurs
				now = datetime.now() #Records the current time
				pulseLength = now - startTime #Calculate time in between pulses
				startTime = now #Resets the start time
				command.append((previousValue, pulseLength.microseconds)) #Adds pulse time to array (previous val acts as an alternating 1 / 0 to show whether time is the on time or off time)
			
			#Interrupts code if an extended high period is detected (End Of Command)	
			if value:
				num1s += 1
			else:
				num1s = 0
			
			if num1s > 10000:
				break
			
			#Reads values again
			previousValue = value
			value = GPIO.input(PinIn)
			
		#Covers data to binary
		for (typ, tme) in command:
			if typ == 1:
				if tme > 1000: #According to NEC protocol a gap of 1687.5 microseconds repesents a logical 1 so over 1000 should make a big enough distinction
					binary = binary * 10 + 1
				else:
					binary *= 10
					
		print("Binary value: " + str(binary)) #Test print
		
		if len(str(binary)) > 34: #Sometimes the binary has two rouge charactes on the end
			binary = int(str(binary)[:34])
			
		return binary
	return 0
	
def sendIRData():
	# Send binaryIrSignalCode
	return

# Run an infinite loop to continuously call the function updatesJson once every 15 seconds.
if __name__ == "__main__":  # To ensure that this is run directly and does not run when imported 
	while 1:
		# If update interval time has crossed 15 seconds update the message buffer with data
	    if time.time() - lastUpdateTime >= updateInterval:
	        updatesJson()
		
		if getIRData() == binaryIrSignalCode:
			tvState != tvState
			
		
		# Read new data from Teamspeak
		#if ?:
		#	sendIRData()