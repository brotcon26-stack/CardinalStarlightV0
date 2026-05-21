import SITL

class barometer:
    def __init__(self):
        self.testGenerator = SITL.readSITLData('Test_Data')

    def getPressure(self):
            testData = next(self.testGenerator)
            return float(testData[3])

def main():
    baro = barometer()
    for i in range (0,50):
        print(baro.getPressure())

if __name__ == '__main__':
    main()
