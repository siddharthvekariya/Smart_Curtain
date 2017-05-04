from flask import Flask
from flask import request
from flask import Flask, request, url_for, redirect, render_template
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

app = Flask(__name__)


global runA #set
global runB #Manual
global runC #Auto
global runD #Daylight

runA = 0
runB = 0
runC = 0
runD = 0


@app.route('/Set', methods=['GET'])
def Set():
	
#	return 'Hello world'
	import RPi.GPIO as GPIO
	from time import sleep
	from datetime import datetime
	import time
	import calendar
	#import ntplib
	from time import ctime


	GPIO.setmode(GPIO.BOARD)

	Motor1A = 35
	Motor1B = 37
	Motor1E = 12
	Limit_UP = 29 #bmc 5
	Limit_Down = 26 #bmc 7

	GPIO.setup(Motor1A, GPIO.OUT)
	GPIO.setup(Motor1B, GPIO.OUT)
	GPIO.setup(Motor1E, GPIO.OUT)
	GPIO.setup(Limit_UP, GPIO.IN)
	GPIO.setup(Limit_Down, GPIO.IN)

#	HOUR_ON  = request.form[_on_hours]  
#	MINUTES_ON = request.form[_On_minutes]  
#
#	HOUR_OFF = request.form[_Off_Hours] 
#	MINUTES_OFF = request.form[_Off_minutes] 



	HOUR_ON  = input ("ON Hour =")  
	MINUTES_ON = input ("ON Minutes =") 

	HOUR_OFF = input ("OFF Hour =") 
	MINUTES_OFF = input ("OFF Minutes =")

	global runA
	global runB
	global runC
	global runD
	
	runB = 0
	runA = 1
	runC = 0
	runD = 0
	


	pwm = GPIO.PWM(Motor1E,100)

	pwm.start(16)
	
	while (runA):
	
		d = datetime.now()
		Current = calendar.timegm(d.timetuple())
	
		time = int(Current / 86400) * 86400
		#print time	
	
		on = (int(HOUR_ON * 3600) + int(MINUTES_ON * 60) + time)
		off = (int(HOUR_OFF * 3600) + int(MINUTES_OFF * 60) + time)
		
		#	print Current

		# the cutain will be up for set time else it will be down

		if (Current in range(on,off)): 
			"print up"
			if (GPIO.input(Limit_UP) == False) :
				GPIO.output(Motor1A, GPIO.LOW)
			else:
				GPIO.output(Motor1A, GPIO.HIGH)
				GPIO.output(Motor1B, GPIO.LOW)
		else:
			print "Down"
			if (GPIO.input(Limit_Down) == False) :
				GPIO.output(Motor1B, GPIO.LOW)
			else:			
				GPIO.output(Motor1A, GPIO.LOW)
				GPIO.output(Motor1B, GPIO.HIGH)

	pwm.stop()
	sleep(0.1) 
	GPIO.cleanup()
	return 'Finished!'

@app.route('/Manual', methods=['GET'])

def Manual():
	global runA
	global runB
	global runC
	 
	runA = 0
	runB = 1
	runC = 0
	
	import RPi.GPIO as GPIO
	from time import sleep
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	Motor1A = 35 	# Motor wire A
	Motor1B = 37 	# Motor wirw B
	Motor1E = 12	# Motor enable for h-bridge
	B1 = 33 	# Input Button Up
	B2 = 31		# Input Button Down
	W_up = 13 	# Web input Button Up
	W_down = 11 	# Web input Button Down
	Limit_UP = 29 	# Limit switch Up
	Limit_Down = 26 # Limit switch Down


	GPIO.setup(Motor1A, GPIO.OUT)
	GPIO.setup(Motor1B, GPIO.OUT)
	GPIO.setup(B1, GPIO.IN)
	GPIO.setup(B2, GPIO.IN)
	GPIO.setup(W_up, GPIO.OUT)
	GPIO.setup(W_down, GPIO.OUT)
	GPIO.setup(Limit_UP, GPIO.IN)
	GPIO.setup(Limit_Down, GPIO.IN)
	GPIO.setup(Motor1E, GPIO.OUT)

	global runA
	global runB
	global runC
	global runD
	
	runB = 1
	runA = 0
	runC = 0
	runD = 0
	

	pwm = GPIO.PWM(Motor1E,100)
	
	pwm.start(20)



	while(runB):


		if (GPIO.input(Limit_UP) == False) :
			GPIO.output(Motor1A, GPIO.LOW)		
		else:
			if (GPIO.input(B1) == False) or (GPIO.input(W_up) == True) :

				GPIO.output(Motor1A, GPIO.HIGH)
				GPIO.output(Motor1B, GPIO.LOW)
		
			else:
				GPIO.output(Motor1A, GPIO.LOW)		
		
		if (GPIO.input(Limit_Down) == False) :		
			GPIO.output(Motor1B, GPIO.LOW)	
		else:
			if (GPIO.input(B2) == GPIO.LOW) or (GPIO.input(W_down) == True):		

				GPIO.output(Motor1A, GPIO.LOW)
				GPIO.output(Motor1B, GPIO.HIGH)
			else:
				GPIO.output(Motor1B, GPIO.LOW)
		
			
	pwm.stop()
	sleep(0.1)
	GPIO.cleanup()
	
	return 'Finished!'


