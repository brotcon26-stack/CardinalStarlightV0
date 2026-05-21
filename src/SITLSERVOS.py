class Servo:
    def __init__ (self, pin, openPOS, closedPOS):
        
          
        self.openPOS = openPOS
        self.closedPOS = closedPOS
    
    def Open(self):
        pass
        
    def Close(self):
        pass
        
    def Move(self,position):
        pass
        
def main():
    test = Servo(13,1300,1700)
    test.Open()
    test.Close()
    test.Move(1600)
    print('Done')

if __name__ == '__main__':
    main()