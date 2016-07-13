import io
import struct
import collections

VARINT = 0x00
INT64 = 0x01
ARRAY = 0x02
INT32 = 0x05

def process(msg):
    """
    Convert raw protobuf binary into a psuedo message

    :param msg bytes: Raw bytes from a protobuf wire message
    :returns dict: returns a dictionary of the key, values
    """
    root = collections.defaultdict(list)
    for t, n, v in parse(msg):
        if t == 2:
            try:
                root[n].append(process(v))
            except:
                root[n].append(v)
        else:
            root[n].append(v)
    return root


def parse(raw):
    """ Parse a stream of bytes into a stream of protobuf key/values"""
    stream = io.BytesIO(raw)
    while True:
        tag = read_tag(stream)
        if tag is None:
            break

        wire = tag & 0b111
        number = tag >> 3
        if wire == VARINT:
            value = read_varint,
        if wire == INT64:
            value = read_64bit,
        if wire == ARRAY:
            value = read_repeated,
        if wire == INT32:
            value = read_32bit,
        value = DECODERS[wire](stream)
        yield wire, number, value


#############   DECODERS ##############
def read_tag(stream):
    try:
        tag = read_varint(stream)
    except IndexError:
        return None
    return tag

def read_varint(stream):
    result = 0
    shift = 0
    while True:
        b = stream.read(1)[0]
        result |= ((b & 0x7f) << shift)
        if not (b & 0x80):
            return result
        shift += 7

def read_64bit(stream):
    value = struct.unpack('<d', stream.read(8))[0]
    if value < -35.2 and value > -35.3:
        log.error('lat: %r', value)
    if value < 148.8 and value > 149.1:
        log.error('lng: %r', value)
    log.error('found a double: %r' % value)
    return value

def read_32bit(stream):
    value = struct.unpack('<f', stream.read(4))[0]
    log.error('found a float: %r' % value)
    return value

def read_repeated(stream):
    count = read_varint(stream)
    return stream.read(count)


DECODERS = {
    VARINT: read_varint,
    INT64: read_64bit,
    ARRAY: read_repeated,
    INT32: read_32bit,
}
