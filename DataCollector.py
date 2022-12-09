try:
    import serial
    import logging
    import string
    import time
    import datetime
    import io
    import pynmea2
    import csv
    import math

except ImportError as e:
    print('Import Error: {}'.format(e))
    logging.error('Import Error: {}'.format(e))

# Imports for BME280 
try:
    from smbus2 import SMBus
except ImportError as e:
    from smbus import SMBus
from bme280 import BME280



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
            file = open(filename, "w", encoding='UTF8')
            writer = csv.writer(file)
            header = ['Latitude','Longitude', 'Temperature', 'Humidity', 'Pressure','PM2.5','PM10']
            writer.writerow(header)
            return writer

        except FileExistsError as e:
            print('CSV file error: {}'.format(e))
            logging.error('CSV file error: {}'.format(e))

"""
Nicht mehr notwendig, aber evtl. gut um den Umgang mit self und init method abzugucken
class Sensor_BME280:

    def __init__(self):

   
    
    def getData(self):
        temperature = self.sensor.get_temperature()
        pressure = self.sensor.get_pressure()
        humidity = self.sensor.get_humidity()
        sensordata = [temperature, pressure, humidity]
        return sensordata

    def printData(self):
        temperature = self.sensor.get_temperature()
        pressure = self.sensor.get_pressure()
        humidity = self.sensor.get_humidity()
        print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
"""

class Sensor:
    def SPS30():
        pass

class GPS:
    #Function getGPS() collects GPS data from GPS receiver
    def getGPS(self,writer,bme280Sensor):
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
                    #GPS Data:
                    lat=newmsg.latitude
                    long=newmsg.longitude

                    #Bosch BME280 Data:
                    temp = round(bme280Sensor.get_temperature(),4)
                    hum = round(bme280Sensor.get_humidity(),4)
                    pres = round(bme280Sensor.get_pressure(),4)

                    #Create Timestamp:
                    creationTimestamp = datetime.datetime.now()
                    #hier noch pressure und humidity einfügen
                    dataString = "Latitude: "+str(lat)+" | Longitude: " +str(long)+ " | Temperature: " +str(temp)+" | Humidity: "+str(hum)+" | Pressure: "+str(pres)
                    print(dataString)
        
                    #Prepare array for 'write to file'
                    dataline=[creationTimestamp,lat,long,temp,hum,pres]
                    #Append new data row to file
                    writer.writerow(dataline)

            except pynmea2.ParseError as e:
                print('Parse error: {}'.format(e))
                logging.error(e)
                continue
            except serial.SerialException as e:
                print('Serial UART error: {}'.format(e))
                logging.error(e)
                break


def main():

    #Define Logging Config for logging
    #Logging level can be adapted 
    FORMAT='%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT,filename='error.log', level=logging.DEBUG)
    print('Logging Setup')
    print('Setup csv file for data storage')
    file= DataStorage.setupFile()
    print('CSV file setup success')

    #initialize BME280 sensor
    #Select I2C Bus to which the device/sensor is connected
    bus = SMBus(1)
    bme280Sensor = BME280(i2c_dev=bus)
    print('initialize Bosch Sensor BMP280')  

    #create object called gps of GPS class
    gps = GPS()
    gps.getGPS(file,bme280Sensor)

if __name__ == "__main__":
    main()