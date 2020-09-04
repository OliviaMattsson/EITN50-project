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