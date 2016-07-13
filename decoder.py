import io
import struct
import collections

VARINT = 0x00
INT64 = 0x01
ARRAY = 0x02
INT32 = 0x05

def process(msg, recurse=True):
    """
    Convert raw protobuf binary into a psuedo message

    :param msg bytes: Raw bytes from a protobuf wire message
    :returns dict: returns a dictionary of the key, values
    """
    root = collections.defaultdict(list)
    for t, n, v in parse(msg):
        if t == 2 and recurse:
            try:
                root[n].append(process(v))
            except:
                root[n].append(v)
        else:
            root[n].append(v)
    return dict(root)


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
    return struct.unpack('<d', stream.read(8))[0]

def read_32bit(stream):
    return struct.unpack('<f', stream.read(4))[0]

def read_repeated(stream):
    count = read_varint(stream)
    return stream.read(count)


DECODERS = {
    VARINT: read_varint,
    INT64: read_64bit,
    ARRAY: read_repeated,
    INT32: read_32bit,
}
