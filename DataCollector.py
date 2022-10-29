import serial
import time
import string
import pynmea2
import logging


def getGPS():
    try:
        while True:
            port="/dev/ttyAMA0"
            ser=serial.Serial(port, baudrate=9600, timeout=0.5)
            dataout=pynmea2.NMEAStreamReader()
            newdata=ser.readline()

            if newdata[0:6] == "$GPRMC":
                newmsg=pynmea2.parse(newdata)
                lat=newmsg.latitude
                long=newmsg.longitude
                gps = "Latitude" + str(lat) + "and Longitude=" + str(long)
                print(gps)
    except Exception as e:
        print("Error occured while receiving or parsing GPS data")
        logging.error(e)
