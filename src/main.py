#Data Logging only file for Starlight. Useful for drop tests or other applications
#Flight computer performs no actions, only passively logs data from startup until shutdown

#This version also has a servo that moves when breakwire is pulled

import utime
import starlight
import machine
import LED
from Servo import Servo
from machine import Pin

#Open and closed positions for the servo
OpenX = 3100
ClosedX = 7000

def getAltitude(pressure):
    return (145366.45 * (1.0 - pow(pressure / 1013.25, 0.190284))) # returns altitude in feet

#Start i2c communications 
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=100000)

#Enable the Level Shifter - this allows the 3.3V RP2040 to talk to the 5V servos
#I'm not totally sure this is necessary, but better safe than sorry
LevelShifter = Pin(14,Pin.OUT)
LevelShifter.value(1)

#Setup the Barometer/Altitude Sensor
baro = starlight.BMP388(i2c, 0x76) #C 291 Creates the altimeter object
baro.enable_temp_and_pressure() #C 292 Enables the sensors
baro.calibrate() #C 293 Calibrates the altimeter
print("Barometer Calibrated")

whiteLED = LED.LED(24)
whiteLED.OFF()

#Detection pin for breakwire
Breakwire = Pin(1, Pin.IN, Pin.PULL_UP)

servo = Servo(11,OpenX,ClosedX)

pressure = 0
temperature = 0
groundAlt = 0
altitude = 0
errorLog = 0

#This code takes a number of readings of the current altitude and then averages them
cycles = 10 #A larger number increases the number of samples, which would make this take longer
groundCalc = 0
for i in range(cycles):
    pressure = baro.getPressure()
    print(pressure)
    groundCalc = groundCalc + getAltitude(pressure)
    utime.sleep(0.1)
groundAlt = groundCalc/cycles
print("Ground Altitude = "+str(groundAlt))



#This is some code to update the counter to create a new file for each flight

try: #first, we try to open the counter.txt file
    counter = open("counter.txt","r")
    z = int(counter.read()) #here, we read the number in the file
    counter.close()
    z +=1 #we add 1 to the number
    counter = open("counter.txt","w")
    counter.write(str(z)) #and then save that number (with 1 added) back to the file, overrighting what was already there
    counter.close()
except OSError: #If the file doesn't exist, we get an error and do this instead
    counter = open("counter.txt","w") #create the file
    counter.write("1") #write a 1
    counter.close() #close the file
    z = 1 #we know the number is 1, so we don't need to read it
    
#Setting up the datalogging file
#FlightData files log raw data, Event files log settings and events.
dataTitle = "DataLogger"+str(z)+".csv" #Title for the raw data

#dataLog = open(dataTitle,"w") #This creates the datalogging file based on the previous blocks of code - each time this runs, a new file is created
with open(dataTitle,'w') as dataLog:
    dataLog.write('time,temperature,pressure,altitude,errorLog\n')

whiteLED.ON() #Turn LED on to signify start of logging

servo.Close()

while True:

    prevPressure = pressure
    try:
        pressure = baro.getPressure() #updates the pressure
        temperature = baro.getTemperature() #updates the temperature
    except OSError:
        print("Barometer error")
        errorLog += 5
    
    if pressure < 0:
        pressure = prevPressure
        errorLog += 5
        print('Barometer Error (Negative 1)')

    altitude = getAltitude(pressure) - groundAlt
    dataFrame = f'{utime.ticks_ms()},{temperature},{pressure},{altitude},{errorLog}\n'

    with open(dataTitle,'a') as dataLog:
        dataLog.write(dataFrame)


    #Servo Logic
    if Breakwire.value() == 0:
        servo.Open()
    else:
        servo.Close()
        
    utime.sleep_ms(50)