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

- Device name: MSDOS5.0
- Serial Number: 
- Filesystem type: 
- Media descriptor: 1.4 Mb floppy, f0
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

b'03a'

Is printed twice, instead of b'6e'.

First bit, BPB_Media, is set wrong. Accodring to documentation it should be 0x0FF8 for FAT12, but it is 0x0FF0 ( 111111110000 instead of 11111111**1**000)
In the first byte of the first entry a copy of the media descriptor is stored. The remaining bits of this entry are 1. In the second entry the end-of-file marker is stored

"A FAT file has four attribute bits that can be turned on or off by the user - archive file, system file, hidden file, and read-only file."

"Beginning with Windows NT 3.5, files created or renamed on FAT volumes use the attribute bits to support long filenames in a way that does not interfere with how MS-DOS or OS/2 accesses the volume. Whenever a user creates a file with a long filename, Windows creates an eight-plus-three name for the file.

In addition to this conventional entry, Windows creates one or more secondary folder entries for the file, one for each 13 characters in the long filename. Each of these secondary folder entries stores a corresponding part of the long filename in Unicode. Windows sets the volume, read-only, system, and hidden file attribute bits of the secondary folder entry to mark it as part of a long filename.

MS-DOS and OS/2 generally ignore folder entries with all four of these attribute bits set, so these entries are effectively invisible to these operating systems. Instead, MS-DOS and OS/2 access the file by using the conventional eight-plus-three filename contained in the folder entry for the file."

## Directories

### FORENSIC
Attributes: 8 (00001000) Vol label
First cluster: 0 = Empty
Filesize: 0

### OUTPUT
Attributes: 20 (00100000) Archive
First cluster: 0200
Filesize: b2f10100

### AGrou (?)
Attributes: 0f, 15 (00001111) Vol label + system + hidden + readonly. Part of longer file
First cluster: 0 = Empty
Filesize: ffffffff

### GROUP01
Attributes: 10 (00010000) Subdir
First cluster: fb00
Filesize: 0 

### AGrou (?)
Attributes: 0f (00001111) Vol label + system + hidden + readonly. Part of longer file
First cluster: 0 = Empty
Filesize: ffffffff

### GROUP02
Attributes: 10 (00010000) Subdir
First cluster: fb00
Filesize: 0

### Used, deleted
Attributes: 0f (00001111) Vol label + system + hidden + read only, Part of longer file
First cluster: 0 = Empty
File size: ffffffff

### Used, deleted
Attributes: 10 (00010000) Subdir
First cluster: fd00
File size: 00020000

### Used, deleted (last space in root dir)
Attributes: 10 (00010000) Subdir
First cluster: 0301
File size: 00020000
