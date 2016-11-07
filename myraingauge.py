#! /usr/bin/python
# Post rainfall and GPS data to dweet.io.
# Assumes a tipping bucket rain gauge similar to one described at:
# https://www.raspberrypi.org/learning/weather-station-guide/rain-gauge.md 
# is connected to the RaspberryPI device.
#
# View data at:
# - https://dweet.io/follow/myraingauge-ABC123
# - or https://freeboard.io/board/W94CLw
# 
# To run this file please install necessary components as follows
# sudo apt-get install -y gpsd gpsd-clients python-gps
# Then simulate GPS via gpsfake -o -n -c 0.1 gpslogs.txt   

import os
from gps import *
from time import *
import time
import threading
import dweepy
import RPi.GPIO as GPIO

# CONSTANTS
#change this value to uniquely identify your rain gauge
MYRAINGAUGENAME = 'myraingauge-ABC123'
#the pin to which the rain gauge is connected to the Raspberry PI device
RAINGAUGEPINNUMBER = 6
#time delay to handle the physical switch bounce problem with software
SWITCHBOUNCETIME = 300
#the amount (in mm) of water that tips the rain gauge bucket
#see: https://www.raspberrypi.org/learning/weather-station-guide/rain-gauge.md
BUCKETTIPRAINAMOUNT = 0.2794
SLEEPTIMEBETWEENDWEETS = 3

# GLOBAL VARIABLES
gpsd = None
sender = MYRAINGAUGENAME
myDweet = {}  
rgpin = RAINGAUGEPINNUMBER
rgtipcount = 0

# FUNCTION bucket_tipped
# - increments a global count to be able to calculate rainfall amount
def bucket_tipped(channel):
  global rgtipcount
  rgtipcount = rgtipcount + 1
  print (rgtipcount * BUCKETTIPRAINAMOUNT)

GPIO.setmode(GPIO.BCM)
GPIO.setup(rgpin, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(rgpin, GPIO.FALLING, callback=bucket_tipped, bouncetime=SWITCHBOUNCETIME)

# rain gauges should be uniquely identified
if sender == 'myraingauge-default': 
    print("Please define a unique name for your rain gauge")
    exit()

os.system('clear') #clear the terminal (optional)
 
class GPSMain(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd 
    gpsd = gps(mode=WATCH_ENABLE) 
    self.current_value = None
    self.running = True 
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() 
 
if __name__ == '__main__':
  gpsp = GPSMain() 
  try:
    gpsp.start()
    while True:
      os.system('clear')
      myDweet['latitude'] = gpsd.fix.latitude
      myDweet['longitude'] = gpsd.fix.longitude
      myDweet['altitude'] = gpsd.fix.altitude
      myDweet['rainfall'] = rgtipcount * BUCKETTIPRAINAMOUNT
      myDweet['timestamp'] = ' '.join([str(gpsd.utc),str(gpsd.fix.time)])
      print
      print ' Rain Gauge ' , MYRAINGAUGENAME, ' dweeting:'
      print '----------------------------------------'
      print 'latitude    :' , gpsd.fix.latitude
      print 'longitude   :' , gpsd.fix.longitude
      print 'altitude (m):' , gpsd.fix.altitude
      print 'rainfall    :' , rgtipcount * BUCKETTIPRAINAMOUNT
      print 'timestamp   :' , gpsd.utc,' + ', gpsd.fix.time
      print '----------------------------------------'

      dweepy.dweet_for(sender, myDweet)  
      time.sleep(SLEEPTIMEBETWEENDWEETS)
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    GPIO.cleanup()
  print "Done.\nExiting."
