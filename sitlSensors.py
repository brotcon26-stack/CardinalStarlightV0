import time
import SITL

file= 'Test_Data'

barometerReplay = SITL.readSITLData(file)
def getPresTemp(baro):
    if time.time() < 20000:
        #Simulate some pressure and temperature readings during ground idle
        pressure = 1013.25  # Standard atmospheric pressure at sea level in hPa
        temperature = 20.0   # Standard temperature in Celsius
    else:
        data = next(barometerReplay)
        pressure = float(data[3])
        temperature = float(data[4])
    return pressure, temperature



def main():
    # Example usage of getPresTemp function
    baro = None  # Placeholder for barometer object
    while True:
        pressure, temperature = getPresTemp(baro)
        print(f"Pressure: {pressure} hPa, Temperature: {temperature} °C")
        time.sleep(0.1)
if __name__ == "__main__":
    main()