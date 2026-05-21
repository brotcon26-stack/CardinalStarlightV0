
class fish:
    def __init__(self,length,mass):
        self.length = length
        self.mass = mass
    
    def getSize(self):
        self.size = self.length * self.mass

    def printSize(self):
        print(self.size)

#Enum to define states
class State():
    IDLE = 0
    ASCENT = 1
    DESCENT = 2
    LANDED = 3
    
salmon = fish(10,10)
salmon.getSize()
salmon.printSize()
print(State.ASCENT)