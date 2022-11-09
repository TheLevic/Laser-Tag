import socket


# We will want to set game is on to false once the timer runs out.
GameIsOn = True;
address = "127.0.0.1"
port = 7501
bufferSize = 1024

# Create our socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Binding the server to our IP
UDPServerSocket.bind((address, port));
print("UDP Server is up a running");

while(GameIsOn):
    # Info 
    info = UDPServerSocket.recvfrom(bufferSize);
    print(info[0])
