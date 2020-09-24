from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

import os
import socket
import sys

# Constants for UDP transmission
UDP_IP = "127.0.0.1"
UDP_PORT = 5005


def main():
    # Sets up the socket and binds it to the IP and Port address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((UDP_IP, UDP_PORT))

        # Dict for the session keys involved
        session_keys = {}
        
        # Sets the associated data for the transmission:
        transmission_no = 0
        
        

        print("[Server up and running ..]")    

        while True:
            # Receives data from the client
            data, (addr, port) = sock.recvfrom(64)
            
            # Function to print messages
            def log(m): print(f"{addr}:{port} {m}")
            
            # 0x00 means initial contact - handshake phase initialized
            if data[0] == 0x00:
                log("[Authentication started ..]")
                private, derived = handshake(data[1:])
                session_keys[(addr, port)] = (private, derived)

                log("[Agreed on session key. ]")

                pub_bytes = private.public_key().public_bytes(
                    encoding=serialization.Encoding.X962,
                    format=serialization.PublicFormat.CompressedPoint,
                )

                sock.sendto(b'\x01' + pub_bytes, (addr, port))
            
            # Transmission phase
            else:
                log("[Message received. Decryption started ..]")
                # Retrieves the session keys
                private, derived = session_keys[(addr, port)]

                # Retrieves the iv
                iv = data[1:17]
                # Retrieves the message
                message = data[17:]
                # Decrypts the cyphertext with the iv
                aesgcm = AESGCM(derived)

                # Associated data - to prevent replay attacks
                transmission_no += 1

                cleartext = aesgcm.decrypt(iv, message, str(transmission_no).encode("utf-8"))

                # Prints the message to the console
                log("Message from client: ")
                log(cleartext.decode('utf-8'))


# Function for the handshake phase. 
def handshake(peer_public_bytes):
    private_key = ec.generate_private_key(ec.SECP384R1())
    peer_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP384R1(),
        peer_public_bytes
    )

    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    
    return (private_key, derived_key)


if __name__ == "__main__":
    main()
