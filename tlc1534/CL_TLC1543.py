#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

class RPS_TLC1543:
	def __init__(self, clock, address, dataOut):
		# self.clock = clock
		# self.address = address
		# self.dataOut = dataOut
		print("Setup complete")
		# GPIO.setmode(GPIO.BCM)
		# GPIO.setwarnings(True)
		# GPIO.setup(self.clock,GPIO.OUT)
		# GPIO.setup(self.address,GPIO.OUT)
		# GPIO.setup(self.dataOut,GPIO.IN,GPIO.PUD_UP)
		
		# self.data = []
		
	def GetADCData():
		return self.data

	def UpdateAllAdcChannels():
		self.data.clear()
	#init with first Adress start at 0
		for i in range(0,16):
			GPIO.output(Address,GPIO.LOW)
			GPIO.output(Clock,GPIO.HIGH)
			GPIO.output(Clock,GPIO.LOW)
		for channel in range (1,15):
			time.sleep(0.001)
			value = 0
			for i in range(1,17):
				if i <=4:
					if((channel >> (4 - i)) & 0x01):
						GPIO.output(Address,GPIO.HIGH)
					else:
						GPIO.output(Address,GPIO.LOW)
					GPIO.output(Clock,GPIO.HIGH)
					value <<= 1
					if(GPIO.input(DataOut)):
						value |= 0x01
					GPIO.output(Clock,GPIO.LOW)
					GPIO.output(Clock,GPIO.LOW)
				if (i >4) and (i <=10):
					GPIO.output(Clock,GPIO.HIGH)
					value <<= 1
					if(GPIO.input(DataOut)):
						value |= 0x01
					GPIO.output(Clock,GPIO.LOW)
				if i>10:
					GPIO.output(Clock,GPIO.HIGH)
					GPIO.output(Clock,GPIO.LOW)
			self.data.append([channel-1,value])

	def __del__(self):
		GPIO.cleanup()
