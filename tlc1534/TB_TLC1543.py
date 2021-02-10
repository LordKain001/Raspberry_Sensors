#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import pprint
import importlib
import RPi.GPIO as GPIO
import sys


import RPi.GPIO as GPIO
from CL_TLC1543 import RPS_TLC1543

Clock = 16
Address = 20
DataOut = 21
Chipselect = 12
EoC = 25
GPIO.setmode(GPIO.BCM)

pp = pprint.PrettyPrinter(indent=8)

def format(l):
    return "["+", ".join(["%04i" % x for x in l])+"]"


try:
	start = time.time()	
	ADC = RPS_TLC1543(Clock,Address,DataOut,Chipselect, EoC)
	
	while True:
		
		ADC.UpdateAllAdcChannels()
		rawdata = ADC.GetAdcRawData()
		print(format(rawdata))
		#pprint.pprint(ADC.GetAdcRawData())
		#print(ADC.GetNumOfMeasurement())

		#time.sleep(0.05)
except:
	print("Unexpected error:", sys.exc_info()[0])
	end = time.time()
	print("\r\n\r\nruntime : %.2f seconds" % (end - start))
	print("%.2f Measurements/seconds\r\n\r\n" % (ADC.GetNumOfMeasurement() / (end - start)))
	raise
GPIO.cleanup()	
