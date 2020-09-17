# Object Security

## Preparations:
* Read paper by Selander, obj sec. for IoT ( http://www.eit.lth.se/fileadmin/eit/courses/eitn50/Project_ObjSec/protected/Application_Layer_Security_Protocols_for_IoT.pdf ).
  Summary: IoT devices ar constrained in terms of data rates, memory, power, bandwidth etc. They also have a need for a secure protocol, sine they can contain sensitive data. The demands of constrained devices and networks have led to a demand for new internet protocols. An example that is brought up in the paper is the CoAP, similar to HTTP but adapted to constrained environments. 
  The trade-off for these protocols adapted to constrained environments is non-security based, so no security is lost compared to protocols in a non-constrained environment. 
  Some of the demands on the security protocol is presented below:
    * Since transmitting & listening for messages may consume large amounts of energy, we need to restrict the budget in terms of message size and number of messages exchanged. 
    * IoT are not always reachable, since they can go to an idle state. Intermediary nodes like proxies perform load-balancing or store-and-forward tasks, which are used to support settings of intermittent connectivity. Performing these functionalities requires the proxy to read or change the message metadata, which has consequences on end-to-end security including privacy. 
    * Maintaining state in a device has a cost, both in terms of writing the state information to persistant memory. Security protocols need to consider the effect of losing state and restarting to prevent attack vectors based on power loss. 
    * A constrained device may not be capable of maintaining a synchronized time, which impacts the ability to verify validity of assertions, like certificates or access control policies. Each device will almost certainely have a clock, they require less power than the natural discharge of batteries. Since they can drift, there is a need for the security protocols to provide freshness information.
  Security at different layers and what they protect:
    * Link layer: Early rejection of invalid messages, reducing unnecessary processing and mitigation DoS-attacks. Link layer security protects one hop in the communcation between endpoints and not the session as a whole.
    * Transport layer: Like TLS/DTLS. Default security solution on the internet. Messages are protected across different links, but since the transport layer decrypts information from the application layer, proxies can't read the metadata from the application layer protocol. 
    * Application layer: If the security is applied here, the message can be sent over different transport protocols (UDP, TCP etc.). Two different versions of application layer security:
      * Only the application payload is protected. Here, intermediate nodes can read and write to the metadata. If the information that needs to be protected is inside the payload, then this will be a good solution. One example is encapsulating with JOSE/COSE. (This should be the case for B-assignments?)
      * Payload and metadata are protected. The security protocol can be designed to balance between making the app layer payload useable by proxies, and at the same time protect sensitive metadata between the endpoints. One example is the use of OSCOAP with CoAP. 
    Other principles:
      * Use optimized primitives whenever possible. CBOR for encoding, COSE for secure message formatting and CoAP for messaging is a good way to go. 
      * Reuse primitives to save on code space. 
      * Reduce the number of options in the protocols to enable lower complexity implementations. Reduces code size and risk for errors. 
  Existing technologies:
    CBOR
      Similar to JSON data model. Encoding and decoding with a small code size. Adapted to constrained environments and have some advantages compared to JSON. 
    CoAP
      RESTful web protocol for constrained environments, especially machine-to-machine apps. Have built-in support for multicast and asynchronous message exchange. Have proxy and caching capabilities. Have low message overhead. Have a major advantage over HTTP. Designed for UDP. 
  Security protocols: 
    COSE
      Uses CBOR. Provides secure wrapping of data. Describes how to create and process encryption, signatures and message authentication codes. 
    OSCOAP
      Defines a way to secure the CoAP communication between two endpoints in the presence of untrusted intermediaries. Sensitive parts of the message are encrypted with COSE,

* Read about forward security (https://scotthelme.co.uk/perfect-forward-secrecy/)
  Summary: Perfect Forward Secrecy assures that your session keys will not be compromised even if the private key of the server is compromised. The server generates a new session key for every session with a user, so a leaked session key can't affect other sessions. Should be used by everyone who uses TLS/SSL.
  Your key exchange has to be Ephermal:
    The client and server generates new Diffie-Hellman parameters for each session. The parameters should never be re-used or stored

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
  Api Docs: https://www.dlitz.net/software/pycrypto/api/current/