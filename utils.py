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

    sector = table
    if table == 2:
        sector = 10

    def reader(offset):
        even = offset % 2 == 0

        offset = (3 * offset) // 2
        byte_stream.seek(sector * 512 + offset)
        data = byte_stream.read(2)

        if even:
            #    1111 2222 3333 4444
            # -> 4444 1111 2222

            full = data[0]                  # 0000 1111 2222
            partial = (data[1] & 0xF) << 8  # 4444 0000 0000
        else:
            #    1111 2222 3333 4444
            # -> 3333 4444 1111

            partial = data[0] >> 4  # 0000 0000 1111
            full = data[1] << 4     # 3333 4444 0000

        return full | partial

    return reader


def readable_date(date):
    assert len(date) == 2, "date must be two bytes"

    date1 = date[0]
    date2 = date[1]

    years_since_1980 = date1 >> 1
    month_of_year = ((date1 & 0b00000001) << 3) | (date2 >> 5)
    day_of_month = date2 & 0b00011111

    return f'{1980 + years_since_1980}-{month_of_year:02}-{day_of_month:02}'


def readable_time(time):
    assert len(time) == 2, "time must be two bytes"
    time1 = time[0]
    time2 = time[1]

    hours = time1 >> 3
    minutes = ((time1 & 0b00000111) << 3) | (time2 >> 5)
    seconds = time2 & 0b00011111

    return f'{hours:02}:{minutes:02}:{seconds:02}'


def readable_datetime(datetime):
    time = datetime[0:2]
    date = datetime[2:4]

    return f'{readable_date(date)} {readable_time(time)}'


def parse_attributes(byte):
    def is_set(x): return 'yes' if byte & x else 'no'
    out = f'Read-only: {is_set(0x01)}, Hidden: {is_set(0x02)}, System: {is_set(0x04)}, '
    out += f'Volume label: {is_set(0x08)}, Subdirectory: {is_set(0x10)}, Archive: {is_set(0x20)}'
    return out
