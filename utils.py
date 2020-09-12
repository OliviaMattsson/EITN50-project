def dec(x): return int.from_bytes(x, 'little')


def hex(x): return f'0x{ x.hex() }'


def str(x): return x.decode()


def sector_reader(byte_stream, sector):
    def reader(offset, len=None):
        byte_stream.seek(sector * 512 + offset)
        return byte_stream.read(len)

    return reader


def fat_reader(byte_stream, table=1):
    assert table == 1 or table == 2, 'Invalid table (must be 1 or 2)'

    def reader(offset):
        even = offset % 2 == 0

        offset = (3 * offset) // 2
        byte_stream.seek(table * 512 + 3 + offset)
        data = byte_stream.read(2)

        if even:
            #    1111 2222 3333 4444
            # -> 4444 1111 2222

            full = data[0]                 # 0000 1111 2222
            partial = (data[1] & 0xF) << 8 # 4444 0000 0000
        else:
            #    1111 2222 3333 4444
            # -> 3333 4444 1111

            partial = data[0] >> 4 # 0000 0000 1111
            full = data[1] << 4    # 3333 4444 0000

        return full | partial

    return reader
