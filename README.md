# EITN50-project

## Assignment 1
Opened the file in hexedit.it. 

Information from Root Sector: 
- Byte 11: Bytes per sector: 0200 (Little Endian), so 512 bytes per sector. 
- Sectors per cluser: 1 (Standard floppy disk if i'm not mistaken).
- 1 reserved sector.
- 2 FATs, it is FAT12 so it's correct. 
- 224 max root dir entries. 
- 2880 total sectors
- 9 sectors per FAT
- 18 sectors per track
- 2 heads
- 41 Boot signature
- 2436b11b (hex) Volume id
- Converted to ascii gave FAT12 as file type. 

Used Python to read the file in code as well to confirm. 

- Device name:
- Serial Number: 
- Filesystem type: 
- Media descriptor:
- Bytes per sector: Bytes per sector: 0200 (Little Endian), so 512 bytes per sector. 
- Number of reserved sectors: 1 reserved sector.
- Number of sectors per allocation: Sectors per cluser: 1 (Standard floppy disk if i'm not mistaken).
- Number of sectors per FAT: 9 sectors per FAT
- Number of sectors per track: 18 sectors per track
- Number of heads on the diskette: 2 heads
- Number of hidden sectors:
- Start of bootstrap routine:
- Number of FATs: 2 FATs, it is FAT12 so it's correct. 
- Boot signature: 41 Boot signature
- Size of the device: 2436b11b (hex) Volume id
- Offset to start of FATs:
- Root dir offset:  
- Offset to data area:


## Assignment 2: 
First bit, BPB_Media, is set wrong. Accodring to documentation it should be 0x0FF8 for FAT12, but it is 0x0FF0 ( 111111110000 instead of 11111111**1**000)