import time

def getAltitude(pressure):
    return (145366.45 * (1.0 - pow(pressure / 1013.25, 0.190284))) # returns altitude in feet

def calcGroundAlt(cycles,baro):
    groundCalc = 0
    for i in range(cycles):
        pressure = baro.getPressure()
        print(pressure)
        groundCalc = groundCalc + getAltitude(pressure)
        time.sleep(0.1)
    groundAltitude = groundCalc/cycles
    return groundAltitude