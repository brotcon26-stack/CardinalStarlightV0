class Breakwire:
    def __init__(self,Pin):
        self.Pin = Pin(1, Pin.IN, Pin.PULL_UP)

    def getStatus(self):
        if self.Pin.value() == 0:
            return True
        if self.Pin.value() == 1:
            return False