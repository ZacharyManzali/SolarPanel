#Import libraries
from datetime import datetime
import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import sqlite3

# main function to drive solar tracker
# Import moduesl
from database import Database
from solarVector import solarVector
from analog_to_digital_implementation import analogToDig

dataClass = Database()
svClass = solarVector()

# Starting GPIO Values
GPIO.output(13, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
GPIO.output(18, GPIO.LOW)

def move(actNum, dir, t):
# 13, 15, 16,18 pins for gpio use
	if (actNum == 1):
		if (dir == 'fwd'):
			GPIO.output(13,GPIO.HIGH)
			time.sleep(t)
			GPIO.output(13, GPIO.LOW)
			print( "Actuator 1 " + str(t * 10) + " mm fwd")
		if (dir == 'rev'):
			GPIO.output(15,GPIO.HIGH)
			time.sleep(t)
			GPIO.output(15, GPIO.LOW)
			print( "Actuator 1 " + str(t * 10) + " mm rev")
	if (actNum == 2):
		if (dir == 'fwd'):
			GPIO.output(16,GPIO.HIGH)
			time.sleep(t)
			GPIO.output(16, GPIO.LOW)
			print( "Actuator 2 " + str(t * 10) + " mm fwd")
		if(dir == 'rev'):
			GPIO.output(18,GPIO.HIGH)
			time.sleep(t)
			GPIO.output(18, GPIO.LOW)
			print( "Actuator 2 " + str(t * 10) + " mm rev")

# Values from UI

longitude = 40.79

latitude = -77.6

tzn = -5

# Creating the databases
# Solar Vectoring is mode 0 and Solar Tracking is mode 1 when using both is mode 2

conn = sqlite3.connect('data')
c = conn.cursor()

c.execute(""" 
          CREATE TABLE IF NOT EXISTS dailyDatabase(
          xStroke real, 
          yStroke real, 
          mode integer, 
          time text
          )""")
conn.commit()

c.execute(""" 
          CREATE TABLE IF NOT EXISTS fullDatabase(
          power real, 
          sunrise text, 
          sunset text,
	  	  date text
          )""")

conn.commit()

# Asking for date
fakeDate = input('What is the date: ')
fakeHour = 10
fakeMin = 0
i = 0
fakeTime = ""

while i < 72:
	if fakeMin < 10:
		fakeTime = str(fakeHour) + ":0" + str(fakeMin)
	else: 
		fakeTime = str(fakeHour) + ":" + str(fakeMin)
	if fakeMin == 55:
		fakeMin = 0
		fakeHour += 1
	else:
		fakeMin += 5
	i += 1
	dataClass.addToDaily(str(svClass.strokeX(latitude, longitude, fakeDate, fakeTime, tzn)), str(svClass.strokeY(latitude, longitude, "11/30/2022", fakeTime, tzn)), str(0), fakeTime)


def initAct():
	move(1, 'rev', 40)
	move(2, 'rev', 40)


# Sun Vectoring
initAct() 
curXStroke = 0
curYStroke = 0
mode = 0
# Asking for date and time	
fakeTime = input('What is the time: ')
curHours = int(fakeTime[0:2])
curMinutes = int(fakeTime[3:5])
c.execute("SELECT * FROM dailyDatabase WHERE time = " + fakeTime)
newXStroke = c.fetchone()[0]
newYStroke = c.fetchone()[1]
if (curXStroke < newXStroke):
    move(1, 'fwd', (newXStroke-curXStroke)/10)
else:
    move(1, 'rev', (curXStroke-newXStroke)/10)
curXStroke = newXStroke
if (curYStroke < newYStroke):
    move(2, 'fwd', (newYStroke-curYStroke)/10)
else:
    move(2, 'rev', (curYStroke-newYStroke)/10)
curYStroke = newYStroke

conn.close()