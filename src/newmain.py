#These imports work regardless of being on the actual hardware
import time
import datalogging
from miscfunctions import getAltitude, calcGroundAlt
from statemachine import State, stateMachine

groundTest = True
slowMode = False
slowModeDelay = 0.5

#These imports are for testing on a PC in CPython
if groundTest:
    import SITLSENSORS as sensors
    import SITLSERVOS as Servo
    import SITLBREAKWIRE as breakwire
    
#These imports are for testing on the actual board
else:
    import Servo
    import LED
    import breakwire


#Servo positions - These are the PWM signals to set each servo to it's open or closed position
XOpen = 7000
XClosed = 3100

#Setting up the servos using my custom servo class
#Servo Setup - We setup two servos, one on the X TVC channel and one on Y.
#These only move once during flight when triggered for parachute deployment or other tasks
servoX = Servo.Servo(11,XOpen,XClosed)
servoXTrigger = State.DESCENT
servoXStatus = False

#Closing the servo
servoX.Close()

z = datalogging.incrementLogNumber()

#Setting up the log file names
#FlightData files log raw data, Event files log settings and events.
dataTitle = "FlightData"+str(z)+".csv" #Title for the raw data
eventTitle = "Flight_"+str(z)+"_Events.csv"


#Actually creating the files based on the titles
dataLog = datalogging.logFile(dataTitle,groundTest)
eventLog = datalogging.logFile(eventTitle,groundTest)

if groundTest:
    eventLog.writeLine("----GROUND TEST MODE----\n") #if we are in ground test mode, I want it to be clear

dataLog.writeLine("pressure,raw_altitude,state,apogee_counter,servo_x_status") #creates a header for the main body of flight data

baro = sensors.barometer()
sm = stateMachine(5,15)
brkwire = breakwire.Breakwire(1)

groundAlt = calcGroundAlt(10,baro)
eventLog.writeLine(f'GroundAltitude={groundAlt}')
#---------------------------------------------------------
#---------------------------------------------------------

while True:
    pressure = baro.getPressure()
    rawAltitude_ft = getAltitude(pressure)
    rawAltitude_ft -= groundAlt
    sm.update(rawAltitude_ft,brkwire.getStatus())

    dataLine = f'{pressure},{rawAltitude_ft},{sm.getState()},{sm.apogeeCounter},{servoXStatus}'
    dataLog.writeLine(dataLine)
    
    if slowMode:
        print(dataLine)
        time.sleep(slowModeDelay)
    
    if sm.getState() == servoXTrigger:
        servoXStatus = True
        servoX.Open()
    elif servoXStatus == False:
        servoX.Close()

    if sm.getState() == State.LANDED and brkwire.getStatus() == False:
        break

eventLog.writeLine(f'MaximumAltitude={sm.maxAltitude}')