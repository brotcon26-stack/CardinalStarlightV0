import time
import SITL

barometerReplay = SITL.readSITLData(file)
def getPresTemp(baro):
    if time.ticks_ms() < 20000:
        #Simulate some pressure and temperature readings during ground idle
        pressure = 1013.25  # Standard atmospheric pressure at sea level in hPa
        temperature = 20.0   # Standard temperature in Celsius
    else:
        
