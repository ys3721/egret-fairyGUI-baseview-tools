import struct

user_name = "2"
password = "1"

def convert_bytes(target):
    bta = bytearray()
    bta.extend(map(ord, target))
    return bta

def login_msg_bytes():
    return struct.pack("!hhpppbippppppiip", 20, 1201, convert_bytes("2"), convert_bytes("1"),convert_bytes(""), False, 1, convert_bytes(""), convert_bytes(""),convert_bytes("12er31ee"),convert_bytes("1.11"),convert_bytes("2"), convert_bytes("extra"), 1101, 957, convert_bytes("extr2"))

def login_msg_bytes1():
    convert1 = convert_bytes("1")
    print("convert1 = %s" % convert1)

    packed = struct.pack("!hh", 10, 1201);
    convert1.insert(0, packed)

lb = login_msg_bytes1()
