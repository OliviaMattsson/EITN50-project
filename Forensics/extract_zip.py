from utils import *


def main():
    with open('image.dat', 'rb') as img:
        # Info from assignment 3
        ABSOLUTE_OFFSET = 148992
        LEN = 2029

        img.seek(ABSOLUTE_OFFSET)
        data = img.read(LEN)

        with open('data_extracted.zip', 'wb') as f:
            f.write(data)


if __name__ == '__main__':
    main()
