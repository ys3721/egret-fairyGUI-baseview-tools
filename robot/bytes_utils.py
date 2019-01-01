# -*- coding=utf-8 -*- #
import struct


def write_short(bytes_arrays, short_value):
    short_bytes = struct.pack("!h", short_value)
    bytes_arrays.extend(short_bytes)
    return bytes_arrays


def write_int(bytes_arrays, int_value):
    int_bytes = struct.pack("!i", int_value)
    bytes_arrays.extend(int_bytes)
    return bytes_arrays


def write_long(byte_arrays, long_value):
    long_bytes = struct.pack("!q", long_value)
    byte_arrays.extend(long_bytes)
    return byte_arrays


def write_utf(byte_arrays, str_value):
    str_bytes = bytes(str_value, "utf-8")
    write_short(byte_arrays, len(str_bytes))
    byte_arrays.extend(str_bytes)
    return byte_arrays



