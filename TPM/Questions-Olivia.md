# 3.1 - Environment setup
- Start the TPM1 and TSS and set up the env. variables
export TCSD_USE_TCP_DEVICE=true
export TCSD_TCP_DEVICE_PORT=6545
export TCSD_TCP_DEVICE_HOSTNAME=10.0.2.14
export TPM_SERVER_NAME=10.0.2.14

# 3.2 - Get TPM ready for use
## 3.2.2
1. Run `tpmbios` on TSS.
2. Run `sudo -E /usr/local/sbin/tcsd -e -f` on TSS.
3. Run `createek` , take print of the EK public key generated.
    This is the endorsement key (EK), and is delivered with the TPM normally. Is set in the manufacturing process. 
4. Run `takeown -pwdo opwd -pwds spwd`,
where ooo and sss are the passwords to the TPM owner and the SRK to take ownership of the TPM. Memorize the passwords.
    Creates the SRK, when taking ownership. 
    pwdo: opwd
    pwds: spwd
5. Which TPM command can be used to obtain the SRK public key in SRK.pub format (not PEM!)? Find the command, see appendix, that achieves this and read (public portion of) SRK from the TPM. Hint: handle of the SRK is 40000000
`ownerreadinternalpub -hk 40000000 -of srk.pub -pwdo opwd`

# 3.1 - Key hierarchy
## 3.3.2
1. The identity key is one type of signature key. Describe some differences between an identity
and a signature key.

Signing keys are asymmetric general purpose keys used to sign application data and messages. Signing keys can be migratable or non-migratable. Migratable keys may be exported / imported between TPM devices. The TPM can sign application data and enforce migration restrictions.

Identity keys are created and controlled by the TPM Owner only. 

2. Which keys can be used for file encryption?

Storage keys :  are asymmetric general purpose keys used to encrypt data or other keys. Storage keys are used for wrapping keys and data managed externally (outside a TPM). 

3. There is one type of key that exists, but its use is not  recommended. Which key is that, and why does it exist?

The TPM_KEY_LEGACY key type is to allow for use by applications where both signing and encryption operations occur with the same key.
## 3.3.3
- Generate keys according to the table in lab instructions (p.7). Use `createkey` and `identity` commands. 

```
A: createkey -kt e -pwdp spwd -pwdk apwd -ok A -hp 40000000
B: createkey -kt e -pwdp apwd -pwdk bpwd -pwdm bmpwd -ok B -hp 4EED94BC
C: createkey -kt s -pwdp bpwd -pwdk cpwd -ok C -hp 86269985
D: createkey -kt s -pwdp bpwd -pwdk dpwd -pwdm dmpwd -ok D -hp 86269985
E: createkey -kt b -pwdp bpwd -pwdk epwd -pwdm empwd -ok E -hp 86269985
F: createkey -kt s -pwdp apwd -pwdk fpwd -ok F -hp 4EED94BC
G: createkey -kt s -pwdp apwd -pwdk gpwd -pwdm gmpwd -ok G -hp 4EED94BC
H: identity -la H -pwdo opwd -pwds spwd -ok H
```

OBS! Keyhandles måste genereras på nytt för nästa försök.

- Make a drawing of the key hierarchy and motivate. 

