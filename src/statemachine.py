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

    def update(self,altitude,breakwire):
        
        if self.state == State.IDLE and breakwire == 1:
            self.state = State.ASCENT
            #Should add a way to get launch time, either here or in main file

        if altitude > self.maxAltitude:
            self.maxAltitude = altitude
            self.apogeeCounter = 0
        
        elif self.state == State.ASCENT:
            self.apgeeCounter += 1

        if self.state == State.ASCENT and self.apogeeCounter == self.apogeeThreshold and altitude > self.lockoutAlt:
            self.state == State.DESCENT

        if self.state == State.DESCENT and altitude < 10:
            self.state == State.LANDED

    def getState(self):
        return self.state
        




#if not Launched and VertAccel > 1.5:  #Use this line for ground testing
    if not Launched and Breakwire.value() == 1: #Use this line for actual flights
        Launched = True
        LaunchTime = utime.ticks_ms() #Launch Time is saved relative to startup, whereas all other times are relative to launch
        Event = 1 #1 means in flight
        print("Launched!")
        whiteLED.ON()
        
    #Burnout is detected when vertical acceleration is close to zero
    if Launched and not Burnout and VertAccel < 0.2:
        Burnout = True
        BurnoutTime = Time #Every event has a time logged, this should help with post flight analysis
        Event = 2 # Event 2 is unpowered coast
        print("Burnout!")
    
    #Max Altitude function. If our current altitude is higher than max altitude, it is the maximum
    if Altitude > MaxAltitude:
        MaxAltitude = Altitude
        ApogeeCounter = 0 #This is used for apogee detection. If we are still ascending, this should be zero
        
    #Apogee Detection - If we are descending a number of times, we detect apogee
    ApogeeThreshold = 5
    if Launched and not Apogee and Altitude < MaxAltitude: #This means we have descended since last reading (and have not yet hit apogee)
        ApogeeCounter +=1 #If we fell, we add 1 to the counter
    if not Apogee and ApogeeCounter == ApogeeThreshold and Altitude > triggerAltitude + 5: #This is how we detect apogee.
        #We must have descended for a certain number of frames (apogee threshold) and be above the triggerAltitude (This prevents early chute deployments)
        Apogee = True
        ApogeeTime = Time
        Event = 3 # Event # 3 is past apogee, descending
        print("Apogee!")
    
    #Landing detect - if we have reached apogee and are under 10 feet, we can assume we have landed
    if Launched and Apogee and not Landed and Altitude < 10:
        Landed = True
        LandingTime = Time
        Event = 4 # Event 4 means on the ground
        print("Landed!")