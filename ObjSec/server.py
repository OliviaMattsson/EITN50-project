import socket
import sys

# Constants for UDP transmission
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello world"

 # Sets up the socket and binds it to the IP and Port address
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((UDP_IP, UDP_PORT))
print("UDP server up and listening")

# Function for the handshake phase. Should use ECDHE!
def handshake():
    return

# Function for the transmission phase.
def transmission():
    return