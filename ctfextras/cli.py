"""
CTF Extras command line.

    python -m ctfextras stego hide  in.bmp "flag{hidden}" --out out.bmp
    python -m ctfextras stego extract out.bmp
    python -m ctfextras writeup --name "Baby RSA" --category crypto --points 100 \
        --flag "flag{...}" --step "Recover p,q" --step "Compute d" --tool RsaCtfTool
"""

from __future__ import annotations

import argparse
import sys

from . import stego, writeup


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ctfextras",
                                description="CTF extras: LSB steganography + writeup generator.")
    sub = p.add_subparsers(dest="command", required=True)

    st = sub.add_parser("stego", help="Hide/extract text in a 24-bit BMP.")
    st_sub = st.add_subparsers(dest="op", required=True)
    h = st_sub.add_parser("hide")
    h.add_argument("image"); h.add_argument("message"); h.add_argument("--out", required=True)
    e = st_sub.add_parser("extract")
    e.add_argument("image")

    w = sub.add_parser("writeup", help="Generate a Markdown CTF writeup.")
    w.add_argument("--name", required=True)
    w.add_argument("--category", default="")
    w.add_argument("--points", default="")
    w.add_argument("--difficulty", default="")
    w.add_argument("--description", default="")
    w.add_argument("--flag", default="")
    w.add_argument("--step", action="append", default=[], help="Repeatable solution step.")
    w.add_argument("--tool", action="append", default=[], help="Repeatable tool used.")
    w.add_argument("--out", help="Write to a file instead of stdout.")
    return p


def main(argv: list | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "stego":
            if args.op == "hide":
                n = stego.hide(args.image, args.message, args.out)
                print(f"Hid {n} bytes -> {args.out}")
            else:
                print(stego.extract(args.image))
        elif args.command == "writeup":
            md = writeup.generate(
                name=args.name, category=args.category, points=args.points,
                difficulty=args.difficulty, description=args.description,
                steps=args.step, tools=args.tool, flag=args.flag)
            if args.out:
                with open(args.out, "w", encoding="utf-8") as fh:
                    fh.write(md)
                print(f"Wrote writeup -> {args.out}")
            else:
                print(md)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
