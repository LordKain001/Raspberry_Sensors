#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

class RPS_TLC1543:
	def __init__(self, clock, address, dataOut, chipselect, endOfConvertion):
		self.clock = clock
		self.address = address
		self.dataOut = dataOut
		self.cs = chipselect
		self.EoC = endOfConvertion
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(True)

		GPIO.setup(self.clock,GPIO.OUT)
		GPIO.setup(self.address,GPIO.OUT)
		GPIO.setup(self.dataOut,GPIO.IN,GPIO.PUD_UP)
		GPIO.setup(self.cs,GPIO.OUT)
		GPIO.setup(self.EoC,GPIO.IN,GPIO.PUD_UP)

		GPIO.output(self.address,GPIO.LOW)
		GPIO.output(self.clock,GPIO.LOW)
		GPIO.output(self.cs,GPIO.HIGH)

		
		self.data = []
		self.counter = 0

	def GetNumOfMeasurement(self):
		return self.counter
		
	def GetAdcRawData(self):
		return self.data

	def UpdateAllAdcChannels(self):
		GPIO.output(self.clock,GPIO.LOW)
		GPIO.output(self.cs,GPIO.LOW)
		#time.sleep(0.001)
		adcData = []
	#init with first Adress start at 0
		for i in range(0,16):
			GPIO.output(self.address,GPIO.LOW)
			GPIO.output(self.clock,GPIO.HIGH)
			GPIO.output(self.clock,GPIO.LOW)
			#pprint.pprint("adress0:" + str(i))
		for channel in range (1,15):
			#pprint.pprint("Channel:" + str(channel))
			#time.sleep(0.01)
			sleepcount = 0
			while not GPIO.input(self.EoC):
				#time.sleep(0.001)
				sleepcount += 1
			#print(sleepcount)

			#time.sleep(0.00005)
			GPIO.output(self.cs,GPIO.LOW)
			#time.sleep(0.00005)
			value = 0
			for i in range(1,11):
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
					GPIO.output(self.cs,GPIO.HIGH)
					GPIO.output(self.clock,GPIO.HIGH)
					GPIO.output(self.clock,GPIO.LOW)
			#adcData.append([channel-1,value])
			adcData.append(value)


		# Check if Data is transieved correctly
		#if (adcData[11][1] == 512 and adcData[12][1] == 0 and adcData[13][1] == 1023):
		if (adcData[11] == 512 and adcData[12] == 0 and adcData[13] == 1023):
			#print("Data OK")
			try:
				adcData.pop(13)
				adcData.pop(12)
				adcData.pop(11)
				#self.data.clear()
				self.data = adcData
				self.counter = self.counter + 1
			except:
				pass
		else:
			#print("Data corrupted")
			#pprint.pprint(self.counter)
			self.counter =  self.counter - 1
			adcData.clear()

		GPIO.output(self.cs,GPIO.HIGH)
		
	def __del__(self):
		GPIO.cleanup()
