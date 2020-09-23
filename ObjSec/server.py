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
        sock.bind((UDP_IP, UDP_PORT))

        session_keys = {}

        while True:
            data, (addr, port) = sock.recvfrom(64)
            def log(m): print(f"{addr}:{port} {m}")

            if data[0] == 0x00:
                log("[auth]")
                private, derived = handshake(data[1:])
                session_keys[(addr, port)] = (private, derived)

                pub_bytes = private.public_key().public_bytes(
                    encoding=serialization.Encoding.X962,
                    format=serialization.PublicFormat.CompressedPoint,
                )

                sock.sendto(b'\x01' + pub_bytes, (addr, port))
            else:
                private, derived = session_keys[(addr, port)]

                iv = data[1:17]

                cipher = Cipher(algorithms.AES(derived), modes.CBC(iv))
                d = cipher.decryptor()

                message = data[17:]
                decrypted = d.update(message) + d.finalize()

                u = padding.PKCS7(128).unpadder()

                unpadded = u.update(decrypted) + u.finalize()
                log(unpadded.decode('utf-8'))


# Function for the handshake phase. Should use ECDHE!
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


# Function for the transmission phase.
def transmission():
    return


if __name__ == "__main__":
    main()
