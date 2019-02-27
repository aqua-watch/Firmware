#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
import sys
from RPi import GPIO

from enum import IntEnum

mh = Adafruit_MotorHAT(addr = 0x60)

UP_DOWN_STEPS = 450
ROT_STEPS = 1000

UP_DOWN_MOTOR = 1
ROT_MOTOR = 2

UP = CW = Adafruit_MotorHAT.FORWARD
DOWN = CCW = Adafruit_MotorHAT.BACKWARD

LOCATION_STATE_PIN = 18
LOCATION_REQUEST_PIN = 27

class Position(IntEnum):
    SAMPLE = 0
    SOLUTION = 1

def releaseAllMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# runs a function on the specified motor (wraps the function in motor initialization and release so that the motor isn't active unless it's running
# (The motors were overheating from not turning off when not in use)
def runOnMotor(motor_num, fn):
    motor = mh.getStepper(200, motor_num)
    motor.setSpeed(200)
    fn(motor)
    releaseAllMotors()

def fullWind(direction):
    runOnMotor(UP_DOWN_MOTOR, lambda motor: motor.step(UP_DOWN_STEPS, direction, Adafruit_MotorHAT.DOUBLE))

def windUp():
    fullWind(Adafruit_MotorHAT.FORWARD)

def windDown():
    fullWind(Adafruit_MotorHAT.BACKWARD)

def rotateCW():
    rotate180(Adafruit_MotorHAT.FORWARD)

def rotateCCW():
    rotate180(Adafruit_MotorHAT.BACKWARD)

def rotate180(direction):
    runOnMotor(ROT_MOTOR, lambda motor: motor.step(ROT_STEPS, direction, Adafruit_MotorHAT.DOUBLE))

def moveToSample():
    windUp()
    rotateCW()
    windDown()

def moveToSolution():
    windUp()
    rotateCCW()
    windDown()

# Make sure all motors get released so that they don't overheat and set on fire
atexit.register(releaseAllMotors)
