# EITN50-project

## Assignment 1
Opened the file in hexedit.it. 

Information from Root Sector: 

Used Python to read the file in code as well to confirm. 

- Device name: NO NAME
- Serial Number: 2436b11b (hex) Volume id
- Filesystem type: Converted to ascii gave FAT12 as file type. 
- Media descriptor: f0 (Generally set to this value for hard disks)
- Bytes per sector: Bytes per sector: 0200 (Little Endian), so 512 bytes per sector. 
- Number of reserved sectors: 1 reserved sector.
- Number of sectors per allocation: Sectors per cluser: 1 (Standard floppy disk if i'm not mistaken).
- Number of sectors per FAT: 9 sectors per FAT
- Number of sectors per track: 18 sectors per track
- Number of heads on the diskette: 2 heads
- Number of hidden sectors: 0 
- Start of bootstrap routine: 0 
- Number of FATs: 2 FATs, it is FAT12 so it's correct. 
- Boot signature: 41 Boot signature
- Size of the device: 179200 bytes
- Offset to start of FATs: 512 (Sector size)
- Root dir offset: 9728 bytes (512*19)
- Offset to data area: 16896 bytes
