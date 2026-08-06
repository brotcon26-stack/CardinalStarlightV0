#C - this means that this line of code was copied from the original main.py for starlight

import utime
import select
import math
import starlight
import time
import _thread
import sys
import machine
import SITL
import LED
import Servo
from machine import Pin, PWM

import gc
gc.disable()

GroundTest = True #sets whether to ground test or not. If true, this replaces real data with replayed data from a file
Slowmode = False #If we are in ground test mode, this can also be enabled. This delays 10 seconds after each loop and prints some of the data
slowmodeDelay = 0.2 #Delay time for slowmode in seconds

def getAltitude(pressure):
    return (145366.45 * (1.0 - pow(pressure / 1013.25, 0.190284))) # returns altitude in feet
#C 16 this was not working in the modified original design

#Start i2c communications 
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=100000) #C 285

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

#Led Pin - this is the white LED used to indicate board state
whiteLED = LED.LED(24) #This creates and LED object on pin 24 (using a custom class)
whiteLED.OFF() #Turns said LED off

#Setup the Gyroscope/IMU
IMU = starlight.ICM42605(i2c, 0x68) #C 287 Creats the IMU object
IMU.config_gyro() #C 288 Sets up the IMU
IMU.enable() #C 289 enables the IMU
IMU.get_bias() #C 332 Calibrates the IMU
print("IMU Calibrated")

#Setup the Barometer/Altitude Sensor
baro = starlight.BMP388(i2c, 0x76) #C 291 Creates the altimeter object
baro.enable_temp_and_pressure() #C 292 Enables the sensors
baro.calibrate() #C 293 Calibrates the altimeter
print("Barometer Calibrated")

#Enable the Level Shifter - this allows the 3.3V RP2040 to talk to the 5V servos
#I'm not totally sure this is necessary, but better safe than sorry
LevelShifter = Pin(14,Pin.OUT)
LevelShifter.value(1)

#Detection pin for breakwire
Breakwire = Pin(1, Pin.IN, Pin.PULL_UP)

#Test pin --> used for groundtesting when not plugged in to a PC
testPin = Pin(0 , Pin.IN, Pin.PULL_UP)
if testPin.value() == 0:
    GroundTest = True

#define and zero our variables for datalogging
pressure = 0 #Current Pressure
temperature = 0 #current Temperature
groundAltitude = 0 #Defines ground level, or 0 ft
Altitude = 0 #Our altitude above ground level
MaxAltitude = 0 #Our highest altitude reached so far
VertAccel = 0 #Our current acceleration in the vertical axis

#List of events
Launched = False #Whether or not the rocket has launched
Burnout = False #True when the rocket has entered unpowered flight
Apogee = False #True when the rocket starts descending
Landed = False #True when the rocket gets close to the ground
LandingTimeout = False #True when the rocket touches down and then a certain amount of time elapses
Timeout = False #True when a certain amount of time in flight has elapsed
timeout2 = False
DescentTrigger = False #True when the rocket reaches a certain altitued on descent

#Some other houskeeping variables
ApogeeCounter = 0
Time = 0
errorLog = 0
#Event times - set to negative 1, if the event doesn't happen we can tell from this
LaunchTime = -1
BurnoutTime = -1
ApogeeTime = -1
LandingTime = -1
TrueTimeoutTime = -1
TrueTimeout2Time = -1
DescentTriggerTime = -1

#This code takes a number of readings of the current altitude and then averages them
cycles = 10 #A larger number increases the number of samples, which would make this take longer
groundCalc = 0
for i in range(cycles):
    pressure = baro.getPressure()
    print(pressure)
    groundCalc = groundCalc + getAltitude(pressure)
    time.sleep(0.1)
groundAltitude = groundCalc/cycles
print("Ground Altitude = "+str(groundAltitude))

#Event settings - timout and triggerAltitude can be set, so we set them here
timoutTime = 675 #Saved in milliseconds

timout2Time = 1500

#This is a terrible variable name. This is the altitude that the trigger is set to true at on descent.
#Ex. if this is set to 30, triggerAltitude is set true when the rocket is descending and under 30 feet high
triggerAltitude = 30

#Before we detect the breakwire, we want to make it clear if we are in Ground Test Mode
if GroundTest:
    whiteLED.Blink(30,0.1) 

#Wait until the breakwire is plugged in to start main loop
#We do this before the datalog file so we can move the servo without creating a file
print("Insert Breakwire Jumper")
while Breakwire.value() == 1:
    utime.sleep_ms(100)
    if GroundTest:
        print("Ground Test Mode")
        break
    
utime.sleep_ms(200)

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
dataTitle = "FlightData"+str(z)+".csv" #Title for the raw data

if GroundTest:
    dataTitle = dataTitle[:-4]
    dataTitle+='****GroundTest****.csv'

dataLog = open(dataTitle,"w") #This creates the datalogging file based on the previous blocks of code - each time this runs, a new file is created

