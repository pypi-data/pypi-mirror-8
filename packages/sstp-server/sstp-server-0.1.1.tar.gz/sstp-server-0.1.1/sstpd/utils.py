import struct


def hexdump():
    pass


def parseLength(s):
    s = chr(ord(s[0]) & 0x0f) + s[1]  # Ignore R
    return struct.unpack('!H', s)[0]

