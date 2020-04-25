# 1) Create a channel as shown in Collect Data in a New Channel.

# 2) Import the necessary libraries for the script.
import urllib2 as ul
import json
import time
import os
import psutil

# 3) Define global variables that track the last connection time and last update time. Also, define time intervals to update the data, and post the data to ThingSpeak.
lastConnectionTime = time.time() # Track the last connection time
lastUpdateTime = time.time() # Track the last update time
postingInterval = 120 # Post data once every 2 minutes
updateInterval = 15 # Update once every 15 seconds

# 4) Define your ThingSpeak channel settings such as write API key and channel ID along with ThingSpeak server settings.
writeAPIkey = "VT49I2XQZN5YLRIJ" # Replace YOUR-CHANNEL-WRITEAPIKEY with your channel write API key
channelID = "1046499" # Replace YOUR-CHANNELID with your channel ID
url = "https://api.thingspeak.com/channels/"+channelID+"/bulk_update.json" # ThingSpeak server settings
messageBuffer = []

# 5) Define the function httpRequest to send data to ThingSpeak and to print the response code from the server. A response code 202 indicates that the server has accepted the request and will process it.
def httpRequest():
	'''Function to send the POST request to 
	ThingSpeak channel for bulk update.'''
	
	global messageBuffer
	data = json.dumps({'write_api_key':writeAPIkey,'updates':messageBuffer}) # Format the json data buffer
	req = ul.Request(url = url)
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
	
# 6) Define the function getData that returns the CPU temperature in Celsius along with the CPU utilization as a percentage.def getData():
def getData():
	'''Function that returns the CPU temperature and percentage of CPU utilization'''
	cmd = '/opt/vc/bin/vcgencmd measure_temp'
	process = os.popen(cmd).readline().strip()
	cpuTemp = process.split('=')[1].split("'")[0]
	cpuUsage = psutil.cpu_percent(interval=2)
	return cpuTemp,cpuUsage

# 7) Define the function updatesJson to continuously update the message buffer every 15 seconds.
def updatesJson():
	'''Function to update the message buffer
	every 15 seconds with data. And then call the httpRequest 
	function every 2 minutes. This examples uses the relative timestamp as it uses the "delta_t" parameter. 
	If your device has a real-time clock, you can also provide the absolute timestamp using the "created_at" parameter.
	'''

	global lastUpdateTime
	message = {}
	message['delta_t'] = int(round(time.time() - lastUpdateTime))
	Temp,Usage = getData()
	print("Temp:", Temp, ", Usage:", Usage)
	message['field1'] = Temp
	message['field2'] = Usage
	global messageBuffer
	messageBuffer.append(message)
    # If posting interval time has crossed 2 minutes update the ThingSpeak channel with your data
	if time.time() - lastConnectionTime >= postingInterval:
		httpRequest()
	lastUpdateTime = time.time()

# 8) Run an infinite loop to continuously call the function updatesJson once every 15 seconds.
if __name__ == "__main__":  # To ensure that this is run directly and does not run when imported 
	while 1:
		# If update interval time has crossed 15 seconds update the message buffer with data
	    if time.time() - lastUpdateTime >= updateInterval:
	        updatesJson()