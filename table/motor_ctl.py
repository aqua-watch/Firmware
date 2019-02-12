#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
import sys

mh = Adafruit_MotorHAT(addr = 0x60)
updownMotor = mh.getStepper(200, 1)
updownMotor.setSpeed(200)
rotMotor = mh.getStepper(200, 2)
rotMotor.setSpeed(200)

def fullWind(direction):
    updownMotor.step(1000, direction, Adafruit_MotorHAT.DOUBLE)

def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def rotate180(direction):
    rotMotor.step(1000, direction, Adafruit_MotorHAT.DOUBLE)

atexit.register(turnOffMotors)

arg = sys.argv[1]
if arg == 'up':
    fullWind(Adafruit_MotorHAT.FORWARD)
if arg == 'down':
    fullWind(Adafruit_MotorHAT.BACKWARD)
if arg == 'cw':
    rotate180(Adafruit_MotorHAT.FORWARD)
if arg == 'ccw':
    rotate180(Adafruit_MotorHAT.BACKWARD)