All keys will have a parent which must be a storage key. SRK is the one that will be in the top of the hierarchy. 
    [Example](https://gyazo.com/dd76d5fbea728c57705e5da947363ba5), found [here on page 3](https://shazkhan.files.wordpress.com/2010/10/http__www-trust-rub-de_media_ei_lehrmaterialien_trusted-computing_keyreplication_.pdf)

- Look at the utility commands in the appendix section. The keys can be loaded into the TPM by using the command loadkey. When loading a key keep track of the key handle the TPM gives to the key.

loadkey -hp 40000000 -ik A.key -pwdp spwd

```
A-keyhandle: 4EED94BC
B-keyhandle: 86269985
C-keyhandle: -- NOT WORKING --
D-keyhandle: 9175ABD5
E-keyhandle: 41E0F29C
F-keyhandle: 0F55E3C8
G-keyhandle: D21D1D03
H-keyhandle: A868FDF1
```

# 3.4 - Key migration
## 3.4.2
1. Is it possible for a migratable key to be the parent of a non-migratable key?

Not for sign keys with storage key parent. "If parentHandle -> keyFlags -> migratable is TRUE and keyInfo -> keyFlags -> migratable is FALSE then return TPM_INVALID_KEYUSAGE" in `TPM_createwrapkey`.
OK for binding key with storage key parent (E).

2. Which command is the first to be executed when performing a key migration?

Validate that keyAuth authorizes the use of the key pointed to by maKeyHandle. 

3. Give a short description of the command TPM_ConvertMigrationBlob.

Takes a migration blob and creates a normal wrapped blob. Migrates private keys only. Decrypts with the storage key specificed in parentHandle.

4. Which TPM command loads the migrated keys into the TPM?

loadmigrationblob -hp <mig. key handle> -if <mig. blob filename> -pwdp <migration key password> [-rewrap]

5. Is it the TPM or the TSS that handles the transfer of the migration blob?


Hint: Use the document ”TPM Main Part 3 Commands” to find more information about the TPM commands.

## 3.4.3 Instructions for key migration in TPM emulator
- Follow instructions in lab assignment to setup TPM2. 
- Fix env. variables. 
- Restart `tcsd`-deamon after modified env. variables.
- After we migrated key B to TPM2 try to load key C, D, and E into TPM2. Explain what happens (why does it work or not work?).

Hints: Warning: when working with two TPMs it is advised to do that from different directories on the TSS machine. When issuing TPM commands files will be written in the directory from which you issue the commands and it may happen that you overwrite existing files.

## 3.4.4
1. Do the above migration and document in your report.
Setup om TPM2: 
- Changed env. variables.
- Run `tpmbios` and sudo-command on TSS
- `Ceateek`
- `takeown -pwdo o2pwd -pwds s2pwd`
- `ownerreadinternalpub -hk 40000000 -of srk.pub -pwdo o2pwd`
- create storage key and loadkey: 
    `createkey -kt e -pwdp s2pwd -pwdk a2pwd -ok A -hp 40000000`
    `loadkey -hp 40000000 -ik A.key -pwdp s2pwd`
    A-handle: 57AD82B2
- `migrate -hp 4EED94BC -pwdp apwd -pwdo opwd -im ../tpm2/A.key -pwdk a2pwd -pwdm bmpwd -ik B.key -ok migrationblob.bin` in TPM1.
- Cahnged env. variables again
- `loadmigrationblob -hp 57AD82B2 -pwdp a2pwd -if ../tpm1/migrationblob.bin`
- "Successfully loaded key into TPM.
New Key Handle = 559BC96E"
- Tries with D and E: (Could not create C-key)
 TPM1: 
 `migrate -hp 86269985 -pwdp bpwd -pwdo opwd -im ../tpm2/A.key -pwdk a2pwd -pwdm dmpwd -ik D.key -ok Dmigrationblob.bin` 
 `migrate -hp 86269985 -pwdp bpwd -pwdo opwd -im ../tpm2/A.key -pwdk a2pwd -pwdm empwd -ik E.key -ok Emigrationblob.bin` 
 TPM2:
`loadmigrationblob -hp 57AD82B2 -pwdp a2pwd -if ../tpm1/Dmigrationblob.bin`
`loadmigrationblob -hp 57AD82B2 -pwdp a2pwd -if ../tpm1/Emigrationblob.bin`
- D worked:
Successfully loaded key into TPM.
New Key Handle = 5FF70D03
- E worked:
Successfully loaded key into TPM.
New Key Handle = 37EEB4FE

2. There are other ways to migrate keys. When do you use a key of type TPM_KEY_USAGE = TPM_Migrate (Hint: look in [8])
    This table defines the types of keys that are possible. Each value defines for what operation the key can be used. Most key usages can be CMKs. See 4.2, TPM_PAYLOAD_TYPE. Each key has a setting defining the encryption and signature scheme to use. The selection of a key usage value limits the choices of encryption and signature schemes.
    This SHALL indicate a key in use for TPM_MigrateKey. 
3. What is the rewrap option of the migrate command used for?
    Used directly to move the key to a new parent (on either this platform or another). The TPM simply re-encrypts the key using a new parent, and outputs a normal encrypted element that can be subsequently used by a TPM_LoadKey command.
    Rewrap the key using the public key in migrationKeyAuth, keeping the existing contents of that key.

# 3.5 - Extending values to PCRs
## 3.5.2
1. Describe one TPM command that can be used to extend a SHA-1 digest to a PCR.
    TPM_SHA1CompleteExtend - This command is designed to complete a hash sequence and extend a PCR in memory-less environments.
    `sha1 -ic [data] -if [filename] -ix [index for PCR]`
2. Describe which TPM command that can be used to read a PCR value.
    TPM_PCRRead - returns the current contents of the named register to the caller. 

## 3.5.3
- Calculate SHA-1 digest of tpmbios, extend to PCR 11.
 `sha -if /usr/local/sbin/tcsd -ix 11` :
    SHA1 hash for file '/usr/local/sbin/tcsd': 
    Hash: c0a2ef976facd5e57c42c4ef46b7675994676b80
    New value of PCR: 9386032bd158a509920c7f4bae157eba2a2891f2

- Type `pcrread` when calculation is done and put it in the report.
`pcrread -ix 11`:
Current value of PCR 11: 9386032bd158a509920c7f4bae157eba2a2891f2

# 3.6 - File encryption

## 3.6.1
1. Why is TSS_Bind a TSS command, and not a TPM command?
2. Give some differences between Data binding and Data sealing.
3. Can a key used for data sealing be migrated to another TPM?
This structure is created during the TPM_Seal process. The confidential data is encrypted using a non-migratable key. When the TPM_Unseal decrypts this structure the TPM_Unseal uses the public information in the structure to validate the current configuration and release the decrypted data.

## 3.6.2 Data binding
- Ceate migratable binding key with `createkey` on TPM1.
    `createkey -kt b -pwdp apwd -pwdk bindpwd -pwdm bindmpwd -ok Bind -hp 4EED94BC`
- Encrypt a textfile with the .pem file created, `bindfile`. 
    `bindfile -ik Bind.pem -if textex.txt -of textexbind`
- Try to decrypt with `unbindfile`. Note that the command loadkey has to be executed before decryption is possible. Why doesn’t the key have to be loaded inside the TPM when encrypting, but it has to be when decrypting?
    We need the key handle, so the key needs to be loaded before we can unbind. Asymmetric decryption needs the public key.
did: `loadkey -hp 4EED94BC -ik Bind.key -pwdp apwd`
Got: New Key Handle = 7380D9B3
Did: `unbindfile -hk 7380D9B3 -if textexbind -of textexunbind -pwdk bindpwd`
Got: A new file containing the same as the textex.txt
- Migrate binding key to TPM2 and try to decrypt there too. Explain what happens. 
    * `migrate -hp 4EED94BC -pwdp apwd -pwdo opwd -im ../tpm2/A.key -pwdk a2pwd -pwdm bindmpwd -ik Bind.key -ok Bindblob.bin` 
    Wrote migration blob and associated data to file.
    Changed to TPM2:
    * `loadmigrationblob -hp 57AD82B2 -pwdp a2pwd -if ../tpm1/Bindblob.bin`
    Successfully loaded key into TPM.
    New Key Handle = 6B47297F
    * `unbindfile -hk 6B47297F -if ../tpm1/textexbind -of textexunbind2 -pwdk bindpwd`
    Worked! Got the same content in the textfile.


## 3.6.3 Data sealing
- Create storage key with `createkey` and `loadkey` into the TPM.
OBS! Made the keys migratable, doesn't work. Needed to make new ones. 
`createkey -kt e -pwdp apwd -pwdk storepwd -pwdm storempwd -ok Store -hp 4EED94BC`
`loadkey -hp 4EED94BC -ik Store.key -pwdp apwd`
New Key Handle = 45F11BCC
`createkey -kt l -pwdp apwd -pwdk legpwd -pwdm legmpwd -ok Leg -hp 4EED94BC`
`loadkey -hp 4EED94BC -ik Leg.key -pwdp apwd`
New Key Handle = E1678D63
_____________________________________
    * createkey -kt e -pwdp apwd -pwdk storepwd -ok StoreNoMig -hp 4EED94BC
    loadkey -hp 4EED94BC -ik StoreNoMig.key -pwdp apwd
    New Key Handle = BC24530A
    * createkey -kt l -pwdp apwd -pwdk legpwd -pwdm legmpwd -ok LegNoMig -hp 4EED94BC
    loadkey -hp 4EED94BC -ik LegNoMig.key -pwdp apwd
    New Key Handle = 948DE430


- Seal a textfile with `sealfile`.
    * Store:
    `sealfile -hk BC24530A -if textex.txt -of textexSealed -pwdk storepwd`
    Got:
    OK! 
    * Legacy:
    `sealfile -hk 948DE430 -if textex.txt -of textexSealedLeg -pwdk legepwd`
    Got:
    Error Invalid key usage from TPM_Seal, the same as when I tried with migratable keys.
    * Sign:
    `sealfile -hk 0F55E3C8 -if textex.txt -of textexSealedSign -pwdk fpwd`
    Got:
    Error Invalid key usage from TPM_Seal
    * Bind:
    `createkey -kt b -pwdp apwd -pwdk bindpwd -ok Bind -hp 4EED94BC`
    `loadkey -hp 4EED94BC -ik Bind.key -pwdp apwd`
    New Key Handle = 58FB356C
    `sealfile -hk 58FB356C -if textex.txt -of textexSealedBind -pwdk bindpwd`
    Error Invalid key usage from TPM_Seal

- Unseal the file with `unsealfile`.
    `unsealfile -hk BC24530A -if textexSealed -of textUnsealed -pwdk storepwd`
    Worked!
    
- Test if you can do it with: (Why/why not?)
    - Legacy key: Error to seal. 
    - Binding key: Error with seal. 
    - Signing key: Error to seal.
- Migrate the storage key to TPM2 and try to unseal. What happens?
    According to documentation, you can't have a migratable storage key to seal with:
    "If the keyHandle points to a migratable key then the TPM MUST return the error code
    TPM_INVALID_KEY_USAGE.", page 3 of part 3 - Commands. 

# 3.7 TPM Auth

## 3.7.2
1. In the above, could the `verifyfile` command have been done by another TPM?
2. Which TPM command is used to decrypt the file?
3. Can the decryption based authentication be done by using data sealing instead of binding?

## 3.7.3
- Document the following in the report:
    1. Sign a file with some text in it by loading a signature key into the TPM1 and use this key to
    sign the file using the utility `signfile`. Let TPM2 verify the signature by using the utility
    `verifyfile`. 
    2. Encrypt a file by creating a binding key and load it into the TPM and then encrypt a text
    file using the command `bindfile` Then decrypt it using the command `unbindfile`.

# 3.8 - Attestation

## 3.8.1 Signature based
- Create an AIK with `identity`.
- Use it to quote a PCR value, like hash digest of tpmbios.
Hints: 
`identity -pwdo <owner password> -la <a label> -pwds <SRK password> -ok <key filename>`
`quote -v -hk <key handle in hex> -bm <pcr hash digest> -pwdk <key password> `
- Document in the report. 
- Note: because the bash shell will hijack your quote command you should instead of just quote enter the full path of the quote command, i.e. /home/tss/tpm/tpm4720/libtpm/utils/quote.

## 3.8.2 Decryption based
- Create a text file and extend the hash digest to a PCR. 
- Create a storage key and bind it to the PCR value using the command `createkey` (-ix is used to specify the PCR index). 
- Load the key into the TPM. 
- Seal the text file using the storage key with the command `sealfile`. Unseal the file using the command `unsealfile` (Should be successful).
- Change the text in the text file and extend the PCR with the new hash digest of the text file. 
- Try decrypt the file again (should not work, PCR value bound to the storage key has changed). 
- Clear ownership of the TPM using the command `forceclear`.
- Document the steps in your report.
