# CTF Extras Toolkit

Two CTF helpers — **dependency-free**, GUI + CLI.

1. **LSB steganography** — hide/extract a text message in the least-significant bits of a
   **24-bit BMP** image (round-trip verified). Classic stego-challenge tooling.
2. **Writeup generator** — turn challenge details into a clean, consistent Markdown writeup.

Standard library only (`struct`, `datetime`). Python 3.8+.
(BMP keeps stego dependency-free; PNG/JPEG would need Pillow.)

## Run
```powershell
python ctfextras/gui.py           # GUI (tabs: Steganography / Writeup), or run.bat

python -m ctfextras stego hide  in.bmp "flag{hidden}" --out out.bmp
python -m ctfextras stego extract out.bmp
python -m ctfextras writeup --name "Baby RSA" --category crypto --points 100 ^
    --flag "flag{...}" --step "Recover p,q" --step "Compute d" --tool RsaCtfTool
```

## Layout
```
ctf-extras-toolkit/
└── ctfextras/
    ├── stego.py     # 24-bit BMP LSB hide/extract
    ├── writeup.py   # Markdown writeup generator
    ├── cli.py  gui.py  run.bat
```

MIT — see [LICENSE](./LICENSE).
