'''
This module takes in variables from sensors such as altitude, acceleration, or anything else, and outputs the current state.
'''

#simple class to define states
class State():
    IDLE = 0
    ASCENT = 1
    DESCENT = 2
    LANDED = 3


class stateMachine:
    
    def __init__(self,apogeeThreshold,lockoutAlt):
       self.state = State.IDLE
       self.apogeeThreshold = apogeeThreshold
       self.lockoutAlt = lockoutAlt

       self.apogeeCounter = 0
       self.maxAltitude = 0

    def update(self,altitude,breakwire):
        
        if self.state == State.IDLE and breakwire == True:
            self.state = State.ASCENT
            #Should add a way to get launch time, either here or in main file

        if altitude > self.maxAltitude:
            self.maxAltitude = altitude
            self.apogeeCounter = 0
        
        elif self.state == State.ASCENT:
            self.apogeeCounter += 1

        if self.state == State.ASCENT and self.apogeeCounter == self.apogeeThreshold and altitude > self.lockoutAlt:
            self.state = State.DESCENT

        if self.state == State.DESCENT and altitude < 10:
            self.state = State.LANDED

    def getState(self):
        return self.state   
    
def main():
    sm = stateMachine(5,10)
    print(sm.getState())
    sm.update(0,True)
    print(sm.getState())
    for alt in range(0,50):
        sm.update(alt,True)
        print(alt)
        print(sm.getState())
    for alt in range(50,-1,-1):
        sm.update(alt,True)
        print(sm.getState())
if __name__ == '__main__':
    main()