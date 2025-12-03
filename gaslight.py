import random

def noisefunc(multiplier):
    noise = random.random()
    noise *= multiplier
    negate = random.random()
    if negate > 0.5:
        noise *= -1
    return noise
def SILAltitude(x):
    if x < 4000:
        y = 0
    elif 4000 <= x < 7605.55128:
        #x = float(x)
        x /= 1000
        #y = float((-16/1000**2)*(x-1802-4000**2)+52)
        y = -16*x**2+185.6*x-538.24+52
    else:
        y = 0
    y += noisefunc(2)
    return y
def SILAcceleration(x):
    if x < 3000:
        y = 0
    elif 3000 <= x < 3750:
        y = 3
    elif 3750 <= x < 4000:
        x /= 1000
        y = -12*x+48
    else:
        y = 0
    y += noisefunc(0.5)
    return y
