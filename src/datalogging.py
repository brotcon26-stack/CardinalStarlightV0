def incrementLogNumber():
    try: #first, we try to open the counter.txt file
        counter = open("counter.txt","r")
        z = int(counter.read()) #here, we read the number in the file
        counter.close()
        z +=1 #we add 1 to the number
        counter = open("counter.txt","w")
        counter.write(str(z)) #and then save that number (with 1 added) back to the file, overrighting what was already there
        counter.close()
    except OSError: #If the file doesn't exist, we get an error and do this instead
        counter = open("counter.txt","w") #create the file
        counter.write("1") #write a 1
        counter.close() #close the file
        z = 1 #we know the number is 1, so we don't need to read it
    return z

class logFile:
    def __init__(self,title,groundTest):
        if groundTest:
            title = title[:-4]
            title+='****GroundTest****.csv'
        self.title = title
        with open(title,'w') as file:
            pass
    
    def writeLine(self,string):
        with open(self.title,'a') as file:
            file.write(f'{string}\n')

def main():
    z = incrementLogNumber()
    title = f'testfile.csv{z}'
    file = logFile(title,True)
    file.writeLine('fish are very cool')
    file.writeLine('really they are')

main()