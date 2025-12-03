#Module for machine testing on CPython
class Pin:
    IN = 0
    OUT = 1

    def __init__(self, pin_number, mode=IN, pull=None):
        self.pin_number = pin_number
        self.mode = mode
        self.state = 0

    def value(self, val=None):
        if val is not None:
            self.state = val
        return self.state
    def on(self):
        self.state = 1
    def off(self):
        self.state = 0
    def PULL_UP(self):
        pass
class PWM:
    def __init__(self, pin):
        self.pin = pin
        self.duty_cycle = 0

    def duty(self, duty_cycle):
        self.duty_cycle = duty_cycle
    def freq(self, frequency):
        self.frequency = frequency
    def duty_u16(self, duty_cycle):
        self.duty_cycle = duty_cycle

class I2C:
    def __init__(self, id, scl, sda, freq=100000):
        self.id = id
        self.scl = scl
        self.sda = sda
        self.freq = freq
        self.devices = {}

    def writeto_mem(self, addr, memaddr, data):
        if addr in self.devices:
            device = self.devices[addr]
            device.write_memory(memaddr, data)

    def readfrom_mem(self, addr, memaddr, nbytes):
        if addr in self.devices:
            device = self.devices[addr]
            return device.read_memory(memaddr, nbytes)
        return bytes([0]*nbytes)

    def register_device(self, addr, device):
        self.devices[addr] = device