# Trusted computing in the cloud, lecture 9

## Enclave technology, see SGX

## Homomorphic encryption
Example:
Consider RSA encryption. Enc(m) = m^e mod n.
According to the math,
Enc(a) * Enc(b) mod n = Enc(a*b) mod n.
This means that we can compute the multiplication mod n by operating on the encrypted versions of the two clear text messages. 

Can compute the multiplication in the cloud without knowing the initial message.

A cryptosystem is Semantically Secure (SS) if given any probalistic, polynomial-time algorithm (PPTA) that is given the ciphertext of a certain message m and the message's length, cannot determine any partial information on the message with probability non-neglibly higher than all other PPTA's that only have access to the message length. 

### Probabilistic encryption
Given a key, randomness and a message m. The result is that the codeword is a single encryptogram of a set of m possible cryptograms. The randomness determines which cryptogram it will be. 


## Trusted VM launch