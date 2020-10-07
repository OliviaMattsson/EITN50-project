# Lecture 8 - part 2

## Project and quiz updates
There are instructions for VirtualBox environment on Canvas. Reading instructions for the next quiz are up as well. Introduction for the last project will be given in a lecture, could be good to attend that one. 

## SELINUX
Secure Linux. 
In a normal OS you have DAC. In a normal Linux, the root user is a powerful. You could take over the computer by getting access to the root user. 

In a MAC system, the premissions are set system wise. Allows you to define permissions for how all processes, subjects, interact with other parts of the system such as files etc, called objects. 

The purpose is to minimize the privilegies for the users. 

### SELinux Concepts
The rights of a process depends on its security process. Like the user role, the identity of the user who started the process, and the domain that the user carried in that time. 
Transitions between domains are controlled by the roles. 

**MLS**
Multi-Level Security. 
Composed of 4 parts, high/low and sensitivity/category. 
There is a hierarchy defined how these levels gives premissions. Is a variation of Bell-La Padula. 

### Architecture
Based on the Linux Kernel, is Linux with additional features. 
Introduces an extra module, LSM. Provides a hook for additional security checks. Usually placed after DAC checks. 
The SELinux isn't always called - if DAC denies access then it is no need to use SELinux. 
The logging and autiding could be difficult. Is the access violation in MAC or DAC?

What does it do?

In the LSM module(yellow p.62) uses a packaging of the file system. You have a policy, a set of rules that describe how subjects can access objects. These policies are used in the sucrity server. Puts the decision in an Access Vector Cache. The evaluations are stored there and you can speed up processes by checking the AVC. 

LSM - the heart of the SELinux. 

### Policy Language
You need to set policies for everything that runs in the system. There are three policies defined:
- Strict
    Every subject and object exists in a specific security domain
- Targeted: 
    Every subject and object runs in the unfonfined_t domain except for the specific targeted daemons. Undefined domain have no restrictions, uses the standard.
- Multi-Level Security
    Like strict but you can have levels, and have capability to express what needs to be done. Not used very often. 

SELinux modes: 
- Enabled
    Enabled-Enforcing: Fully functioning
    Enabled-Permissive: Have SELinnux enabled, but if a rule is violated there is no blocking, but there will be a logging event. Commonly used during development, to check. 
- Disabled
    SELinux support not available in the kernel, applications will load differently. 

### Why run SELinux?
Isolation! Use the policy rules to create better policy rules to applications. Limit the capabilities of the root user. Loads at start, enforces the kernel to work with these policies. Before OS start. 
Good to protect the kernel from break-ins. Use this extra isolation to limit an escalation, when a server crashes. 

## Why not run SELinux?
The policy file is difficult to create. You need to tweak it for each new application that uses system resources. 
SELinux breaks your code - doesn't like text relocation. Will not allow it in enforcing mode. Can be allowed by applying special rules on the code file. 

### Alternatives
Alternatives that all use the LSM machinery, but the way that the policies and how the LSM should work is different.
- AppArmor
    Implements a pathbased MAC, unlike SELinux which is based on applying labels, attributes, to files. Have an idea how to group policies together based on the file path.  
    Standard in Ubuntu.

- Simple MAC Kernel
    Also have MAC using labels attached to tasks and data containers.

### IMA 
Idea is to detect if files have been altered, both remotely and locally:
- Collect
- Store
- Attest  
- Protect
If we detect some deviations, we can raise an error or stop the whole system. Policy choice. 

## UNIX CONTAINERS (LXC)
Using the VM to create isolation. VM have control of the MMU. Each VM has its own OS. Is it really necessary? 
The motivation of developing containers. 

p.84 : Bare metal case:
Host OS are running on top of the hardware. We add an additional layer to have container's engine there. Then we have containers that contains applications, databases etc. THrough the container engine we provide Kernel namespaced, virtual ethernet connections etc. Allows us to create a kind of VM, much less code for the containers. 

The isolation between the containers is less good than the isolation via VMs. Container-based solutions are less secure than the VM solution. Can have additional separation, adding thes host OS and containers in the VM. 

## Trusted computing in Android-OS and IOS

### Android
p.94
Two applications that together form a user application. A search and a map. Using components that interact with each other. 

#### Access control
Using a multi-user Linux OS.
Inter-components have communication and they need permission for it. Have some SELinux features.

Each application runs as an unique Linux user. The isolation is the same as two different users on a normal OS. Runs under its unique User-ID that is set during the installation of the application. 

There are some reserved IDs, apps get User-ID >= 10 000. 

After the User-ID is set in the installment, they also gets a part of a file system. Like Usr/home/FoxPositioner and Usr/home/FoxMap. 
In a normal OS, these cannot reach each other unless they are given permissions to do so explicitly.

The applications in Android are signed. A signed application meant in Java is that you know who signed it. A trusted app was signed by a ceritified user, in the certification. 
In Android, only to assure that the User-ID is unique. It is signed, therefore it was given a User-ID. Mainly to keep the applications apart. Signed by self-certificate. Two applications can share the same User-ID if they are signed using the same key/certificate. 

#### Runtime protections
- ASLR: Randomizes the address space. Makes it much harder to use buffer overflow attacks. The fourth project shows that even if you have ASLR, it cannot fully solve buffer overflow attacks. 

- ARM NX: Uses ARM type CPUs, the not execute feature for data reduces risk of exploits of 

- DM-VERITY: Block-level (block oriented storage) integrity protection solution for read-only partitions. Used on storage devices. Uses a hash-tree. Calculates a hash of every block, and for every block in each layer. If you want to update something, you only walk up to the tree and update that part. 

### IOS in comparison to Android

#### IOS Sandboxing
Not based on Linux system, but similar. 
All applications in IOS run as user "mobile". 

#### Built-in trusted root
Build in. Have a root key that is used in implementing a secure boot process. Support different boot modes. 
- Normal boot: Boot ROM -> LowLevelBoolloader -> lboot -> Kernel
- Recovery mode: Fail-safe option in the lboot that allows uploading of a RAM disk and reflashing of the device.
- DFU mode: Fall-back, allows to restore from a given boot state.

The difference to Android is that the secure boot isn't really specified. In IOS, it is an integrated part of the system.

### Can we trust smartphones?
The applications are the problem. 