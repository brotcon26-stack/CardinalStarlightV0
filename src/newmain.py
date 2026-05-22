import statemachine
import time
import datalogging

groundTest = True
slowMode = False
slowModeDelay = 0.5

if groundTest:
    import SITLSENSORS as sensors
    import SITLSERVOS as Servo
    from SITLMACHINE import Pin

else:
    import Servo
    import LED
    from machine import Pin

def getAltitude(pressure):
    return (145366.45 * (1.0 - pow(pressure / 1013.25, 0.190284))) # returns altitude in feet


#Servo positions - These are the PWM signals to set each servo to it's open or closed position
XOpen = 7000
XClosed = 3100

YOpen = 3100
YClosed = 7000

#Setting up the servos using my custom servo class
#Servo Setup - We setup two servos, one on the X TVC channel and one on Y.
#These only move once during flight when triggered for parachute deployment or other tasks
servoX = Servo.Servo(11,XOpen,XClosed)

servoY = Servo.Servo(12, YOpen, YClosed)

#Closing both servos
servoX.Close()
servoY.Close()


#Detection pin for breakwire
#Breakwire = Pin(1, Pin.IN, Pin.PULL_UP)

#Test pin --> used for groundtesting when not plugged in to a PC
#testPin = Pin(0 , Pin.IN, Pin.PULL_UP)
#if testPin.value() == 0:
#    groundTest = True

z = datalogging.incrementLogNumber()

#Setting up the datalogging file
#FlightData files log raw data, Event files log settings and events.
dataTitle = "FlightData"+str(z)+".csv" #Title for the raw data

#During ground testing we append some ground test stuff in the title
if GroundTest:
    dataTitle = dataTitle[:-4]
    dataTitle+='****GroundTest****.csv'



eventTitle = "Flight_"+str(z)+"_Events.csv"

if GroundTest:
    eventTitle = eventTitle[:-4]
    eventTitle+='****GroundTest****.csv'

#Actually creating the files based on the titles
#TO_DO: This should use with instead of just open
dataLog = open(dataTitle,"w") #This creates the datalogging file based on the previous blocks of code - each time this runs, a new file is created
eventLog = open(eventTitle, "w") #These lines of code repeat this for the event log.

if GroundTest:
    eventLog.write("----GROUND TEST MODE----\n") #if we are in ground test mode, I want it to be clear
eventLog.write("Timeout Time = "+str(timoutTime)+"\n") 
eventLog.write("Trigger Altitude = "+str(triggerAltitude)+"\n ") 

dataLog.write("time_launch_ms,filtered_altitude_ft,unfiltered_altitude_ft,pressure,temperature,acceleration_x_g,acceleration_y_g,acceleration_z_g,gyro_x_rate,gyro_y_rate,gyro_z_rate,max_altitude_ft,apogee_counter,event#,servo_x_state,servo_y_state,error_flag \n") #creates a header for the main body of flight data

dataLog.close()
eventLog.close() #These make sure the logs close correctly


baro = sensors.barometer()

while True:
    pressure = baro.getPressure()
    print(pressure)
    print(getAltitude(pressure))
    time.sleep(1)