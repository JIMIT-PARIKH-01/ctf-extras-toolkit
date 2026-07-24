"""
LSB image steganography (standard library only).

Hides / extracts a text message in the least-significant bits of a 24-bit
uncompressed BMP image. Great for CTF stego challenges. (PNG/JPEG would need
Pillow; BMP keeps this dependency-free and easy to inspect.)
"""

from __future__ import annotations

import struct


def _load_bmp(path: str):
    with open(path, "rb") as fh:
        data = bytearray(fh.read())
    if data[:2] != b"BM":
        raise ValueError("not a BMP file (expected 'BM' magic)")
    pixel_offset = struct.unpack("<I", data[10:14])[0]
    bpp = struct.unpack("<H", data[28:30])[0]
    if bpp != 24:
        raise ValueError(f"only 24-bit BMP supported (this is {bpp}-bit)")
    return data, pixel_offset


def _bytes_to_bits(bs: bytes) -> str:
    return "".join(f"{b:08b}" for b in bs)


def _bits_to_bytes(bits: str) -> bytes:
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) - 7, 8))


def capacity_bytes(path: str) -> int:
    data, offset = _load_bmp(path)
    return (len(data) - offset) // 8 - 4       # minus the 4-byte length header


def hide(in_path: str, message: str, out_path: str) -> int:
    data, offset = _load_bmp(in_path)
    payload = message.encode("utf-8")
    blob = struct.pack("<I", len(payload)) + payload     # 4-byte length prefix
    bits = _bytes_to_bits(blob)
    slots = len(data) - offset
    if len(bits) > slots:
        raise ValueError(f"message too big: needs {len(bits)} bits, image has {slots}")
    for i, bit in enumerate(bits):
        data[offset + i] = (data[offset + i] & 0xFE) | int(bit)
    with open(out_path, "wb") as fh:
        fh.write(data)
    return len(payload)


def extract(in_path: str) -> str:
    data, offset = _load_bmp(in_path)

    def read_bits(start: int, count: int) -> str:
        return "".join(str(data[offset + start + i] & 1) for i in range(count))

    length = struct.unpack("<I", _bits_to_bytes(read_bits(0, 32)))[0]
    max_len = (len(data) - offset - 32) // 8
    if length > max_len:
        raise ValueError("no valid hidden message found (bad length header)")
    payload = _bits_to_bytes(read_bits(32, length * 8))
    return payload.decode("utf-8", "replace")
