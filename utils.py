def dec(x): return int.from_bytes(x, 'little')


def hex(x): return f'0x{ x.hex() }'


def str(x): return x.decode()


def sector_reader(byte_stream, sector):
    def reader(offset, len=None):
        byte_stream.seek(sector * 512 + offset)
        return byte_stream.read(len)

    return reader
