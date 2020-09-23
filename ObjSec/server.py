from cryptography.hazmat.primitives import hashes, hmac, serialization, padding
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
                message = data[17:]
                cleartext_message = aes_decrypt(derived, iv, message)
                
                log(cleartext_message)


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


def aes_decrypt(key, iv, ciphertext):
    # MAC for integrity on transmission

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    d = cipher.decryptor()

    decrypted = d.update(ciphertext) + d.finalize()

    u = padding.PKCS7(128).unpadder()
    unpadded = u.update(decrypted) + u.finalize()
    cleartext = unpadded.decode('utf-8')

    return cleartext

def check_hmac(message, key):
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(message)
    h.verify()

    return message

if __name__ == "__main__":
    main()
