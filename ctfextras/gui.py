"""
Tkinter GUI for the CTF Extras Toolkit (standard library only).
Tabs: Steganography · Writeup generator.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

try:
    from ctfextras import stego, writeup
except ImportError:  # pragma: no cover
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from ctfextras import stego, writeup


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CTF Extras Toolkit")
        self.geometry("800x640")
        self.minsize(680, 520)
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=8)
        nb.add(StegoTab(nb), text="  Steganography  ")
        nb.add(WriteupTab(nb), text="  Writeup  ")


class StegoTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.columnconfigure(1, weight=1); self.rowconfigure(4, weight=1)
        ttk.Label(self, text="BMP image").grid(row=0, column=0, sticky="w")
        self.img = tk.StringVar()
        ttk.Entry(self, textvariable=self.img).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(self, text="Browse…", command=self._browse).grid(row=0, column=2)
        ttk.Label(self, text="Message").grid(row=1, column=0, sticky="w")
        self.msg = tk.StringVar()
        ttk.Entry(self, textvariable=self.msg).grid(row=1, column=1, columnspan=2, sticky="ew", padx=6)
        bar = ttk.Frame(self); bar.grid(row=2, column=0, columnspan=3, sticky="ew", pady=6)
        ttk.Button(bar, text="Hide -> save as…", command=self.hide).pack(side="left")
        ttk.Button(bar, text="Extract", command=self.extract).pack(side="left", padx=6)
        self.out = scrolledtext.ScrolledText(self, height=10, wrap="word",
                                             font=("Consolas", 10), state="disabled")
        self.out.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(8, 0))

    def _browse(self):
        f = filedialog.askopenfilename(filetypes=[("BMP", "*.bmp"), ("All", "*.*")])
        if f:
            self.img.set(f)

    def _show(self, text):
        self.out.configure(state="normal"); self.out.delete("1.0", "end")
        self.out.insert("1.0", text); self.out.configure(state="disabled")

    def hide(self):
        if not self.img.get().strip():
            messagebox.showinfo("No image", "Choose a BMP."); return
        out = filedialog.asksaveasfilename(defaultextension=".bmp",
                                           filetypes=[("BMP", "*.bmp")])
        if not out:
            return
        try:
            n = stego.hide(self.img.get(), self.msg.get(), out)
            self._show(f"Hid {n} bytes into:\n{out}")
        except Exception as exc:  # noqa: BLE001
            self._show(f"Error: {exc}")

    def extract(self):
        if not self.img.get().strip():
            messagebox.showinfo("No image", "Choose a BMP."); return
        try:
            self._show("Hidden message:\n\n" + stego.extract(self.img.get()))
        except Exception as exc:  # noqa: BLE001
            self._show(f"Error: {exc}")


class WriteupTab(ttk.Frame):
    FIELDS = [("name", "Name"), ("category", "Category"), ("points", "Points"),
              ("difficulty", "Difficulty"), ("flag", "Flag")]

    def __init__(self, master):
        super().__init__(master, padding=10)
        self.columnconfigure(1, weight=1); self.rowconfigure(8, weight=1)
        self.vars = {}
        for r, (key, label) in enumerate(self.FIELDS):
            ttk.Label(self, text=label).grid(row=r, column=0, sticky="w")
            v = tk.StringVar(); self.vars[key] = v
            ttk.Entry(self, textvariable=v).grid(row=r, column=1, sticky="ew", padx=6, pady=2)
        ttk.Label(self, text="Steps (one per line)").grid(row=6, column=0, sticky="nw")
        self.steps = scrolledtext.ScrolledText(self, height=5, wrap="word", font=("Segoe UI", 10))
        self.steps.grid(row=6, column=1, sticky="ew", padx=6)
        ttk.Button(self, text="Generate Markdown", command=self.gen).grid(
            row=7, column=1, sticky="e", pady=6)
        self.out = scrolledtext.ScrolledText(self, height=10, wrap="word",
                                             font=("Consolas", 10), state="disabled")
        self.out.grid(row=8, column=0, columnspan=2, sticky="nsew", pady=(6, 0))

    def gen(self):
        steps = [s for s in self.steps.get("1.0", "end").splitlines() if s.strip()]
        md = writeup.generate(name=self.vars["name"].get() or "Untitled",
                              category=self.vars["category"].get(),
                              points=self.vars["points"].get(),
                              difficulty=self.vars["difficulty"].get(),
                              flag=self.vars["flag"].get(), steps=steps)
        self.out.configure(state="normal"); self.out.delete("1.0", "end")
        self.out.insert("1.0", md); self.out.configure(state="disabled")


def main() -> int:
    App().mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
