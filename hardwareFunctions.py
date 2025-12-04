import machine
import starlight
from machine import Pin
import LED

def initHardware():
    #Start i2c communications 
    i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=100000) #C 285
    
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
    else:
        GroundTest = False
    return i2c, whiteLED, IMU, baro, Breakwire, GroundTest 

def main():
    initHardware()
if __name__ == "__main__":
    main()
