#This main file is a rough pseudoish code of the v2 main file, I would like the final version to be this simple
#but we will see
import imports.py

i2c = init.i2c()
IMU = init.IMU()
baro= init.baro()
breakwire = init.breakwire()

groundAlt = calibrateGroundAlt(baro)

eventTitle, dataTitle = init.getTitles()
createFiles(eventTitle, dataTitle)

usbConnected = checkUSBConnection()

while True:
    pressure, temperature = sensors.getPresTemp(baro)
    altitude = calculateAltitude(pressure, groundAlt)
    filtAltitude = filterAltitude(a,altitude)

    
