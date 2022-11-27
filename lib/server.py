import socket

class Server:
    def __init__(self):
        # We will want to set game is on to false once the timer runs out.
        self.GameIsOn = True;
        self.address = "127.0.0.1"
        self.port = 7501 
        self.bufferSize = 1024

    # Create our socket
    def createSocket(self,address,port):
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM);
        # Binding the server to our IP
        UDPServerSocket.bind((address, port));
        print("UDP Server is up and running");
        return UDPServerSocket;

    def setServerStatus(self):
        self.GameIsOn = not self.GameIsOn;

    # Call this method after creating our server object in main.py
    def runServer(self, playerDict, displayString):
        server = self.createSocket(self.address, self.port);
        while self.GameIsOn:
            info = server.recvfrom(self.bufferSize);
            playerHit = info[0];
            # Parse the infomation, going from bytes form to string.
            infoString = playerHit.decode("utf-8");
            infoString = infoString.split(":")
            # InfoString[0] is going to be the playerId that needs hits incremented by 1
            # From here we need to use infoString[0] to find the player in the playerDict, and increment their hits by 1.
            
            #Loop through each of the lists and see if player.uid == infoString[0]
            playerThatHit = playerDict[infoString[0]];
            playerDict[infoString[0]].numHits+= 1;
            playerGotHit = playerDict[infoString[1]];
            displayString.append(f"Player {playerThatHit.name} hit player {playerGotHit.name}.");