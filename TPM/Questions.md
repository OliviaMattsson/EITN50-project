# 3.1 - Environment setup
- Start the TPM1 and TSS and set up the env. variables

# 3.2 - Get TPM ready for use
## 3.2.2
1. Run `tpmbios` on TSS.
2. Run `sudo -E /usr/local/sbin/tcsd -e -f` on TSS.
3. Run `createek` , take print of the EK public key generated.
    This is the endorsement key (EK), and is delivered with the TPM normally. Is set in the manufacturing process. 
4. Run `takeown -pwdo ooo -pwds sss`,
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
3. There is one type of key that exists, but its use is not  recommended. Which key is that, and
why does it exist?
    The TPM_KEY_LEGACY key type is to allow for use by applications where both signing and encryption operations occur with the same key.
## 3.3.3
- Generate keys according to the table in lab instructions (p.7). Use `createkey` and `identity` commands. 
    A: createkey -kt e -pwdp spwd -pwdk apwd -ok A -hp 40000000
    B: createkey -kt e -pwdp apwd -pwdk bpwd -pwdm bmpwd -ok B -hp D86C163F
    C: createkey -kt s -pwdp bpwd -pwdk cpwd -ok C -hp 0D851F37
    D: createkey -kt s -pwdp bpwd -pwdk dpwd -pwdm dmpwd -ok D -hp 0D851F37
    E: createkey -kt b -pwdp bpwd -pwdk epwd -pwdm empwd -ok E -hp 0D851F37
    F: createkey -kt s -pwdp apwd -pwdk fpwd -ok F -hp D86C163F
    G: createkey -kt s -pwdp apwd -pwdk gpwd -pwdm gmpwd -ok G -hp D86C163F
    H: identity -la H -pwdo opwd -pwds spwd -ok H

OBS! Keyhandles måste genereras på nytt för nästa försök.

- Make a drawing of the key hierarchy and motivate. 
    All keys will have a parent which must be a storage key. SRK is the one that will be in the top of the hierarchy. 
    [Example](https://gyazo.com/dd76d5fbea728c57705e5da947363ba5), found [here on page 3](https://shazkhan.files.wordpress.com/2010/10/http__www-trust-rub-de_media_ei_lehrmaterialien_trusted-computing_keyreplication_.pdf)
- Look at the utility commands
in the appendix section. The keys can be loaded into the TPM by using the command loadkey. When loading a key keep track of the key handle the TPM gives to the key.
    A-keyhandle: D86C163F
    B-keyhandle: 0D851F37
    C-keyhandle: --NOT WORKING--
    D-keyhandle: --NOT WORKING--
    E-keyhandle: E13DCD2D
    F-keyhandle: E4F7E4A7
    G-keyhandle: 0E19221C
    H-keyhandle: 2701AD26

# 3.4 - Key migration
## 3.4.2
1. Is it possible for a migratable key to be the parent of a non-migratable key?
    Not for sign keys with storage key parent. "If parentHandle -> keyFlags -> migratable is TRUE and keyInfo -> keyFlags -> migratable is FALSE then return TPM_INVALID_KEYUSAGE" in TPM_createwrapkey.
    OK for binding key with storage key parent (E).
2. Which command is the first to be executed when performing a key migration?
    Validate that keyAuth authorizes the use of the key pointed to by maKeyHandle. 
3. Give a short description of the command TPM_ConvertMigrationBlob.
    Takes a migration blob and creates a normal wrapped blob. Migrates private keys only. Decrypts with the storage key specificed in parentHandle.
4. Which TPM command loads the migrated keys into the TPM?
    lloadmigrationblob -hp <mig. key handle> -if <mig. blob filename> -pwdp <migration key password> [-rewrap]
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
2. There are other ways to migrate keys. When do you use a key of type TPM_KEY_USAGE = TPM_Migrate (Hint: look in [8])
    This SHALL indicate a key in use for TPM_MigrateKey. 
3. What is the rewrap option of the migrate command used for?
    Used directly to move the key to a new parent (on either this platform or another). The TPM simply re-encrypts the key using a new parent, and outputs a normal encrypted element that can be subsequently used by a TPM_LoadKey command.
    Rewrap the key using the public key in migrationKeyAuth, keeping the existing contents of that key.

# 3.5 - Extending values to PCRs
## 3.5.2
1. Describe one TPM command that can be used to extend a SHA-1 digest to a PCR.
    TPM_SHA1CompleteExtend - This command is designed to complete a hash sequence and extend a PCR in memory-less environments
2. Describe which TPM command that can be used to read a PCR value.
    TPM_PCRRead - returns the current contents of the named register to the caller. 

## 3.5.3
- Calculate SHA-1 digest of tpmbios, extend to PCR 11. 
- Type `pcrread` when calculation is done and put it in the report.

# 3.6 - File encryption

## 3.6.1
1. Why is TSS_Bind a TSS command, and not a TPM command?
2. Give some differences between Data binding and Data sealing.
3. Can a key used for data sealing be migrated to another TPM?

## 3.6.2 Data binding
- Ceate migratable binding key with `createkey` on TPM1.
- Encrypt a textfile with the .pem file created, `bindfile`. 
- Try to decrypt with `unbindfile`. Note that the command loadkey has to be executed before decryption is possible. Why doesn’t the key have to be loaded inside the TPM when encrypting, but it has to be when decrypting?
- Migrate binding key to TPM2 and try to decrypt there too. Explain what happens. 

## 3.6.3 Data sealing
- Create storage key with `createkey` and `loadkey` into the TPM.
- Seal a textfile with `sealfile`.
- Unseal the file with `unsealfile`.
- Test if you can do it with: (Why/why not?)
    - Legacy key:
    - Binding key:
    - Signing key:
- Migrate the storage key to TPM2 and try to unseal. What happens?

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