eventTitle = "Flight_"+str(z)+"_Events.csv"

if GroundTest:
    eventTitle = eventTitle[:-4]
    eventTitle+='****GroundTest****.csv'
eventLog = open(eventTitle, "w") #These lines of code repeat this for the event log.

if GroundTest:
    eventLog.write("----GROUND TEST MODE----\n") #if we are in ground test mode, I want it to be clear
eventLog.write("Timeout Time = "+str(timoutTime)+"\n") 
eventLog.write("Trigger Altitude = "+str(triggerAltitude)+"\n ") 

dataLog.write("time_launch_ms,filtered_altitude_ft,unfiltered_altitude_ft,pressure,temperature,acceleration_x_g,acceleration_y_g,acceleration_z_g,gyro_x_rate,gyro_y_rate,gyro_z_rate,max_altitude_ft,apogee_counter,event#,servo_x_state,servo_y_state,error_flag \n") #creates a header for the main body of flight data

dataLog.close()
eventLog.close() #These make sure the logs close correctly
print("setup done")

#Variables for the altitude filter
PrevAltitude = 0
a=0.5

#Here we start a blinking on and off LED to show the board is flight ready
whiteLED.start_flash(0.1,1)

StartTime = utime.ticks_ms()

#Setup for ground testing if in ground test mode
if GroundTest:
    testGenerator = SITL.readSITLData('Test_Data')
    prevTime = 0
    
Event = 0 #This variable tells us what phase of flight we are in

frameStart = 0

SIE_STATUS_REG = 0x50110000 + 0x50
SIE_CONNECTED  = 1 << 16
SIE_SUSPENDED  = 1 << 4
usbConnected   = (machine.mem32[SIE_STATUS_REG] & (SIE_CONNECTED | SIE_SUSPENDED)) == SIE_CONNECTED #These lines check if connected to a computer

if usbConnected:
    whiteLED.Blink(3,1)

#Opening the datalog file
#We leave it open for the whole flight and flush occasionally for loop timing
dataLog = open(dataTitle,"a")

