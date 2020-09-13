from utils import *


def walk_dir(img, sector, depth=0):
    r = sector_reader(img, sector)

    indent = ''.join(['    ' for x in range(depth)])

    def p_indent(s=''): print(f'{indent}{s}')

    for i in range(512//32):
        file_start = i * 32

        filename = r(file_start, 8)
        if filename[0] == 0 or filename[0] == 0xE5:
            continue  # Free or unused

        attr = dec(r(file_start+11, 1))
        is_dir = attr & 0x10

        create_datetime = readable_datetime(r(file_start+14, 4))
        last_accessed = readable_date(r(file_start+18, 2))
        last_write = readable_datetime(r(file_start+22, 4))
        fat_index = dec(r(file_start+26, 2))
        absolute_offset = 33 + fat_index - 2

        if i != 0 or depth != 0:
            print()

        if is_dir:
            p_indent(f'Directory name          {str(filename)}')
        else:
            p_indent(f'File name               {str(filename)}')
            p_indent(f'Extension               {str(r(file_start+8, 3))}')

        p_indent(f'Attributes              {parse_attributes(attr)}')
        p_indent(f'Creation date           {create_datetime}')
        p_indent(f'Last accessed           {last_accessed}')
        p_indent(f'Last write              {last_write}')
        p_indent(f"Cluster's chain in FAT  {fat_index}")
        p_indent(f'Absolute offset         {absolute_offset}')
        p_indent(f'File size (bytes)       {dec(r(file_start+28, 4))}')

        if is_dir and str(filename).strip() not in ['.', '..']:
            walk_dir(img, absolute_offset, depth + 1)


def main():
    with open('image.dat', 'rb') as img:
        for sector in range(19, 32):
            walk_dir(img, sector)


if __name__ == '__main__':
    main()
