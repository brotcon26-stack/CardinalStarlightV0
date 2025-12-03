from machine import Pin, PWM

class Servo:
    def __init__ (self, pin, openPOS, closedPOS):
        
        self.serv = PWM(Pin(pin))
        self.serv.freq(50)
        
        self.openPOS = openPOS
        self.closedPOS = closedPOS
    
    def Open(self):
        self.serv.duty_u16(self.openPOS)
        
    def Close(self):
        self.serv.duty_u16(self.closedPOS)
        
    def Move(self,position):
        self.serv.duty_u16(position)
        
'''def main():
    import time
    testServo = Servo(11,3500,6500)
    testServo.Open()
    time.sleep(1)
    testServo.close()
    
if __name__ == '__main__':
    main()
    '''