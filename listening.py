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
	arm_port = '/dev/ttyUSB1' 

	arm_serial = Serial(arm_port, 9600)
	aqua_watch_serial = Serial(aqua_watch_port, 9600)


	while True:  
	    print("reading") 
	    gpio_status = arm_serial.readline()
	    print(gpio_status)
	    if(int(gpio_status) == 1): #ready for sampling
	    	print("ready to read from aquawatch")
	    	while(True):
	    		current_data_set = aqua_watch_serial.readline()
	    		try:
	    			json.loads(current_data_set)
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
	    time.sleep(15)

	

	aqua_watch_serial.close()
	arm_serial.close()

if __name__ == '__main__':
	main()