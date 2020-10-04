# 3.2.2
3. In the third step the EK keypair will be created.  When using the emulator the EK has tobe created by the user. This is done by using the utility `createek`. Keep an eye on the TPM emulator terminal when the command `createek` is executed. The EK public key will be printed to the terminal.
```
TPM_State_Trace: disable 0 p_deactive 0 v_deactive 0 owned 0 state 2
 TPM_IO_Write: length 314
 00 C4 00 00 01 3A 00 00 00 00 00 00 00 01 00 03 
 00 01 00 00 00 0C 00 00 08 00 00 00 00 02 00 00 
 00 00 00 00 01 00 D0 4E 62 E2 A3 F2 C8 D9 42 6B 
 A2 6C 5F 1D 45 25 B9 4F 12 D6 09 49 03 58 C7 B0 
 82 DE 2F D0 2F C5 2A 75 BC 90 85 39 E3 2F 4F 92 
 AC 11 18 5A E8 D9 5A 00 0F 10 8A 26 1A 47 74 2F 
 D5 94 32 63 5D 94 12 4E 50 F5 9D C7 B2 4D 75 C4 
 8D 77 95 2A 12 EA 2A 1F 06 AB 9D 31 17 02 18 D5 
 1F C7 23 FA 03 B8 42 BC 0E DE 4B 84 54 28 87 52 
 C3 19 5E 36 76 A4 3B 17 D6 FE 11 9F 01 1B FD 71 
 7D B6 09 77 F8 0E 71 5F 3D EA 73 16 FF 32 B2 5C 
 86 23 23 0A 97 EF F8 FB CE 52 12 04 8A 38 3B EF 
 2F D0 A3 2F 7C 26 6D 4B DD 73 84 E6 01 28 D4 16 
 C3 97 D2 C5 8A 34 86 27 66 BD 0B A6 51 EA A0 2C 
 3A 4A 5D A8 D3 AB A0 A2 D8 F3 01 0B 3C 85 25 BD 
 F0 98 7C A3 07 2D 3D 78 C7 2B 1F 4F 78 A3 80 CC 
 CA 68 0D 09 4D 36 11 65 79 73 8D C9 79 E6 0D E3 
 F1 67 81 B6 0D 70 67 59 4D 3F 6D A3 05 27 A3 32 
 29 38 7F F2 4D 3D 46 7D F3 25 A8 80 6B F7 40 96 
 6D 3F A2 2C 6D 00 A9 33 83 A3 
TPM_IO_Connect: Waiting for connections on port 6545
```

4. The next step is to take ownership of the TPM. This will create the SRK and set a `password` to the TPM and the SRK. The utility for taking ownership is `takeown -pwdo ooo -pwds sss`,where `ooo` and `sss` are the passwords to the TPM owner and the SRK. These passwords canbe set to other values by the user.
```
takeown -pwdo ooo -pwds sss
```

5. Which TPM command can be used to obtain the SRK public key in `SRK.pub` format (not PEM!)?  Find the command, see appendix, that achieves this and read (public portion of)SRK from the TPM.
```
ownerreadinternalpub -hk 40000000 -of srk.pub -pwdo ooo
```

# 3.3.2

1. The identity key is one type of signature key.  Describe some differences between an identity and a signature key.

**FIXME**

2. Which keys can be used for file encryption?

Storage keys.

3. There is one type of key that exists, but its use is not recommended.  Which key is that, andwhy does it exist?

Legacy keys.

# 3.3.3

Create keys with `createkey`. Then use `loadkey -hp parent <name>.key` to get their handle.
```
SRK_HANDLE=40000000

# A
createkey -kt e -pwdp sss -pwdk aaa -ok A -hp $SRK_HANDLE
loadkey -hp $SRK_HANDLE -ik A.key -pwdp sss
A_HANDLE=#output of prev command

# B
createkey -kt e -ok B -hp $A_HANDLE -pwdm mmm -pwdk bbb -pwdp aaa
loadkey -hp $A_HANDLE -ik B.key -pwdp aaa
B_HANDLE=#output

# C
createkey -kt s -ok C -hp $B_HANDLE -pwdk ccc -pwdp bbb
# Does not work! FIXME: WHY?

# D
createkey -kt s -pwdk ddd -pwdp bbb -pwdm mmm -ok D -hp $B_HANDLE
loadkey -hp $B_HANDLE -ik D.key -pwdp bbb
D_HANDLE=#out

# E
createkey -kt b -pwdk eee -pwdp bbb -pwdm mmm -ok E -hp $B_HANDLE
loadkey -hp $B_HANDLE -ik E.key -pwdp bbb
E_HANDLE=#out

# F
createkey -kt s -ok F -hp $A_HANDLE -pwdp aaa
loadkey -hp $A_HANDLE -ik F.key -pwdp aaa
F_HANDLE=#output

# G
createkey -kt s -pwdk ggg -pwdm mmm -ok G -hp $A_HANDLE -pwdp aaa
loadkey -hp $A_HANDLE -ik G.key -pwdp aaa
G_HANDLE=#output

# H
identity -la H -ok H -pwds sss -pwdo ooo
loadkey -hp $SRK_HANDLE -ik H.key -pwdp sss
H_HANDLE=#out
```

