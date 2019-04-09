#!/usr/bin/env python3

"""
Created on Sun Nov  4 16:29:05 2018

@author: Armin's abouri
"""
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import model
from serial import Serial
import datetime
import time
from datetime import timedelta 
import time
import json 
import atexit
from motor_ctl import Position, moveToSample, moveToSolution

# Constants
TIME_TO_SAMPLE = datetime.timedelta(hours=0, minutes=10, seconds=0)
TIME_TO_CLEAN = datetime.timedelta(hours=0, minutes=0, seconds=20)
AQUA_WATCH_PORT = '/dev/ttyACM0' 
BAUD_RATE = 9600
MODEL_PATH = 'phase_1/model'
MODEL_DESCRIPTION = '500 ml of distilled, 2.5ml of vinegar, 100cm^2'

# Allow us to perform movement without being connected to the arduino
USE_DWEEN = False if '--no_dween' in sys.argv else True
CALIBRATE = False if '--no_calib' in sys.argv else True

# Serial setup and cleanup
aqua_watch_serial = Serial(AQUA_WATCH_PORT, BAUD_RATE) if USE_DWEEN else None
if USE_DWEEN:
	atexit.register(lambda: aqua_watch_serial.close())

# Initialize information about where we are in the sampling process
curr_position = Position.SAMPLE
start_time = datetime.datetime.now()

def currTime():
	return datetime.datetime.now()

def timeToSample():
	return \
		(curr_position == Position.SAMPLE and currTime() < start_time + TIME_TO_SAMPLE) or \
		(curr_position == Position.SOLUTION and currTime() > start_time + TIME_TO_CLEAN)

def timeToClean():
	return \
		(curr_position == Position.SOLUTION and currTime() < start_time + TIME_TO_CLEAN) or \
		(curr_position == Position.SAMPLE and currTime() > start_time + TIME_TO_SAMPLE)

def performSample():
	# Can't sample if the dween's not attached
	if not USE_DWEEN:
		print("Not sampling -- no_dween flag was used")
		return

	#Tell Aqua Watch to sample
	aqua_watch_serial.write(str.encode(str(1), 'utf-8'))
	while(True):
		current_data_set = aqua_watch_serial.readline().decode('utf-8')
		print(current_data_set)
		try:
			testable_dataset = json.loads(current_data_set)
			continue_flag = False
			for k, v in testable_dataset.items():
				if(not type(v) == list or len(v) < 49):
					print("Malformed data: " + v)
					continue_flag = True
					break
				else:
					for val in v:
						if(not type(val) == dict or len(val) < 5):
							print("Malformed data: " + val)
							continue_flag = True
							break
			if(continue_flag):
				continue_flag = False
				continue

		except:	
			continue
		break
			
		
	model.insert_model(MODEL_PATH, MODEL_DESCRIPTION, 1, -1 , current_data_set) #parms name of model, desc,  iscont, amoutn of cont
	print("SAMPLE DONE")

def calibrate():
	print("Place the sample jar directly under the probes, lower the probes into the jar. Press [Enter] to continue.")
	input()
	moveToSolution()
	print("Place the solution jars under the probes, and lower the probes into the jars. Press [Enter] to continue.")
	input()
	moveToSample()
	print("Calibration done.")

def main():
	global start_time
	global curr_position

	#if CALIBRATE:
#		calibrate()

	if USE_DWEEN:
		while aqua_watch_serial.in_waiting > 0:
			aqua_watch_serial.read()

	print("Starting sampling.")
	performSample()
	start_time = currTime()

	while True:
		if timeToSample():
			if curr_position != Position.SAMPLE:
				moveToSample()
				curr_position = Position.SAMPLE
				start_time = currTime()
				performSample()

		if timeToClean():
			if curr_position != Position.SOLUTION:	
				moveToSolution()
				curr_position = Position.SOLUTION
				start_time = currTime()

if __name__ == '__main__':
	main()
