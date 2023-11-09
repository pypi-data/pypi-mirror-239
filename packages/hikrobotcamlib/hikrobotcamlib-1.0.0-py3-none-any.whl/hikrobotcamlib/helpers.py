"""helpers"""
from typing import Tuple, Iterable


def get_octets(src: int) -> Tuple[int, int, int, int]:
    """Get the octets from an integer, useful for ips etc. returned highest first"""
    nip1 = (src & 0xFF000000) >> 24
    nip2 = (src & 0x00FF0000) >> 16
    nip3 = (src & 0x0000FF00) >> 8
    nip4 = src & 0x000000FF
    return nip1, nip2, nip3, nip4


def get_str(cstr: Iterable[int]) -> str:
    """Convert C string from the camera structs into str"""
    ret = ""
    for val in cstr:
        if val == 0x0:
            break
        ret += chr(val)
    return ret