# 3.4.2

1. Is it possible for a migratable key to be the parent of a non-migratable key?

No. 

2. Which command is the first to be executed when performing a key migration

TPM_
The creation of the migration blob, `migrate`.

3. Give a short description of the commandTPM_ConvertMigrationBlob.

The migration blob is converted to a wrapped blob. That is, it can be used by the loadkey command directly.

4. Which TPM command loads the migrated keys into the TPM?

5. Is it the TPM or the TSS that handles the transfer of the migration blob?

bör väl vara tss som hämtar från tpm1 och sen skickar till tpm2?

# 3.4.4

1. Do the above migration and document in your report.
TPM2

```
TPM_State_Trace: disable 0 p_deactive 0 v_deactive 0 owned 0 state 2
 TPM_IO_Write: length 314
 00 C4 00 00 01 3A 00 00 00 00 00 00 00 01 00 03 
 00 01 00 00 00 0C 00 00 08 00 00 00 00 02 00 00 
 00 00 00 00 01 00 D3 4E 32 01 09 FB C8 50 94 7F 
 BE 06 4E F7 43 1D 07 03 59 D4 65 35 04 31 E0 7A 
 87 0D 6E A0 11 4C FC BF 55 3F DE 56 40 AA 96 9F 
 D1 CA 4A 79 A3 D6 71 65 7D AF FA 91 51 45 36 3A 
 54 7B BE 7D 9C EC DB 5A AB 93 72 16 D5 56 9B 5C 
 04 4E 7A E7 F6 CE 95 BD 54 EA D8 04 D0 74 A7 D9 
 5C 6B B6 1C 0C B9 5F 16 93 00 9E D1 DE 44 6B 7F 
 00 4F F9 0C 25 0C 80 8B 25 A1 51 4F CD 25 3F DC 
 23 96 C5 4E 81 00 46 75 F8 D2 49 6B 7D 99 9C 40 
 B3 1E C3 BE F4 0C D3 22 5C A9 CF 66 90 AC 93 A2 
 B6 54 CC A9 04 54 EE 0A AA 62 70 EB 85 A1 07 46 
 E3 BA 5C CF F3 4A 66 5E A7 C9 8E C6 A9 AE D8 61 
 17 C4 DE 08 CE BE F6 22 57 59 D1 BC 43 EE F2 8E 
 A2 D7 D4 0E C0 28 D1 F9 16 FB 98 E8 F5 AA 03 0A 
 C2 A0 05 42 2C BB 89 7E 9D 55 2E BB 9C CF B8 AA 
 CD 3B 46 67 58 9F 27 BF 07 89 A1 F3 56 5D 0D A3 
 48 B1 36 13 08 51 3F 26 22 A2 B6 AD 6D 5F 31 80 
 20 C0 BB 1B CD DD A9 E2 FD 37 
TPM_IO_Connect: Waiting for connections on port 6545
```

```
# TPM1
migrate -hp $A_HANDLE -pwdp aaa -pwdo ooo -im ../tpm2/A.key -pwdk aaa -pwdm mmm -ik B.key -ok migrationblob.bin

# TPM2
loadmigrationblob -hp $A_HANDLE -pwdp aaa -if ../tpm1/migrationblob.bin
```

2. There are other ways to migrate keys.  When do you use a key of typeTPM_KEY_USAGE=TPM_Migrate(Hint:  look in [8])


3. What is the rewrap option of the migratecommand used for?
ReWrap mode is used directly to move the key to a new parent (on either this platform oranother). The TPM simply re-encrypts the key using a new parent, and outputs a normal encrypted element that can be subsequently used by a TPM_LoadKey command.

