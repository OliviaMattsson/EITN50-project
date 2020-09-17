from utils import *


def walk_dir(img, sector, depth=0):
    r = sector_reader(img, sector)

    indent = ''.join(['    ' for x in range(depth)])

    def p_indent(s=''): print(f'{indent}{s}')

    for i in range(512//32):
        file_start = i * 32

        filename = r(file_start, 8)
        if filename[0] == 0:
            continue  # Free or unused

        if i == 0:
            p_indent(f'# Sector                {sector}')

        print()

        if filename[0] == 0xE5:
            p_indent(f'### DELETED ENTRY')
            filename = filename[1:]
        p_indent(f'# Bytes                 {file_start}..{file_start + 32}')

        attr = r(file_start+11, 1)
        attr_str = f'{hex(attr)}, {parse_attributes(dec(attr))}'

        is_dir = dec(attr) & 0x10

        create_datetime = readable_datetime(r(file_start+14, 4))
        last_accessed = readable_date(r(file_start+18, 2))
        last_write = readable_datetime(r(file_start+22, 4))
        fat_index = dec(r(file_start+26, 2))

        if str(filename) == 'GROUP02 ':
            p_indent('# Invalid FAT chain, increment one')
            fat_index += 1

        file_sector = 33 + fat_index - 2

        if is_dir:
            p_indent(f'Directory name          {str(filename)}')
        else:
            p_indent(f'File name               {str(filename)}')
            p_indent(f'Extension               {str(r(file_start+8, 3))}')

        p_indent(f'Attributes              {attr_str}')
        p_indent(f'Creation date           {create_datetime}')
        p_indent(f'Last accessed           {last_accessed}')
        p_indent(f'Last write              {last_write}')
        p_indent(f"Cluster's chain in FAT  {fat_index}")
        p_indent(f'Absolute offset         {file_sector * 512}')
        p_indent(f'File size (bytes)       {dec(r(file_start+28, 4))}')

        if not is_dir:
            file_reader = sector_reader(img, file_sector)
            first = file_reader(0, 512)
            if dec(first) == 0:
                first = '0x00 * 512'
            p_indent(f'First cluster (512b)    {first}')
        elif is_dir and str(filename).strip() not in ['.', '..']:
            walk_dir(img, file_sector, depth + 1)


def main():
    with open('image.dat', 'rb') as img:
        for sector in range(19, 33):
            walk_dir(img, sector)


if __name__ == '__main__':
    main()
