# A class to create different players to add in to the laser tag game


class Player:
    def __init__(self):
        self.name = None;
        self.uid = None;
        self.numPlayersHit = 0;
        self.gotHit = False;
        self.hitOtherPlayer = False;
        self.countdown = 20; # Countdown timer for vest to reactivate
        self.alive = True;

    def setName(self, name):
        self.name = name;

    def setUID(self, UID):
        self.uid = UID;

    def subtractLife(self):
        self.numLives = self.numLives - 1;

    def gotHit(self):
        self.gotHit = True;

    def hitOtherPlayer(self):
        self.numPlayersHit = self.numHits + 1;
        self.hitOtherPlayer = True;

    def countdown(self):
        if self.gotHit == True:
            self.countdown = self.countdown - 1;
    
    def toggleLife(self):
        if self.numLives > 0:
            pass;
        else:
            self.alive = False;

    def update(self):
        self.toggleLife();
        
    