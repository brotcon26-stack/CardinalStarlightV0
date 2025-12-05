#This main file is a rough pseudoish code of the v2 main file, I would like the final version to be this simple
#but we will see
#from imported import importDepend
#importDepend('SITL')

import sitlInit as init
import sitlSensors as sensors
import logging
import baroFun
import time
import SITL

i2c = init.i2c()
IMU = init.IMU()
baro= init.baro()
breakwire = init.breakwire()

groundAlt = baroFun.calibrateGroundAlt(baro, 10)
previousAlt = groundAlt
eventTitle, dataTitle = logging.getTitles()
logging.createFiles(eventTitle, dataTitle)

usbConnected = init.checkUSBConnection()

while True:
    pressure, temperature = sensors.getPresTemp(baro)
    altitude = baroFun.calculateAltitude(pressure, groundAlt)
    filtAltitude = baroFun.filterAltitude(previousAlt, altitude, 0.4)
    print(f'Altitude: {filtAltitude} m, Temperature: {temperature} °C Filtered Altitude: {filtAltitude} m')

    
