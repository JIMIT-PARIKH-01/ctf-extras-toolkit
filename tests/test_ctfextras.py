"""Offline tests for the CTF Extras Toolkit."""

import struct

from ctfextras import stego, writeup


def _make_bmp(w=20, h=20):
    row = (w * 3 + 3) & ~3
    pixels = bytes(row * h)
    dib = struct.pack("<IiiHHIIiiII", 40, w, h, 1, 24, 0, len(pixels), 2835, 2835, 0, 0)
    return b"BM" + struct.pack("<IHHI", 14 + 40 + len(pixels), 0, 0, 54) + dib + pixels


def test_stego_roundtrip(tmp_path):
    src = tmp_path / "in.bmp"
    out = tmp_path / "out.bmp"
    src.write_bytes(_make_bmp())
    msg = "flag{lsb_stego_w0rks}"
    stego.hide(str(src), msg, str(out))
    assert stego.extract(str(out)) == msg


def test_stego_capacity(tmp_path):
    src = tmp_path / "in.bmp"
    src.write_bytes(_make_bmp())
    assert stego.capacity_bytes(str(src)) > 0


def test_stego_rejects_non_bmp(tmp_path):
    import pytest
    bad = tmp_path / "x.bmp"
    bad.write_bytes(b"not a bmp")
    with pytest.raises(ValueError):
        stego.extract(str(bad))


def test_writeup_generates_markdown():
    md = writeup.generate(name="Baby RSA", category="crypto", points="100",
                          flag="flag{r5a}", steps=["Recover p,q", "Compute d"])
    assert "# Baby RSA" in md and "## Flag" in md and "flag{r5a}" in md
    assert "1. Recover p,q" in md
