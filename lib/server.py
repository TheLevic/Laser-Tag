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
        print("UDP Server is up a running");
        return UDPServerSocket;

    # Call this method after creating our server object in main.py
    def runServer(self):
        server = self.createSocket(self.address, self.port);
        while self.GameIsOn:
            info = server.recvfrom(self.bufferSize);
            print(info[0]);
server = Server();
server.runServer();
