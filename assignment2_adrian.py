from utils import *


def main():
    with open('image.dat', 'rb') as img:
        fat1 = fat_reader(img, 1)
        next = fat1(2)

        files = []

        for index in range(2, 400):
            index_already_processed = False

            for f in files:
                if index in f:
                    index_already_processed = True
                    break

            if index_already_processed:
                continue

            current = fat1(index)

            if current == 0:
                # Unused
                continue

            print(f'scanning file for index { index }', end='... ')
            f = set()

            while True:
                if current in range(0xFF8, 0xFFF+1):
                    print('reached end of file')
                    break

                f.add(current)
                next = fat1(current)

                if next in f:
                    fallback = current + 1
                    print(
                        f'{ current } -> { next } is recursive. try increment pointer to { fallback }',
                        end='... '
                    )

                    next = fallback
                    if next in f:
                        print('fallback also visited, skipping')
                        break

                current = next

            files.append(f)


if __name__ == '__main__':
    main()
