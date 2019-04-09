#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
import sys
import datetime
from RPi import GPIO
from enum import IntEnum
from datetime import timedelta 

BIG_UP_DOWN_STEPS = 590
SMALL_UP_DOWN_STEPS = 380

ROT_STEPS = 1000

UP_DOWN_MOTOR = 1
ROT_MOTOR = 2

UP = CW = Adafruit_MotorHAT.FORWARD
DOWN = CCW = Adafruit_MotorHAT.BACKWARD

# These two pins are the input end of the endstop connection
SAMPLE_ENDSTOP_PIN = 23
SOLUTION_ENDSTOP_PIN = 27
RAIL_ENDSTOP_PIN = 25

MOTOR_TIMEOUT = datetime.timedelta(hours=0, minutes=0, seconds=15)

mh = Adafruit_MotorHAT(addr = 0x60)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SAMPLE_ENDSTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SOLUTION_ENDSTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RAIL_ENDSTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class Position(IntEnum):
    SAMPLE = 0
    SOLUTION = 1

def releaseAllMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# Only now do I see why some people who like functional languages hate python.
def windUntilStoppedHelper(motor, direction, endstop_pin):
    # Run for at most 10 seconds. 
    # If it's not done winding in 10 seconds then something is wrong, so kill the process
    end_time = datetime.datetime.now() + MOTOR_TIMEOUT
    while GPIO.input(endstop_pin) == 0: 
        if datetime.datetime.now() >= end_time:
            print("windUntilStoppedHelper timed out on motor {} with direction {}".format(motor.motornum, direction))
            sys.exit(1)
        motor.step(1, direction, Adafruit_MotorHAT.DOUBLE)

def windUntilStopped(motor, direction, endstop_pin):
    runOnMotor(motor, lambda motor: windUntilStoppedHelper(motor, direction, endstop_pin))

# runs a function on the specified motor (wraps the function in motor initialization and release so that the motor isn't active unless it's running
# (The motors were overheating from not turning off when not in use)
def runOnMotor(motor_num, fn):
    motor = mh.getStepper(200, motor_num)
    motor.setSpeed(200)
    fn(motor)

def fullWind(direction):
    runOnMotor(UP_DOWN_MOTOR, lambda motor: motor.step(BIG_UP_DOWN_STEPS, direction, Adafruit_MotorHAT.DOUBLE))

def halfWind(direction):
    runOnMotor(UP_DOWN_MOTOR, lambda motor: motor.step(SMALL_UP_DOWN_STEPS, direction, Adafruit_MotorHAT.DOUBLE))

def windUp():
    windUntilStopped(UP_DOWN_MOTOR, UP, RAIL_ENDSTOP_PIN)

def windDown():
    fullWind(Adafruit_MotorHAT.BACKWARD)

def windDownHalf():
    halfWind(Adafruit_MotorHAT.BACKWARD)

def rotateCW():
    windUntilStopped(ROT_MOTOR, CW, SOLUTION_ENDSTOP_PIN)

def rotateCCW():
    windUntilStopped(ROT_MOTOR, CCW, SAMPLE_ENDSTOP_PIN)

def moveToSample():
    windUp()
    rotateCCW()
    windDownHalf()
    releaseAllMotors()

def moveToSolution():
    windUp()
    rotateCW()
    windDown()

# Make sure all motors get released so that they don't overheat and set on fire
atexit.register(releaseAllMotors)

# Testing code
if __name__ == '__main__':
    while True:
        windUp()