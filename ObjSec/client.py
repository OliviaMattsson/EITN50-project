import socket
import sys

# Constants for UDP transmission
UDP_IP = "127.0.0.1"
UDP_PORT = 5005


def main():
    # Sets up the socket and binds it to the IP and Port address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect((UDP_IP, UDP_PORT))

        while True:
            data = input("Send: ")
            sock.sendall(data.encode("utf-8"))


# Function for the handshake phase. Should use ECDHE!
def handshake():
    return


# Function for the transmission phase.
def transmission():
    return


if __name__ == "__main__":
    main()
