# A class to create different players to add in to the laser tag game


class Player:
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid
        self.numHits = 0
        self.color = ""