#Main flight loop
while True:
    
    #First, update variables and log data
    frameStart = utime.ticks_ms()
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
    try:
        IMUData = IMU.get_accel_and_gyro_data()
    except OSError:
        print("IMU Error")
        errorLog +=1
        
    OriYRate = IMU.gy
    VertAccel = IMU.ay
    RawAltitude = getAltitude(pressure) - groundAltitude #This updates altitude. getAltitude gives altitude from Sea Level so we subtract the groundAltitude
    
    #Ground test stuff - if we are in ground test mode, replace the acceleration and altitude values with SIL versions
    if GroundTest and Launched:
        try:
            testData = next(testGenerator)
            RawAltitude = float(testData[2])
            VertAccel = float(testData[6])
            OriYRate = float(testData[9])
        except IndexError:
            print("No More Data")
            break
        
    


    #Datalogging - we only do this while in flight
    if Launched:
        Time = utime.ticks_ms() - LaunchTime #This updates the relative to launch time. This is not the time since startup, but the time since launch
        #if GroundTest:
            #Time = int(testData[0])
        FrameData = str(Time)+","+str(Altitude)+","+str(RawAltitude)+","+str(pressure)+","+str(temperature)+","+str(IMUData)+","+str(MaxAltitude)+","+str(ApogeeCounter)+","+str(Event)+","+str(ServoX_Trigger)+","+str(ServoY_Trigger)+","+str(errorLog)+"\n"
        FrameData = FrameData.replace("(","")
        FrameData = FrameData.replace(")","")
        dataLog.write(FrameData)
        #dataLog.flush() #This flushes the data to the file so we don't lose it if the board crashes or loses power
      
    #Here are some test bits for orientation measurment (very questionable)
    #frameTime = Time - prevTime
    #error
    #OriY = OriYRate*frameTime
    
    #Slowmode -> if ground testing, we can add a delay and print data in the loops
    if Launched and GroundTest and Slowmode:
        print("\n")
        print("Unfiltered Altitude: "+str(RawAltitude))
        print("Filtered Altitude: "+str(Altitude))
        print("Vertical Acceleration: "+str(VertAccel))
        print(f'Apogee Counter: {ApogeeCounter}')
        print(f'Servo X: {ServoX_Trigger}')
        print(f'Servo Y: {ServoY_Trigger}')
        #print("Roll Orientation: "+str(OriY))
        utime.sleep(slowmodeDelay)
        
    
    #This allows us to trigger launches without the breakwire
    if GroundTest and not Launched and usbConnected:
        input("Hit Enter To Launch: ")
        Launched = True
        
    #if not Launched and VertAccel > 1.5:  #Use this line for ground testing
    if not Launched and Breakwire.value() == 1: #Use this line for actual flights
        Launched = True
        LaunchTime = utime.ticks_ms() #Launch Time is saved relative to startup, whereas all other times are relative to launch
        Event = 1 #1 means in flight
        print("Launched!")
        whiteLED.ON()
        
    #Burnout is detected when vertical acceleration is close to zero
    if Launched and not Burnout and VertAccel < 0.2:
        Burnout = True
        BurnoutTime = Time #Every event has a time logged, this should help with post flight analysis
        Event = 2 # Event 2 is unpowered coast
        print("Burnout!")
    
    #Max Altitude function. If our current altitude is higher than max altitude, it is the maximum
    if Altitude > MaxAltitude:
        MaxAltitude = Altitude
        ApogeeCounter = 0 #This is used for apogee detection. If we are still ascending, this should be zero
        
    #Apogee Detection - If we are descending a number of times, we detect apogee
    ApogeeThreshold = 5
    if Launched and not Apogee and Altitude < MaxAltitude: #This means we have descended since last reading (and have not yet hit apogee)
        ApogeeCounter +=1 #If we fell, we add 1 to the counter
    if not Apogee and ApogeeCounter == ApogeeThreshold and Altitude > triggerAltitude + 5: #This is how we detect apogee.
        #We must have descended for a certain number of frames (apogee threshold) and be above the triggerAltitude (This prevents early chute deployments)
        Apogee = True
        ApogeeTime = Time
        Event = 3 # Event # 3 is past apogee, descending
        print("Apogee!")
    
    #Landing detect - if we have reached apogee and are under 10 feet, we can assume we have landed
    if Launched and Apogee and not Landed and Altitude < 10:
        Landed = True
        LandingTime = Time
        Event = 4 # Event 4 means on the ground
        print("Landed!")
        
    #Timer Trigger - this just looks at time after launch to trigger an event
    if Launched and not Timeout and Time > timoutTime:
        Timeout = True
        TrueTimeoutTime = Time #We still record the time to help in postflight analysis even though it should be the timeout time
        print("Timeout Trigger Activated")
        
        
    #Second timeout trigger
    if Launched and not timeout2 and Time > timout2Time:
        timeout2 = True
        TrueTimeout2Time = Time #We still record the time to help in postflight analysis even though it should be the timeout time
        print("Timeout 2 Trigger Activated")
        
    #Altitude Trigger - this is based purely on altitude, and triggers on descent after going below a certain altitude.
    #This could also easily be done on ascent by just removing the apogee constraint and making it greater than, but I don't see a need for this for now
    if Launched and Apogee and not DescentTrigger and Altitude < triggerAltitude:
        DescentTrigger = True
        DescentTriggerTime = Time
        print("Descent Trigger Activated")
        
    #Altitude filter - this smooths the noisy barometer data
    Altitude = a*RawAltitude + (1-a)*PrevAltitude
    PrevAltitude = Altitude
    #Altitude = RawAltitude #Bypass for Altitude Filter
    
    #Servo Triggers - this allows the trigger we use for servos to be easily changed here
    #These can be set to any of the events listed above
    ServoX_Trigger = Apogee
    ServoY_Trigger = Timeout

    #Servo Checks - this checks if the servo trigger is true and moves the servo to the relevent position
    if ServoX_Trigger: #If the servo trigger is true, set it to open position
        servoX.Open()
    else:
        servoX.Close() #Otherwise, set it closed
    
    if ServoY_Trigger: #Repeat with the Y servo
        servoY.Open()
    else:
        servoY.Close()
        
    if not Launched:
        whiteLED.update() #This updates the flash of the LED
        
    #Cutoff - This exits the loop a bit of time after landing so that we can finish up some stuff and stop the code running
    #if Landed and Time - LandingTime > 2000: #this happens 2 seconds after landing, could be changed. 
        #break
    if Landed and Breakwire.value() == 0:
        break
    #time.sleep(0.02)
    while utime.ticks_ms() < frameStart + 10: #This ensures that the loop takes at least 10ms to run (Otherwise we could get errors)
        pass
    
    prevTime = Time    
    #if Launched:
        #error
    
    #dataLog.close()

#Final datalogging to print some important info from flight

#eventLog = open(eventTitle,"a")
#eventLog.write("\n")

with open(eventTitle,'a') as eventLog:
    eventLog.write("Max Altitude:"+str(MaxAltitude)+"\n")
    eventLog.write("Launch Time:"+str(LaunchTime)+"\n")
    eventLog.write("Burnout Time:"+str(BurnoutTime)+"\n")
    eventLog.write("ApogeeTime:"+str(ApogeeTime)+"\n")
    eventLog.write("Landing Time:"+str(LandingTime)+"\n")
    eventLog.write("Actual Timeout Time: "+str(TrueTimeoutTime)+"\n")
    eventLog.write("Altitude Trigger Time :"+str(DescentTriggerTime)+"\n")
    eventLog.write(f'Actual timout 2 time: {TrueTimeout2Time}')


dataLog.close()
eventLog.close()







whiteLED.OFF()
print("Finished!")
