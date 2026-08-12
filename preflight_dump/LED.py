import machine
import time

class LED:
    def __init__(self,Pin):
        self.led = machine.Pin(Pin, machine.Pin.OUT)
    
    def Blink(self, repititions, duration):
        number = 0
        while number < repititions:
            self.led.on()
            time.sleep(duration)
            self.led.off()
            time.sleep(duration)
            number += 1
            
    def start_flash(self, on_time, interval):
        """Start flashing the LED on for a certain amount of time every interval seconds without blocking execution."""
        self.flash_on_time = on_time * 1000
        self.flash_interval = interval * 1000
        self.flashing = True
        self.last_flash_time = time.ticks_ms()

    def update(self):
        """Update the LED state, should be called regularly in the main loop."""
        if self.flashing:
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, self.last_flash_time) >= self.flash_interval:
                self.led.on()
                self.last_flash_time = current_time
            elif time.ticks_diff(current_time, self.last_flash_time) >= self.flash_on_time:
                self.led.off()
                
    def ON(self):
        self.led.on()
        
    def OFF(self):
        self.led.off()
        
        
def main():
    testLED = LED(24)
    testLED.ON()
    time.sleep(5)
    testLED.OFF()
    testLED.Blink(5,1)
if __name__ == "__main__":
    main()