from time import sleep


# Define functions for movement
def forwardBil():
    print("L: 100")
    print("R: 100")

def backwardBil():
    print("L: -100")
    print("R: -100")

def venstreBil():
    print("L: 0")
    print("R: 50")

def hoyreBil():
    print("L: 50")
    print("R: 0")

def stopBil():
    print("L: 0")
    print("R: 0")

def set_speed(speed):
    print("Speed L: ", speed)
    print("Speed R: ", speed)



def goForward():
    print("Gï¿½r fremover!")
    forwardBil()

def goBackward():
    print("Gï¿½r bakover!")
    backwardBil()

def goLeft():
    print("Snur venstre!")
    venstreBil()

def goRight():
    print("Snur hï¿½yre!")
    hoyreBil()
    
def stop():
    print("Stoppet!")
    stopBil()
    
def direction(direction):
    if direction == 0:
        stop()
    elif direction == 1:
        goForward()
    elif direction == -1:
        goBackward()
    elif direction == 2:
        goLeft()
    elif direction == 3:
        goRight()
