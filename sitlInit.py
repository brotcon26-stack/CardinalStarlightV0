#Hardware initializations for SITL on CPython -> Not for flight use

def i2c():
    return 'mockI2C'
def IMU():
    return 'mockIMU'
def baro():
    return 'mockBaro'
def breakwire():
    return 'mockBreakwire'
def checkUSBConnection():
    return False