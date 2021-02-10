#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import pprint
import importlib
import RPi.GPIO as GPIO
import sys



clock = 16
address = 20
dataOut = 21

pp = pprint.PrettyPrinter(indent=4)




class RPS_TLC1543:
	def __init__(self, clock, address, dataOut):
		self.clock = clock
		self.address = address
		self.dataOut = dataOut
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(True)
		GPIO.setup(self.clock,GPIO.OUT)
		GPIO.setup(self.address,GPIO.OUT)
		GPIO.setup(self.dataOut,GPIO.IN,GPIO.PUD_UP)
		
		self.data = []
		
	def GetADCData(self):
		return self.data

	def UpdateAllAdcChannels(self):
		self.data.clear()
	#init with first Adress start at 0
		for i in range(0,16):
			GPIO.output(self.address,GPIO.LOW)
			GPIO.output(self.clock,GPIO.HIGH)
			GPIO.output(self.clock,GPIO.LOW)
			#pprint.pprint("adress0:" + str(i))
		for channel in range (1,15):
			#pprint.pprint("Channel:" + str(channel))
			time.sleep(0.01)
			value = 0
			for i in range(1,17):
				#pprint.pprint("Get:" + str(i))
				if i <=4:
					if((channel >> (4 - i)) & 0x01):
						GPIO.output(self.address,GPIO.HIGH)
					else:
						GPIO.output(self.address,GPIO.LOW)
					GPIO.output(self.clock,GPIO.HIGH)
					value <<= 1
					if(GPIO.input(self.dataOut)):
						value |= 0x01
					GPIO.output(self.clock,GPIO.LOW)
					GPIO.output(self.clock,GPIO.LOW)
				if (i >4) and (i <=10):
					GPIO.output(self.clock,GPIO.HIGH)
					value <<= 1
					if(GPIO.input(self.dataOut)):
						value |= 0x01
					GPIO.output(self.clock,GPIO.LOW)
				if i>10:
					GPIO.output(self.clock,GPIO.HIGH)
					GPIO.output(self.clock,GPIO.LOW)
			self.data.append([channel-1,value])
		if (self.data[11][1] == 512 and self.data[12][1] == 0 and self.data[13][1] == 1023):
			print("Data OK")
			try:
				self.data.pop(13)
				self.data.pop(12)
				self.data.pop(11)
			except:
				pass
		else:
			print("Data corrupted")
			self.data.clear()
		

	def __del__(self):
		GPIO.cleanup()




try:
	
	ADC = RPS_TLC1543(clock,address,dataOut)
	
	while True:
		ADC.UpdateAllAdcChannels()
		pprint.pprint(ADC.GetADCData())
		time.sleep(2)
except:
	print("Unexpected error:", sys.exc_info()[0])
	raise
	GPIO.cleanup()