from SITL import readSITLData

class barometer:
    def __init__():
        SITLGenerator = readSITLData('Test_Data')

    def getPressure():
            testData = next(SITLGenerator)
            return testData[3]
def main():
    baro = barometer()
    for i in range (0,50):
        print(baro.getPressure)

if __name__ == '__main__':
     main()
