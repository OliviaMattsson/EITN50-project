# Object Security

## Preparations:
* Read paper by Selander, obj sec. for IoT ( http://www.eit.lth.se/fileadmin/eit/courses/eitn50/Project_ObjSec/protected/Application_Layer_Security_Protocols_for_IoT.pdf ).
* Read about forward security (https://scotthelme.co.uk/perfect-forward-secrecy/)
Summary: Perfect Forward Secrecy assures that your session keys will not be compromised even if the private key of the server is compromised. The server generates a new session key for every session with a user, so a leaked session key can't affect other sessions. Should be used by everyone who uses TLS/SSL.
Your key exchange has to be:
  * Ephermal
  The client and server generates new Diffie-Hellman parameters for each session. The parameters should never be re-used or stored. 
  * Diffie-Hellman

How to get PFS:
* Diffie-Hellman key exchange with sipher suits Elliptic Curve DHE (ECDHE). ECDHE is the most preferred one. 

Not a lot of sites have started to use PFS. Most hosts are happy as long as their users get the padlock in their browser. 

Heartbleed
Is a bug that allows a hacker to extract data from the memory of a vulnerable server. From passwords and email addresses to the private key. If they retrieve the private key and have been recodring traffic, they can now decrypt it. This is what PFS prevents, since the keys are different for each session. 

Got a link to "Getting an A+ rating on the Qualys SSL Test" (https://scotthelme.co.uk/a-plus-rating-qualys-ssl-test/)


## General layout of the report
* Group number + names
* Brief architectural overview of the implementation
* Document the work with logs and printouts
* The code should include all non-standard dependencies on libraries
* Reported in pdf-format.

## Assignment 1
Implement an Object Security-based communication adapted for IoT. The following criteria should be fulfilled:
### Part A
* Work on the principle of object security
  * On the application level. Secure object consists of a header (metadata), a payload (potentially encrypted), and an integrity verification tag. 
* Provide integrity, confidentiality, and replay protection
  * Integrity: Can be read but not changed. 
  * Confidentiality: In order for a communication session to provide forward secrecy, the communicating parties can run an Elliptic Curve Diffie-Hellman (ECDH) key exchange protocol with ephemeral keys, from which shared key material can be derived. Ephemeral Diffie-Hellman Over COSE (EDHOC) is a compact and lightweight authenticated Diffie-Hellman key exchange protocol with ephemeral keys. Use for authentication and key exchange. Look on ACE as well, auth framework suitable for IoT. 
  * Replay protection: 
* Use UDP as the way to exchange data between the two parties (sending and rceiving party)
* Work on the princple of forward security
  * See article summary above. 
* Should have at leat two distinct parts; handshake and protected data exchange
* Actually work when we test in. The data packets should be as small as one can expect for small IoT devices, max 64 bytes 
* Document and explain the design choices for your implementation
### Part B
* Report should contain a sequence diagram of the protocol parts (using PLANTUML)
* Test with an intermediate party that acts as a cache that your receiving party can later pickup the objects from the intermediatory party

## Helpful tips
* Use Java or Python (Python maybe?)
* Cryptography libraries: PyCrypto or cryptography (Python), BouncyCastle (Java)