import sitlSensors as sensors
import time

def calibrateGroundAlt(baro, samples=10):
    total_altitude = 0.0
    for _ in range(samples):
        pressure, _ = sensors.getPresTemp(baro)
        # Simple formula to convert pressure to altitude (in meters)
        altitude = 44330.0 * (1.0 - (pressure / 1013.25) ** (1/5.255))
        total_altitude += altitude
        time.sleep(0.1)  # Simulate delay between readings
    ground_altitude = total_altitude / samples
    return ground_altitude

def calculateAltitude(pressure, groundAlt):
    altitude = 44330.0 * (1.0 - (pressure / 1013.25) ** (1/5.255))
    return altitude - groundAlt

def filterAltitude(prevAlt, Alt, a=0.4):
    filtAlt = a * Alt + (1 - a) * prevAlt
    return filtAlt