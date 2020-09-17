import sys
import os
import binascii
from functools import partial


def main():
    with open('image.dat', 'rb') as img:
        with open('fatentries.txt', 'w') as f:
            print('\n FAT-table: \n', file=f)
            img.seek(512,0)
            data = binascii.hexlify(img.read(200))
            print(data.decode('utf-8'), end='\n', file=f)

            img.seek(512,0)
            
            for index in range(101):
                data = binascii.hexlify(img.read(3))
                firstbyte = data[3:4]
                firstbyte += data[:2]
                secondbyte = data[-2:]
                secondbyte += data[2:3]
                print('\n {}'.format(firstbyte), file=f)
                print('\n {}'.format(secondbyte), file=f)
if __name__ == '__main__':
    main()
