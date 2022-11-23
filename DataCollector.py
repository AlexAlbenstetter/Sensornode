import serial
import logging
import string
import time
import datetime
import io
import pynmea2
import csv


class DataStorage:
#Create new csv file for measurement storage
    def setupFile():
        try:
            fileCreation= datetime.datetime.now() 
            day=fileCreation.strftime('%d')
            month=fileCreation.strftime('%b')
            year=fileCreation.strftime('%Y')
            time=fileCreation.strftime('%X').replace(':','')
            
            filename= f'{day}{month}{year}_{time}_Measurements.csv'
            file = open(filename, "x")
            return file

        except FileExistsError as e:
            print('CSV file error: {}'.format(e))
            logging.error('CSV file error: {}'.format(e))


class GPS:
    #Function getGPS() collects GPS data from GPS receiver
    def getGPS(file):
        #define serial connection with UART
        port="/dev/ttyAMA0"
        ser=serial.Serial(port, baudrate=9600, timeout=5.0)
        #define IO Buffer for UART ingres 
        sio=io.TextIOWrapper(io.BufferedReader(ser), encoding='latin-1')
        #Set line selector for GPS data
        startparams = '$GPRMC'
        while True:
            try:
                line=sio.readline()
                substring =line[0:6]
                if substring == startparams:
                    newmsg=pynmea2.parse(line)
                    lat=newmsg.latitude
                    long=newmsg.longitude
                    gps = "Latitude" + str(lat) + "and Longitude=" + str(long)
                    print(gps)
                    dataline=f'{lat},{long}'
                    file.write(dataline)

            except pynmea2.ParseError as e:
                print('Parse error: {}'.format(e))
                logging.error(e)
                continue
            except serial.SerialException as e:
                print('Serial UART error: {}'.format(e))
                logging.error(e)
                break
class Sensor:
    def SPS30():
        print('test SPS30')

    def BMP280():
        print('test BMP280')

def main():

    #Define Logging Config for logging
    #Logging level can be adapted 
    FORMAT='%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT,filename='error.log', level=logging.DEBUG)
    print('Logging Setup')
    print('Setup csv file for data storage')
    file= DataStorage.setupFile()
    print('CSV file setup success')
    GPS.getGPS(file)

if __name__ == "__main__":
    main()