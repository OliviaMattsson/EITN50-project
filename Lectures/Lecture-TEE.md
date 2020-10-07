# Lect 6 - cont. (tror jag)

TEE Architecture.
Bridge between the REE and the TEE with a TEE entry in device hardware and firmware with TEE support. 
Wouldn't have the isolation if it was run by OS. 

# TEE in mobile device
Trust anchor - in hardware in firmware. 
Cryptographic mechanisms - identity of device
Boot sequence 
Platform integrity - can implement secure boot features. 

Two ways we can realize TEE:
- ARM TrustZone, first and still used.
- Intel SGX, newer and has taken over more. 

## ARM TrustZone
Samsung uses it. To protect applications, keys, files,media content etc. 

Standard approach:
Uses protection rings with memory boundaries, two modes.
Privileged mode: OS and kernel services.
User mode: Applications runs here.
Protected by the MMU. 
Intel has similar rings but more than two. 

Cannot give good guarantees that the sensitive applications cannot be tampered b/c a lot of code is running in user mode and protection mode.
Their approach was:
Have two userspaces: normal and secure. 
Normal OS would not directly to use something in the secure space. We want to move from the normal world to the  secure world in a controlled way. The monitor is the "gatekeeper", controlling everyone who moves into the secure userspace. 

Introduced a bit on the buses, caches and pages, NS-bit, that tells if the data belongs to the secure or normal world. They also have hardware that controls the handling. 

To make the switch possible from normal to secure, they introduced a special instruction that is called the SMC, allows to do a context switch. Very simple, doesn't add that much hardware. 

Called a tagged architecture. 
TrustZone have secure interrupt. Can have a secure timer going off that checks the system. At that point, the normal world cannot intervene with the secure interrupt. Allows you to do some checking features that prevents the normal world to do a DoS-attack on the secure-world application. 

TrustZone embedded in CPU systems. DOesn't need that much software. Doesn't work exactly the same. There is technology to make even IoT devices secure. 

## Intel SGX - Software Guard eXtensions
An extension on a normal CPU. Creates enclaves, similar to (something I missed, perhaps rings?). 

Do a context switch into an enclave, but the thread itself must come from the normal mode. But when you're in the enclave, everything i sprotected. 
Enclaves are isolated memory regions where we can put coe and data. The EPC memory is encrypted. (Enclave Page Cache). 
Encryption is done by hardware-support, no software and integrated in the CPU Die.
The core trusted hardware(root of trust) is the chip itself. No app or operation sw involved. 

Normally we have the separation vertically between app space and privileged mode. Applications could not intervene with the privileged code, was a context switch. Have separations between the apps by the os. 
The problem here was that the privileged code could reach out to the app code.

This solution have an addition layer called the VMM between hardware and OS. Have an app that uses SGX to create an enclave. Lives now in the application. Is now a sensitive part. Part of the reason to design it like this that the OS will give a thread... 
Because the enclave doesn't come from the OS or the VMM but from the hardware, any malware that would exist in the OS or VMM or other apps cannot steal secrets from the enclave. Smaller attack surface, 

Wasn't possible before, no mechanisms to prevent it in TrustZone. 

In the enclave you will have code, data, and control structures to control the program running in the enclave. In the ARM you had the monitor controlling from secure to normal, here we have the Enclave entry- and exit points. Defines entry and exit points that you can communicate with the "outer world". 

EPC size is limited in the first version, unlimited in the next version. Another difference is that you can create many enclaves, each app can have 1 or 2 enclaves. As long as you have enough EPC you can create as many as you want, and they are all isolated. In ARM, you have only one trust and exection-environment. 

This does,however, not have a secure interrupt. Much more compilcated as we have runtime encryption and  integrity protected. 

When you have data that goes to the system memory, it have unencrypted data in CPU package. 

The enclaves lives like a backpack on the app. The enclave have call gates where we can nommunicate with the application. They are called ECALLs into the enclave and OCALLs from the enclave to the application. The thread that the enclave will execute on is from the app. 


### Life-cycle
You start your app with embedded enclave. HW will build the enclave environment. While it is built, it does some measurements on what we actually start with this enclave. Can do remote attestation to see what we actually started with. When the attestation is done, we can also do sealing/unsealing and software upgrades etc. Similar to TPM.


### Local vs remote attestation

