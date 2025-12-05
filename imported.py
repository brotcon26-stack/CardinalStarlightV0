
def importDepend(mode):
    #SITL VERSION OF IMPORTS -> NOT FOR FLIGHT USE
    if mode == 'SITL':
        import sitlInit as init
        import sitlSensors as sensors
    else:
        error

