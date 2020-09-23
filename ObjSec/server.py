from cryptography.hazmat.primitives import hashes, hmac, serialization, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from jose import jwt

import os
import socket
import sys

# Constants for UDP transmission
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Constants for decryption
SIGN_KEY_SIZE = hashes.SHA256.digest_size
AES_KEY_SIZE = 16
AES_BLOCK_SIZE = 16

def main():
    # Sets up the socket and binds it to the IP and Port address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((UDP_IP, UDP_PORT))

        session_keys = {}
        while True:
            data, (addr, port) = sock.recvfrom(131)
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
                crypt_key, sign_key = split_keys(derived)
                sent_signature = data[-65:]
                log(len(data))
                log(sent_signature)
                data_no_sign = data[:-32]
                log(data_no_sign)
                iv = data_no_sign[1:17]
                message = data_no_sign[17:]
                
                try:
                    check_hmac(message, sent_signature, derived)
                    log("Hash authenticated!")
                    return 
                except:
                    log("Hash not authenticated..")
                    return
                # cleartext_message = aes_decrypt(derived, iv, message)
                
                # log(cleartext_message)


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

def check_hmac(message, sentSign, signKey):
    h = hmac.HMAC(signKey, hashes.SHA256())
    h.update(message)
    h.verify(sentSign)


def split_keys(derived_key):
    crypt_key = derived_key[:-16]
    sign_key = derived_key[-16:]
    return (crypt_key, sign_key)


if __name__ == "__main__":
    main()