Remote - very similar to TPM. Remotely interested to see what is running. We must know extrenally certificate. The app has an enclave, we send a request from challenger enclave to the app, which asks enclave for a report. We sign it with the quoting enclave, which is only for the purpose of signing the report. They can talk to each other with local attestation. The quote is sent to the challenger enclave, which can verify. 
Local attestation - happens only between two enclaves that lives on the same Die/chip. Will use the hardware key,they can derive a shared key that the can use to do a MAC signature instead of public key sign, makes it faster. 

You don't have this function in TrustZone, but here it is built in the hardware. 


### Identities
Normaly we associate with the identifier the credentials. The proof that you are the true owner. The binding between the credentials and identifier tells you that the securet belongs to you, in a namespace. 

There must be an issuer that binds you to it. 
Can be done in various ways. 

Zero-knowledge proof: 
Based on the discrete log that can be compute over prime numbers. If you know that y = g^x mod p, you want to prove without giving the value of x. The protocols that achieve this are called zero-knowledge proof. 

One example is EPID in SGX.
Creates something that is called group or public key. One public corresponds to multiple private keys. Each unique private key can be used to generate a signature. Signature can be verified with the group public key. An EPID signature is message + private key. 

Need to bind the credentials to the identifier. Each member gets an unique EPID private key by the issues. The group public key is given to a verifyer, and for every user we can use the public key. By having different members, you can hide who is doing the signature. You cannot distinguish the members from each other. 
You can get better privacy on using public key cryptography, when everyone has a separate public key. You can easily track people if everyone have a separate public key. EPID signatures are untraceable and anonymous. 
EPID construction is based on bilinear map functions. 

# Lect 7: Trusted Computing
Secure cryptoprocessors: 

## HSM
Dedicated microprocessor system with physical protection features: 
- Tamper-detecting and tamper-evident containment. 
- Automatic zeroization - all the secrets are wiped when opening. 
Etc. 

Smart cards are another type of cryptoprocessors, SIM etc.

HSM come in various sizes. They are very expensive. 
Gives high-grade protection and its purpose is to store critical information and keys. 

How do you know that these HSM is trustworthy? 
By certifications. FIPS 140-2 and CC-EAL are the most important.
FIPS: US standard on hardware equipment. 

## Security devices
### Smartcards
Has an interface in the chip. With this, you can communicate with the card. 
The communication goes through the standard procotol called APDU. 
You send a command into the card, and then the card will answer with a response. All communcation follows this pattern. You always send a command and you get the answer back. 

CAD - smart card acceptance devices.
Standardized by ISO. ISO 7816-4.
There are terminals and readers who communicate with the cards. 
Terminals: Have memory, logic, power. Like for ATMs and gas pumps. 
Readers: Connected to a computer. USB, serial, parallel port. 

The contacts are very simple. (Parts of the chip). Goes by a serial port interface. There are 8 contacts in java smartcards.

Instead of those physical you can have contactless interface. 
Power from CAD. Is a modulation, the magnetic field in the reader is used to power up the contactless card. Here it is important to avoid collisions, and there are some anti collision implemented. When multiple cards are close to the reader. 

Data transmission T=0 protocol:
Different standards that details how it should look like, T=0 is one of them. 
Is byte oriented. Standardises what commands are compulsory and optional. 


Attacks:
How can you attack these smartcards?

There are two inroads for attacks:
Traditional mathematical attacks:
- Algorithm modeled as ideal mathematical object. 
- Would typically generalize.
- In practice its seldom that this succeeds, mostly theoretical. 

Implementation attacks:
- Physical implementation is attacked:
    - By reverse engineering, open up the smartcard for example
    - Probing, make some active wire tapping on the smartcard
- Difficult to control
- Attacks are often operational, if it goes bad you can mount an attack on a card. 
- Specific and not generalized. 

Leakage attacks:
The cryptographic algorithm that runs on the card consume power and radiates heat etc. You can observe this and use these characteristics to deduct and compute the cryptographic key. 
    Simple power analysis:
    Attacker directly uses power consumption to learn bits of the secret key. Wave forms are visually examined. This is relatively easy to defend against. 
        Attacking modular exponentiation.
        When you implement RSA you have something called Square-and-Multiply. Can find the secret, the exponent, and used in simple power analysis.

### RFID

### NFC