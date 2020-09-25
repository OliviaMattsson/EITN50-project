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
import binascii

# Constants for UDP transmission
UDP_IP = "127.0.0.1"
UDP_PORT = 5005


def main():
    # Sets up the socket and binds it to the IP and Port address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect((UDP_IP, UDP_PORT))

        # Performs a handshake and gets the private and the derived, symmetric key
        private_key, derived_key = handshake(sock)

        # Sets the associated data for the transmission:
        transmission_no = 0

        while True:
            data = input("Send: ")

            # initialization_vector
            # They do not need to be kept secret and they can be included in a transmitted message.
            # Each time something is encrypted a new initialization_vector should be generated.
            iv = os.urandom(16)

            # Encrypts the data to cyphertext with the iv and AES GCM
            aesgcm = AESGCM(derived_key)

            # Associated data - to prevent replay attacks
            transmission_no += 1

            # Encrypts the data
            cyphertext = aesgcm.encrypt(iv, data.encode(
                "utf-8"), str(transmission_no).encode("utf-8"))

            # 0x02 is the "operation" header
            message = b'\x02' + iv + cyphertext

            # Asserts that the packet is not greater than 64 bytes
            assert len(message) < 64, "Message size exceeds 64 bytes"

            print("[Message encrypted, transmitting to server ..]")
            # Sends the message to the server
            sock.sendall(message)


# Function for the handshake phase. Should use ECDHE!
def handshake(socket):
    print("[Initiating handshake with the server ..]")
    private_key = ec.generate_private_key(ec.SECP384R1())

    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.CompressedPoint,
    )
    data = b'\x00' + public_bytes

    print("[Private and public keys generated. Sending to server ..]")
    socket.sendall(data)

    data, (addr, port) = socket.recvfrom(64)
    if data[0] != 0x01:
        raise "Invalid auth response"

    peer_public_bytes = data[1:]
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

    print("[Session key agreed on. Starting transmission phase ..]")
    return (private_key, derived_key)


if __name__ == "__main__":
    main()
