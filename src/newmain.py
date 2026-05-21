import statemachine
import time

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




baro = sensors.barometer()

while True:
    pressure = baro.getPressure()
    print(pressure)
    print(getAltitude(pressure))
    time.sleep(1)