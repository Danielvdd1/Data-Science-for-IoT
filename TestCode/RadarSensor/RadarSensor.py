# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
sensorPin = 17 # Broadcom pin 17 (P1 pin 11)

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(sensorPin, GPIO.IN) # Button pin set as input


print("Here we go! Press CTRL+C to exit")
try:
	while 1:
		if GPIO.input(sensorPin): # button is released
			print("On")
		else: # button is pressed
			print("Off")
		
		time.sleep(0.1)
		
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly
	GPIO.cleanup() # cleanup all GPIO

