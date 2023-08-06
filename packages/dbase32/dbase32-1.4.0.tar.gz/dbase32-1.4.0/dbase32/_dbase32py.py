# dbase32: base32-encoding with a sorted-order alphabet (for databases)
# Copyright (C) 2013 Novacut Inc
#
# This file is part of `dbase32`.
#
# `dbase32` is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# `dbase32` is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with `dbase32`.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Jason Gerard DeRose <jderose@novacut.com>
#

"""
Pure-Python implementation of the Dbase32 encoding.
"""

from os import urandom
import time


DB32ALPHABET = '3456789ABCDEFGHIJKLMNOPQRSTUVWXY'
MAX_BIN_LEN = 60  # 480 bits
MAX_TXT_LEN = 96

DB32_START = 51
DB32_END = 89
DB32_FORWARD = DB32ALPHABET
DB32_REVERSE = (
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,
      0,  # '3' [51]
      1,  # '4' [52]
      2,  # '5' [53]
      3,  # '6' [54]
      4,  # '7' [55]
      5,  # '8' [56]
      6,  # '9' [57]
    255,  # ':' [58]
    255,  # ';' [59]
    255,  # '<' [60]
    255,  # '=' [61]
    255,  # '>' [62]
    255,  # '?' [63]
    255,  # '@' [64]
      7,  # 'A' [65]
      8,  # 'B' [66]
      9,  # 'C' [67]
     10,  # 'D' [68]
     11,  # 'E' [69]
     12,  # 'F' [70]
     13,  # 'G' [71]
     14,  # 'H' [72]
     15,  # 'I' [73]
     16,  # 'J' [74]
     17,  # 'K' [75]
     18,  # 'L' [76]
     19,  # 'M' [77]
     20,  # 'N' [78]
     21,  # 'O' [79]
     22,  # 'P' [80]
     23,  # 'Q' [81]
     24,  # 'R' [82]
     25,  # 'S' [83]
     26,  # 'T' [84]
     27,  # 'U' [85]
     28,  # 'V' [86]
     29,  # 'W' [87]
     30,  # 'X' [88]
     31,  # 'Y' [89]
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
    255,255,255,255,255,255,255,255,255,255,255,255,255,255,
)

DB32_SET = frozenset(DB32_FORWARD.encode('utf-8'))


def _text_to_bytes(text):
    """
    Common type checking and conversion for `isdb32()` and `check_db32()`.
    """
    if isinstance(text, str):
        return text.encode('utf-8')
    if not isinstance(text, bytes):
        if isinstance(text, bytearray):
            raise TypeError('must be read-only pinned buffer, not bytearray')
        name = type(text).__name__
        raise TypeError(
            '{!r} does not support the buffer interface'.format(name)
        )
    return text


def _check_length(text):
    """
    Common text length check for `db32dec()` and `check_db32()`.
    """
    assert isinstance(text, bytes)
    if not (8 <= len(text) <= MAX_TXT_LEN):
        raise ValueError(
            'len(text) is {}, need 8 <= len(text) <= {}'.format(
                len(text), MAX_TXT_LEN
            )
        )
    if len(text) % 8 != 0:
        raise ValueError(
            'len(text) is {}, need len(text) % 8 == 0'.format(len(text))
        )
    return text


def _encode_x_iter(data, x_forward):
    assert isinstance(data, bytes)
    taxi = 0
    bits = 0
    for d in data:
        taxi = (taxi << 8) | d
        bits += 8
        while bits >= 5:
            bits -= 5
            yield x_forward[(taxi >> bits) & 31]
    assert bits == 0


def encode_x(data, x_forward):
    if not isinstance(data, bytes):
        raise TypeError("'str' does not support the buffer interface")
    if not (5 <= len(data) <= MAX_BIN_LEN):
        raise ValueError(
            'len(data) is {}, need 5 <= len(data) <= {}'.format(
                len(data), MAX_BIN_LEN
            )
        )
    if len(data) % 5 != 0:
        raise ValueError(
            'len(data) is {}, need len(data) % 5 == 0'.format(len(data))
        )
    return ''.join(_encode_x_iter(data, x_forward))


def _decode_x_iter(text, x_reverse):
    utf8 = _check_length(_text_to_bytes(text))
    taxi = 0
    bits = 0
    for i in utf8:
        r = x_reverse[i]
        if r > 31:
            raise ValueError('invalid Dbase32: {!r}'.format(text))
        taxi = (taxi << 5) | r
        bits += 5
        while bits >= 8:
            bits -= 8
            yield (taxi >> bits) & 255
    assert bits == 0


def decode_x(text, x_reverse):
    return bytes(_decode_x_iter(text, x_reverse))


def db32enc(data):
    """
    Encode *data* into a Dbase32 string.

    For exmple:

    >>> db32enc(b'binary foo')
    'FCNPVRELI7J9FUUI'

    """
    return encode_x(data, DB32_FORWARD)


def db32dec(text):
    """
    Decode Dbase32 encoded *text*.

    For exmple:

    >>> db32dec('FCNPVRELI7J9FUUI')
    b'binary foo'

    """
    return decode_x(text, DB32_REVERSE)


def isdb32(text):
    text = _text_to_bytes(text)
    if not (8 <= len(text) <= MAX_TXT_LEN):
        return False
    if len(text) % 8 != 0:
        return False
    return DB32_SET.issuperset(text)


def check_db32(text):
    utf8 = _check_length(_text_to_bytes(text))
    if not DB32_SET.issuperset(utf8):
        raise ValueError('invalid Dbase32: {!r}'.format(text))


def random_id(numbytes=15):
    """
    Returns a 120-bit DBase32-encoded random ID.

    The ID will be 24-characters long, URL and filesystem safe.
    """
    if not isinstance(numbytes, int):
        if isinstance(numbytes, float):
            raise TypeError('integer argument expected, got float')
        if isinstance(numbytes, str):
            raise TypeError("'str' object cannot be interpreted as an integer")
        raise TypeError(
            'numbytes must be an int; got {!r}'.format(type(numbytes))
        )
    if not (5 <= numbytes <= MAX_BIN_LEN):
        raise ValueError('numbytes is {}, need 5 <= numbytes <= {}'.format(
                numbytes, MAX_BIN_LEN)
        )
    if numbytes % 5 != 0:
        raise ValueError(
            'numbytes is {}, need numbytes % 5 == 0'.format(numbytes)
        )
    return db32enc(urandom(numbytes))


def time_id(timestamp=-1):
    assert isinstance(timestamp, (int, float))
    ts = int(timestamp if timestamp >= 0 else time.time())
    buf = bytearray()

    # First 4 bytes are from the timestamp:
    buf.append((ts >> 24) & 255)
    buf.append((ts >> 16) & 255)
    buf.append((ts >>  8) & 255)
    buf.append(ts & 255)

    # Next 11 bytes are from os.urandom():
    buf.extend(urandom(11))

    return db32enc(bytes(buf))