@app.route('/Auto', methods=['GET'])
def Auto():
	import RPi.GPIO as GPIO
	from time import sleep
	from tsl2561 import TSL2561
	import time
	GPIO.setmode(GPIO.BOARD)

	Motor1A = 35
	Motor1B = 37
	Limit_UP = 29 #bmc 5
	Limit_Down = 26 #bmc 7
	Motor1E = 12
	
	GPIO.setup(Motor1A, GPIO.OUT)
	GPIO.setup(Motor1B, GPIO.OUT)
	GPIO.setup(Motor1E, GPIO.OUT)
	GPIO.setup(Limit_UP, GPIO.IN)
	GPIO.setup(Limit_Down, GPIO.IN)
	global runA
	global runB
	global runC
	global runD
	
	runB = 0
	runA = 0
	runC = 1
	runD = 0
	

	pwm = GPIO.PWM(Motor1E,100)
	pwm.start(10)

	while(runC):
	
		tsl = TSL2561(address = 0x39)
		lux = int(tsl.lux())
		print lux
	
		if (lux > 110): 
			print "Up"
			if (GPIO.input(Limit_UP) == False) :
				print "Motor Stopp"
				GPIO.output(Motor1A, GPIO.LOW)
			else:
				print "Motor UP"
				GPIO.output(Motor1A, GPIO.HIGH)
				GPIO.output(Motor1B, GPIO.LOW)
		
		
		else:
			print "Down"
			if (GPIO.input(Limit_Down) == False) :
				print "Motor Stop"
				GPIO.output(Motor1B, GPIO.LOW)
			else:			
				print "Motor DOWN"
				GPIO.output(Motor1A, GPIO.LOW)
				GPIO.output(Motor1B, GPIO.HIGH)		

	pwm.stop()
	sleep(0.1) 
	GPIO.cleanup()

	return 'Finished'


@app.route('/Daylight', methods=['GET'])
def Daylight():
	import RPi.GPIO as GPIO
	from time import sleep
	from datetime import datetime
	import time
	import calendar
	import urllib, json
	import re

	GPIO.setmode(GPIO.BOARD)
	
	
	Motor1A = 35
	Motor1B = 37
	Motor1E = 12
	Limit_UP = 29 
	Limit_Down = 26 

	GPIO.setup(Motor1A, GPIO.OUT)
	GPIO.setup(Motor1B, GPIO.OUT)
	GPIO.setup(Motor1E, GPIO.OUT)
	GPIO.setup(Limit_UP, GPIO.IN)
	GPIO.setup(Limit_Down, GPIO.IN)
	
	global runA
	global runB
	global runC
	global runD
	
	runB = 0
	runA = 0
	runC = 0
	runD = 1
	
	htmlfile = urllib.urlopen("http://api.openweathermap.org/data/2.5/weather?q=London&units=metric&APPID=e43f2e1d61a364587b8ae902cc2a8dc1")

	htmltext = htmlfile.read()

	d = json.loads(htmltext)

	sunrise = d['sys']['sunrise'] + 3600

	sunset = d['sys']['sunset'] + 3600

	print sunrise
	print sunset

	pwm = GPIO.PWM(Motor1E,100)

	pwm.start(30)

	while (runD):

		d = datetime.now()
		Current = calendar.timegm(d.timetuple())	
#		print Current
		GPIO.setmode(GPIO.BOARD)

		if (Current in range(sunrise, sunset)): 
			GPIO.setmode(GPIO.BOARD)

			if (GPIO.input(Limit_UP) == True) :
				
				#print "Motor UP"
				GPIO.output(Motor1A, GPIO.HIGH)
				GPIO.output(Motor1B, GPIO.LOW)
		
			else:
				#print "Motor Stop"
				GPIO.output(Motor1A, GPIO.LOW)
			
		else:
			if (GPIO.input(Limit_Down) == True) :
				#print "Motor DOWN"
				GPIO.output(Motor1A, GPIO.LOW)
				GPIO.output(Motor1B, GPIO.HIGH)
			else:
				#print "Motor Stop"
				GPIO.output(Motor1B, GPIO.LOW)	
		
				
	sleep(0.5) 
	pwm.stop()
	GPIO.cleanup()
	return 'Finished'

@app.route('/s', methods=['GET'])
def s():
	from flask import Flask, request, url_for, redirect

	global runA
	global runB
	global runC
	global runD
	
	runB = 0
	runA = 0
	runC = 0
	runD = 0
	
	return redirect("http://192.168.0.105:3000/", code=302)	
	

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='192.168.0.105', port=4200)
