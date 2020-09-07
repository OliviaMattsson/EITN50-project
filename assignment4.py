import sys
import os
import binascii
from functools import partial


def main():
    print("Native byteorder: ", sys.byteorder)
    with open('image.dat', 'rb') as img:
        print('Boot Sector: \n')
        img.seek(0,0)
        data = binascii.hexlify(img.read(61))
        print(data.decode('utf-8'), end='\n')
        
        print('.. Empty .. \n FAT-table: \n')
        img.seek(512,0)
        data = binascii.hexlify(img.read(500))
        print(data.decode('utf-8'), end='\n')
        
        print('.. Empty .. \n Root directory: \n')
        img.seek(9728,0)
        data = binascii.hexlify(img.read(800))
        print(data.decode('utf-8'), end='\n')
        
        img.seek(9728,0)
        for index in range(20):
            print('\n Next directory:')
            filename = binascii.hexlify(img.read(8))
            print('Filename: ' + printAscii(filename))
            
            ext = binascii.hexlify(img.read(3))
            print('Extension: ' + ext.decode('utf-8'))

            att = binascii.hexlify(img.read(1))
            print('Attributes: ' + att.decode('utf-8'))

            creation = binascii.hexlify(img.read(4))
            print('Created: ' + creation.decode('utf-8'))

            lastAcc = binascii.hexlify(img.read(4))
            print('Last Accessed: ' + lastAcc.decode('utf-8'))

            ig = binascii.hexlify(img.read(2))
            print('Last Accessed: ' + ig.decode('utf-8'))

            modified = binascii.hexlify(img.read(4))
            print('Modified: ' + modified.decode('utf-8'))

            nextCluster = binascii.hexlify(img.read(2))
            print('First Cluster: ' + nextCluster.decode('utf-8'))

            fileSize = binascii.hexlify(img.read(4))
            print('File Size: '+ fileSize.decode('utf-8'), end='\n')
    
def printAscii(input):
    first = input[:2]   
    try:
        if first == b'00':
            return 'Free'
        if first == b'e5':
            return 'Used, but now deleted'
        if first == b'2e':
            return 'Directory'
        return bytes.fromhex(input.decode('ascii')).decode('ascii')
    except UnicodeDecodeError:
        return ''
    else:
        pass

if __name__ == '__main__':
    main()
