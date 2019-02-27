#!/usr/bin/env python3

"""
Created on Sun Nov  4 16:29:05 2018

@author: Armin
"""
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# import model
from serial import Serial
import datetime
import time
from datetime import timedelta 
import time
import json 
import atexit
from motor_ctl import Position, moveToSample, moveToSolution

# TODO: Should probably put this in a class instead of having all these globals
TIME_BEFORE_CHECK = 15
TIME_TO_SAMPLE = datetime.timedelta(hours=0, minutes=0, seconds=15)
TIME_TO_CLEAN = datetime.timedelta(hours=0, minutes=0, seconds=10)

aqua_watch_port = '/dev/ttyACM0' 
aqua_watch_serial = Serial(aqua_watch_port, 9600)
atexit.register(lambda: aqua_watch_serial.close())
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
	#Tell Aqua Watch to sample
	aqua_watch_serial.write("1\n")

	current_data_set = aqua_watch_serial.readline()
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
			
		
	model.insert_model("/table_test/test", current_data_set)
	print("SAMPLE DONE")

def main():
	global start_time
	global curr_position

	while True:
		if timeToSample():
			if curr_position != Position.SAMPLE:
				moveToSample()
				curr_position = Position.SAMPLE
				start_time = currTime()
			# performSample()

		if timeToClean():
			if curr_position != Position.SOLUTION:	
				moveToSolution()
				curr_position = Position.SOLUTION
				start_time = currTime()

		time.sleep(TIME_BEFORE_CHECK)

if __name__ == '__main__':
	main()