# 3.5

### 3.5.2

1. Describe one TPM command that can be used to extend a SHA-1 digest to a PCR.
`sha`.
2. Describe which TPM command that can be used to read a PCR value
`pcrread`

```
$ sha -if ../tpm/tpm4720/libtpm/utils/tpmbios -ix 11
SHA1 hash for file '../tpm/tpm4720/libtpm/utils/tpmbios': 
Hash: 55ac0462404445623f38fdae9adf87d487125874
New value of PCR: dba8c73876627a1e4439627b64c96c8f9c8d404a

$ pcrread -ix 11
Current value of PCR 11: dba8c73876627a1e4439627b64c96c8f9c8d404a
```

# 3.6
### 3.6.1

1. Why is TSS_Bind a TSS command, and not a TPM command?

Bind encrypts using the public portion of a bind key and can only be decrypted by the TPM.

2. Give some differences between Data binding and Data sealing.

Data binding is sending encrypted data to the TPM. When sealing you encrypt data as well as telling TPM the required state of one or more registers in order to be able to decrypt the data. For example, a computer could store its current state as a PCR and only be able to decrypt certain data during boot.

3. Can a key used for data sealing be migrated to another TPM?
Nope

### 3.6.2

```
createkey -kt b -pwdk enc -pwdp bbb -pwdm mmm -ok encryption -hp $B_HANDLE

bindfile -ik encryption.pem -if kryptera.txt -of krypterad

loadkey -hp $B_HANDLE -ik encryption.key -pwdp bbb
ENC_HANDLE=#output

unbindfile -hk $ENC_HANDLE -if krypterad -of dekrypterad.txt -pwdk enc
```

The public key is available outside the TPM but the private key is not. Therefore the public key needs to be loaded (in order to get a handle to reference the private key) for decryption.

```
# TPM1
migrate -hp $B_HANDLE -pwdp bbb -pwdo ooo -im ../tpm2/A.key -pwdk aaa -pwdm mmm -ik encryption.key -ok binding_migrationblob.bin

# TPM2
loadmigrationblob -hp $A_HANDLE -pwdp aaa -if ../tpm1/binding_migrationblob.bin
```

The binding key is transferred and the data is decrypted just as before. The results of `unbindfile` are the same.

### 3.6.3

```
createkey -kt e -pwdk storage -pwdp aaa -ok storage -hp $A_HANDLE
loadkey -hp $A_HANDLE -ik storage.key -pwdp aaa
STORAGE_HANDLE=#output

sealfile -hk $STORAGE_HANDLE -if kryptera.txt -of sealed -pwdk storage
unsealfile -hk $STORAGE_HANDLE -if sealed -of unsealed.txt -pwdk storage
```

Per the documentation.
> If the keyUsage field of the key indicated by keyHandle does not have the value TPM_KEY_STORAGE, the TPM must return the error code TPM_INVALID_KEYUSAGE.
> If the keyHandle points to a migratable key then the TPM MUST return the error codeTPM_INVALID_KEY_USAGE.

That is, the key cannot be migrated and the key must be of type storage.

# 3.7

### 3.7.1

1. In the above, could the `verifyfile` command have been done by another TPM?

Yes, the data needed to verify a signature is: the signature itself, the data and the public key of the signing party.

2. Which TPM command is used to decrypt the file?

`unbindfile`

3. Can the decryption based authentication be done by using data sealing instead of binding?

Yes, but the sealing as well as the unsealing requires the use of the TPM and knowing the handle of the storage key used to encrypt the data.

One could for example seal a file during the setup of a TPM and then keep it secured and use only for authenticating the TPM afterwards. Given that the storage key handle is still known.

### 3.7.3

```
# TPM1
signfile -hk $G_HANDLE -if kryptera.txt -os krypt_sign -pwdk ggg

# TPM2
verifyfile -is ../tpm1/krypt_sign -if ../tpm1/kryptera.txt -ik ../tpm1/G.pem
```

```
bindfile -ik E.pem -if kryptera.txt -of krypterad_bind

unbindfile -hk $E_HANDLE -if krypterad_bind -of avkrypterad_bind -pwdk eee
```

## 3.8

### 3.8.1

