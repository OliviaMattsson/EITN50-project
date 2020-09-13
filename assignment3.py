from utils import *


def main():
    with open('image.dat', 'rb') as img:
        for sector in range(19, 32):
            r = sector_reader(img, sector)

            for i in range(512//32):
                file_start = i*32

                filename = r(file_start, 8)
                if filename[0] == 0 or filename[0] == 0xE5:
                    # Free or unused
                    continue

                attr = dec(r(file_start+11, 1))

                is_dir = attr & 0x10

                create_datetime = readable_datetime(r(file_start+14, 4))
                last_accessed = readable_date(r(file_start+18, 2))
                last_write = readable_datetime(r(file_start+22, 4))
                fat_index = dec(r(file_start+26, 2))

                if i != 0:
                    print()

                if is_dir:
                    print(f'Directory name          {str(filename)}')
                else:
                    print(f'file name               {str(filename)}')
                    print(f'Extension               {str(r(file_start+8, 3))}')

                print(f'Attributes              {parse_attributes(attr)}')
                print(f'Creation date           {create_datetime}')
                print(f'Last accessed           {last_accessed}')
                print(f'Last write              {last_write}')
                print(f"Cluster's chain in FAT  {fat_index}")
                print(f'Absolute offset         {33 + fat_index - 2}')
                print(f'File size (bytes)       {dec(r(file_start+28, 4))}')


if __name__ == '__main__':
    main()
