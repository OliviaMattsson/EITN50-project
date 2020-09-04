import sys;
import os;



def main():
img_file = open('image.dat', 'r')
    for line in img_file:
        print line,
        
img_file.close()
if __name__ == '__main__':
    main()