```
identity -pwdo ooo -la AIK -pwds sss -ok AIK
loadkey -hp $SRK_HANDLE -ik AIK.key -pwdp sss
AIK_HANDLE=#out

/home/tss/tpm/tpm4720/libtpm/utils/quote -v -hk $AIK_HANDLE -bm 55ac0462404445623f38fdae9adf87d487125874

    TPM_Send: GetCapability
    TPM_TransmitSocket: To TPM [GetCapability] length=22
    00 C1 00 00 00 16 00 00 00 65 00 00 00 05 00 00 
    00 04 00 00 01 01 
    TPM_ReceiveSocket: From TPM length=18
    00 C4 00 00 00 12 00 00 00 00 00 00 00 04 00 00 
    00 18 

    TPM_Send: GetCapability
    TPM_TransmitSocket: To TPM [GetCapability] length=22
    00 C1 00 00 00 16 00 00 00 65 00 00 00 05 00 00 
    00 04 00 00 01 10 
    TPM_ReceiveSocket: From TPM length=18
    00 C4 00 00 00 12 00 00 00 00 00 00 00 04 00 00 
    00 03 

    TPM_Send: GetCapability
    TPM_TransmitSocket: To TPM [GetCapability] length=22
    00 C1 00 00 00 16 00 00 00 65 00 00 00 07 00 00 
    00 04 00 00 00 01 
    TPM_ReceiveSocket: From TPM length=28
    00 C4 00 00 00 1C 00 00 00 00 00 00 00 0E 00 03 
    A8 78 3A FD 28 29 35 EF A7 89 21 44 

    TPM_Send: SaveContext
    TPM_TransmitSocket: To TPM [SaveContext] length=34
    00 C1 00 00 00 22 00 00 00 B8 A8 78 3A FD 00 00 
    00 01 DD 65 C1 B4 B3 E6 6E 76 55 23 87 3B D2 9C 
    F5 D6 
    TPM_ReceiveSocket: From TPM length=616
    00 C4 00 00 02 68 00 00 00 00 00 00 02 5A 00 01 
    00 00 00 01 A8 78 3A FD DD 65 C1 B4 B3 E6 6E 76 
    55 23 87 3B D2 9C F5 D6 00 00 00 00 0F 40 59 C5 
    A9 94 D0 5D 18 EF 3D 75 96 A6 7C 18 7E 66 6B D4 
    00 00 00 00 00 00 02 20 24 91 B3 10 C0 82 0E BB 
    4F 31 4D E2 46 6C 0E D0 CA 17 F1 EE F3 64 8A 09 
    5B 0F B8 89 3D AA 1D DC 60 A2 C1 13 45 FF B6 39 
    4F 62 3D 42 03 B2 22 5D B1 9A 2E A8 47 F8 4B 64 
    EC A3 3D 18 FF CC 31 AC 75 37 24 EF F8 D7 84 A2 
    54 64 53 80 55 09 47 EA 8F 9F 5F 94 CB 60 BF C1 
    59 E4 EB C7 2D 1A 1B E7 B1 83 40 91 0B 65 DE 24 
    02 C5 0C 49 61 8F 50 11 CC C0 85 3C 61 86 BC 93 
    44 4C 32 42 37 EE 97 A7 DE 64 D5 53 B0 8B 73 5C 
    71 0D 52 C2 BF 9E 3A 12 23 0F 9B 25 2E 11 5A 19 
    EE EF 32 E8 1C A8 23 1B 54 CA D3 06 81 B0 46 3A 
    37 92 90 ED EE 8D 22 A0 B4 2D FC D9 32 D8 38 22 
    74 FA FE 2C D9 3D 24 0C D1 47 BC 93 F9 16 BF F8 
    38 74 77 B3 3E BC 84 2F C4 29 F4 73 A0 51 44 6C 
    8C AB 2D 12 0C 21 C4 19 DF B4 F0 69 34 27 A8 C8 
    64 3A 24 66 AF C9 9D 8E 19 B6 41 AA 39 F6 7D 05 
    0B CB F7 F4 1F E5 B3 C4 FF C0 E1 CC 96 C6 80 E3 
    B2 F2 35 B6 4D B7 61 D2 AC 93 03 E1 06 CF 2D 9E 
    2F 40 E0 B2 C6 0B BC 32 F5 DA AB F7 64 9B 48 FD 
    83 A8 5C CC 81 43 2D 7D 1F 7D A2 A0 3E FE A2 9D 
    8A E5 DE F9 5C A9 7D 2E 62 FF 77 21 FE 05 04 B4 
    7D 66 33 59 E3 DD 7B 1F 94 F7 32 B7 19 CE 27 72 
    64 78 4F 0E BE C8 73 03 23 D6 DB E5 DE A0 B9 43 
    0E 22 51 E5 02 15 74 B3 64 47 FB B0 58 20 D7 10 
    50 20 BB 31 CF BC 32 61 F1 21 0F FF 4C AD 79 3E 
    FD 3B 65 A4 DA E6 28 25 24 39 C5 1F 5E 21 55 93 
    57 66 77 34 0F 6E A2 D5 B7 7B C2 68 39 B5 E0 39 
    C9 58 B0 F4 79 B3 13 68 ED 43 81 12 74 F3 88 DD 
    70 5B BF 66 04 21 88 0C C4 E2 25 A7 38 E1 0A 80 
    B8 E6 67 45 63 E6 52 89 D6 B1 CE B7 7B C4 9F DE 
    30 A4 88 D2 F0 72 80 5A E7 2F 42 99 E8 31 62 8B 
    48 40 D2 18 08 7F B2 EA D4 15 61 75 B7 C5 5B B5 
    F2 A1 F7 8A 7D 72 67 4D FE 5E D8 40 D7 EB C3 DC 
    32 B6 54 AC F8 7D 20 3F 1A D3 B4 7B 2C 9E 7D 9E 
    9B 6E AD AB A9 AF C1 36 

    TPM_Send: EvictKey
    TPM_TransmitSocket: To TPM [EvictKey] length=14
    00 C1 00 00 00 0E 00 00 00 22 A8 78 3A FD 
    TPM_ReceiveSocket: From TPM length=10
    00 C4 00 00 00 0A 00 00 00 00 

    TPM_Send: Quote
    TPM_TransmitSocket: To TPM [Quote] length=39
    00 C1 00 00 00 27 00 00 00 16 28 29 35 EF 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 03 FF FF FF 
    TPM_ReceiveSocket: From TPM length=759
    00 C4 00 00 02 F7 00 00 00 00 00 03 FF FF FF 00 
    00 01 E0 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DB 
    A8 C7 38 76 62 7A 1E 44 39 62 7B 64 C9 6C 8F 9C 
    8D 40 4A 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF FF 
    FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
    FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
    FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
    FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
    FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
    FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
    FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 01 00 62 0B 3D F5 1E 09 16 AB 00 
    3C C9 36 3B 7D 52 85 8E F3 87 CA D4 A9 72 14 CF 
    ED D5 6E 69 D1 C5 AC CB EF 2C 0B 56 0E 83 95 81 
    18 E3 A0 2E 67 A6 11 ED A5 EE 05 C8 1C A5 46 63 
    DE 18 28 02 11 DC 22 49 FF 36 A8 17 0C 43 60 C9 
    07 32 73 CF 19 7E 42 A8 74 94 18 67 A8 9D 59 A4 
    6E 52 0D 39 8C CE 11 26 3F D7 F1 6A 88 7B B5 3E 
    BA 63 D3 5F D2 8F 9B 53 21 5C 3D C3 BE 8B A9 5E 
    C9 E0 38 E1 31 86 7F 90 7A 9D 11 F1 A7 72 7E 79 
    BF 6D 10 5A DA FE 52 4D 34 36 D5 EA 2E 76 BF 36 
    D4 EC 3D 13 46 B8 40 E1 CA 56 B1 17 00 FA 43 5B 
    AF 84 00 73 F7 40 7B 28 71 40 ED 6F 54 FA BF 91 
    76 D8 20 52 9E 43 2F 43 2E C9 59 4F D4 DE C3 BE 
    F7 FB 04 BC A1 15 96 F5 2C 69 EE 39 8F BC 76 2D 
    66 21 C5 80 47 39 9E CB 1A E0 6C 5D CB E3 3B E8 
    0C 69 7B A3 5F C7 64 4A 9F 31 32 D2 58 27 95 A2 
    E1 43 48 51 FD BD 91 

    TPM_Send: GetCapability
    TPM_TransmitSocket: To TPM [GetCapability] length=22
    00 C1 00 00 00 16 00 00 00 65 00 00 00 05 00 00 
    00 04 00 00 01 10 
    TPM_ReceiveSocket: From TPM length=18
    00 C4 00 00 00 12 00 00 00 00 00 00 00 04 00 00 
    00 03 

    TPM_Send: GetCapability
    TPM_TransmitSocket: To TPM [GetCapability] length=22
    00 C1 00 00 00 16 00 00 00 65 00 00 00 07 00 00 
    00 04 00 00 00 01 
    TPM_ReceiveSocket: From TPM length=24
    00 C4 00 00 00 18 00 00 00 00 00 00 00 0A 00 02 
    28 29 35 EF A7 89 21 44 

    TPM_Send: GetPubKey - NO AUTH
    TPM_TransmitSocket: To TPM [GetPubKey - NO AUTH] length=14
    00 C1 00 00 00 0E 00 00 00 21 28 29 35 EF 
    TPM_ReceiveSocket: From TPM length=294
    00 C4 00 00 01 26 00 00 00 00 00 00 00 01 00 01 
    00 02 00 00 00 0C 00 00 08 00 00 00 00 02 00 00 
    00 00 00 00 01 00 C5 6C 68 4E 69 29 B0 7D 70 E7 
    DC 17 D8 D0 B2 68 DC B1 05 CF 90 ED A2 CA C2 E3 
    4F DA 40 50 13 78 75 3E E0 6A 41 D8 EA A7 F1 5D 
    7C 93 C5 88 61 4A 55 C8 96 8F A8 1F 46 AF 95 F4 
    D7 E8 DF 2E 5B 31 66 0A C6 E2 3E 40 89 72 BA FF 
    E4 8B 1D 82 27 C1 33 E3 EF FB E9 C4 33 C7 58 9B 
    68 D2 E0 76 EC 95 2E BA F4 F2 B8 5B BF F8 08 DB 
    F0 3D 62 52 A9 6F 6A 05 7B BA 7F 50 03 FD 28 A5 
    1C BC 1F 5C 2B C2 95 B2 5B 49 CA 36 0B 3A A9 3B 
    65 91 68 97 38 B9 DB F2 B1 A1 D3 BA D6 3F CC B5 
    BD AF 9D EB F7 C4 90 36 90 FC 34 66 2D 88 32 3A 
    B3 30 18 01 BB 43 17 4A A4 B7 05 3A 37 56 A8 B3 
    A3 C7 E2 2D 8B C8 CF 58 A8 7E A7 14 89 10 B9 46 
    11 6B DA 57 54 8F 06 72 E4 F2 74 15 25 5E 8C 6E 
    31 4D 11 90 61 36 AA 0E 66 DA F6 C9 9B AD 5C 86 
    D5 4F B3 3C 4C 70 6A 0A AA AA 9D 72 30 38 56 65 
    18 2E 2D 33 D8 27 

    TPM_Send: GetCapability
    TPM_TransmitSocket: To TPM [GetCapability] length=18
    00 C1 00 00 00 12 00 00 00 65 00 00 00 06 00 00 
    00 00 
    TPM_ReceiveSocket: From TPM length=18
    00 C4 00 00 00 12 00 00 00 00 00 00 00 04 01 01 
    00 00 
    Verification against AIK succeeded
```

