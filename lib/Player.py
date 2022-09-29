# A class to create different players to add in to the laser tag game


class Player:
    def __init__(self):
        self.name = None
        self.uid = None
        self.numPlayersHit = 0
        self.gotHit = False
        self.count_down = 20  # Countdown timer for vest to reactivate
        self.alive = True
        self.numLives = 1  # numLives was originally declared in subtractLife(),
        # set to default in initialization for now
        self.numHits = 0

    def setName(self, name):
        self.name = name

    def setUID(self, UID):
        self.uid = UID

    def subtractLife(self):
        self.numLives = self.numLives - 1

    def gotHit(self):
        self.gotHit = True

    def hitOtherPlayer(self):
        self.numPlayersHit = self.numHits + 1

    def countdown(self):
        if self.gotHit is True:
            if self.count_down > 0:
                self.count_down = self.count_down - 1
            else:
                self.gotHit = False
                self.count_down = 20
    
    def toggleLife(self):
        if self.numLives > 0:
            pass
        else:
            self.alive = False

    def update(self):
        self.toggleLife()
        self.countdown()
        
        
    