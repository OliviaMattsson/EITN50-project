from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
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
        sock.connect((UDP_IP, UDP_PORT))

        private_key, derived_key = handshake(sock)

        while True:
            data = input("Send: ")

            # initialization_vector
            # They do not need to be kept secret and they can be included in a transmitted message.
            # Each time something is encrypted a new initialization_vector should be generated.
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))

            p = padding.PKCS7(128).padder()
            padded_data = p.update(data.encode('utf-8')) + p.finalize()

            e = cipher.encryptor()
            encrypted = e.update(padded_data) + e.finalize()

            # 0x02 is the "operation" header
            message = b'\x02' + iv + encrypted

            assert len(message) < 64, "Message size exceeds 64 bytes"
            sock.sendall(message)


# Function for the handshake phase. Should use ECDHE!
def handshake(socket):
    private_key = ec.generate_private_key(ec.SECP384R1())

    public_key = private_key.public_key()

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.CompressedPoint,
    )
    data = b'\x00' + public_bytes
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

    return (private_key, derived_key)


# Function for the transmission phase.
# Perhaps not needed? Since we have while loop in main method. 
def transmission(key):

    # Generate iv for each transmission - should be moved to main if function removed!
    iv = os.urandom(16);


    return

def encrypt(key, iv):

    # My suggestion is AES. Limited in RAM usage and fast. 
    # Use nonces for generating the keys. Perhaps already done with the ivs right?
    # MAC for integrity on transmission

    return

def decrypt():

    return



if __name__ == "__main__":
    main()