### 3.8.2

```
echo hello > decrypt_attest

$ sha -if decrypt_attest -ix 11
SHA1 hash for file 'decrypt_attest': 
Hash: f572d396fae9206628714fb2ce00f72e94f2258f
New value of PCR: 72204b110c9d58b1519843f32c721f62bae5369b

createkey -kt e -ix 11 72204b110c9d58b1519843f32c721f62bae5369b -pwdk attest -pwdp aaa -ok attest -hp $A_HANDLE

loadkey -hp $A_HANDLE -ik attest.key -pwdp aaa
ATTEST_HANDLE=#out

sealfile -hk $ATTEST_HANDLE -if decrypt_attest -of decrypted_attest -pwdk attest

unsealfile -hk $ATTEST_HANDLE -if decrypted_attest -of decryptedest_attest -pwdk attest

echo goodbye > decrypt_attest

$ sha -if decrypt_attest -ix 11SHA1 hash for file 'decrypt_attest': 
Hash: e7d9b82b45d5833c9dada13f2379e7b66c823434
New value of PCR: bd64b3bbf86da6dc9baef760dffd64d636bf1c3f

$ unsealfile -hk $ATTEST_HANDLE -if decrypted_attest -of decryptedest_attest -pwdk attest
Error PCR mismatch from TPM_Unseal

forceclear
```
