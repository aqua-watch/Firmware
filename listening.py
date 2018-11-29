# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 16:29:05 2018

@author: Armin
"""
import model
from serial import Serial 
import time
import json 


""" Two portions we need to listen to the arm (OPRPA) and we need to ignore or add to the model """

def main():
	aqua_watch_port = '/dev/ttyACM0' 
	arm_port = '/dev/ttyUSB0' 

	arm_serial = Serial(arm_port, 9600)
	aqua_watch_serial = Serial(aqua_watch_port, 9600)
	TIME_BEFORE_CHECK = 15

	while True:  
	    print("reading") 
	    gpio_status = arm_serial.readline()
	    print("GPIO status: " + gpio_status)
	    try:
	    	temp = int(gpio_status)

	    except:
	    	time.sleep(TIME_BEFORE_CHECK)
	    	continue



	    if(int(gpio_status) == 1): #ready for sampling
	    	print("ready to read from aquawatch")
	    	while(True):
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
	    			
	    		break 
	    	model.insert_model("test_arm", current_data_set)
	    # else:
	    # 	#keep checking
	    # 	time.sleep(1)
	    # 	continue

	    # print str("GPIO Status")
	    print("DONE")
	    time.sleep(TIME_BEFORE_CHECK) #

	

	aqua_watch_serial.close()
	arm_serial.close()

if __name__ == '__main__':
	main()