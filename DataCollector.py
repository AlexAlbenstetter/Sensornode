import serial
import logging
import string
import time
import io
import pynmea2


logging.basicConfig(filename='example.log', level=logging.DEBUG)



def getGPS():
    port="/dev/ttyAMA0"
    startparams = '$GPRMC'
    ser=serial.Serial(port, baudrate=9600, timeout=5.0)
    sio=io.TextIOWrapper(io.BufferedReader(ser),encoding='latin-1')

    while True:
        try:
            #dataout=pynmea2.NMEAStreamReader()
            line=sio.readline()

            substring =line[0:6]

            if substring == startparams:

                newmsg=pynmea2.parse(line)

                #print(newmsg)

                lat=newmsg.latitude

                long=newmsg.longitude

                gps = "Latitude" + str(lat) + "and Longitude=" + str(long)

                print(gps)

        #except Exception as e:

            #print("Error occured while receiving or parsing GPS data")

            #logging.error(e)

            #break

        except pynmea2.ParseError as e:

            print('Parse error: {}'.format(e))

            logging.error(e)

            continue



getGPS()
