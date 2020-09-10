from utils import *

with open('image.dat', 'rb') as img:
    r = sector_reader(img, 0)

    print(f'Device name                               { str(r(43, 11)) }')
    print(f'Serial number                             { dec(r(39, 4)) }')
    print(f'Filesystem type                           { str(r(54, 8)) }')
    print(f'Media descriptor                          { hex(r(21, 1)) }')
    print(f'Bytes per sector                          { dec(r(11, 2)) }')
    print(f'Number of reserved sectors                { dec(r(14, 2)) }')

    # Sectors per cluster?
    print(f'Number of sectors per allocation          { dec(r(13, 1)) }')

    print(f'Number of sectors per FAT                 { dec(r(22, 2)) }')
    print(f'Number of sectors per track               { dec(r(24, 2)) }')
    print(f'Number of heads on the diskette           { dec(r(26, 2)) }')
    print(f'Number of hidden sectors                  { dec(r(28, 4)) }')
    print(f'Start of bootstrap routine                0x3e')
    print(f'Number of FATs                            { dec(r(16, 1)) }')
    print(f'Boot signature                            { hex(r(38, 1)) }')
    print(f'Size of the device(bytes)                 { len(r(0)) }')
    print(f'Offset to start of FAT(s)                 { 512 }')
    print(f'Root Directory Offset                     { 19*512 }')
    print(f'Offset to data area                       { 33*512 }')
