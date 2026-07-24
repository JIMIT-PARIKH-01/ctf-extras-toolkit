"""
CTF writeup generator (standard library only).

Turns challenge details into a clean, consistent Markdown writeup you can drop
straight into a repo or blog.
"""

from __future__ import annotations

from datetime import date


def generate(name: str, category: str = "", points: str = "", difficulty: str = "",
             description: str = "", steps=None, tools=None, flag: str = "",
             author: str = "Jimit Parikh") -> str:
    steps = steps or []
    tools = tools or []
    lines = [f"# {name}", ""]

    meta = []
    if category:
        meta.append(f"**Category:** {category}")
    if points:
        meta.append(f"**Points:** {points}")
    if difficulty:
        meta.append(f"**Difficulty:** {difficulty}")
    if meta:
        lines.append("  |  ".join(meta))
        lines.append("")

    if description:
        lines += ["## Challenge", description, ""]
    if tools:
        lines += ["## Tools used", *[f"- {t}" for t in tools], ""]
    if steps:
        lines += ["## Solution", ""]
        for i, step in enumerate(steps, 1):
            lines.append(f"{i}. {step}")
        lines.append("")
    if flag:
        lines += ["## Flag", "```", flag, "```", ""]

    lines += ["---", f"_Writeup by {author} — {date.today().isoformat()}_"]
    return "\n".join(lines)


def save(path: str, **kwargs) -> int:
    text = generate(**kwargs)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return len(text)
