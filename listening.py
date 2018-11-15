# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 16:29:05 2018

@author: Armin
"""
import model
import serial
import time

""" Two portions we need to listen to the arm (OPRPA) and we need to ignore or add to the model """

def main():
	arm_port = '/dev/ttyl' # temp
	aqua_watch_port = '/dev/ttyl' #temp

	arm_serial = serial.Serial(arm_port, 9600)
	aqua_watch_serial = serial.Serial(aqua_watch_port, 9600)


	while True:    
	    gpio_status = arm_serial.read()

	    if(int(gpio_status) == 1): #ready for sampling
	    	current_data_set = aqua_watch_serial.read()
	    	model.addToModel(current_data_set, "new_data_set")
	    else:
	    	#keep checking
	    	time.sleep(1)
	    	continue

	    print str("GPIO Status")
	    time.sleep(15)


if __name__ == '__main__':
	main()