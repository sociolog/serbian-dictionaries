#!/usr/bin/env python3
"""Builds both spelling dictionaries from source/2019/sr_RS/sr_RS.dic and corrections.tsv.

The Latin dictionary is the Cyrillic one, transliterated line by line, so a correction is made
once. Run from the top folder of the repository.
"""
import collections

LATIN = dict(zip("абвгдђежзијклмнопрстћуфхцчш", "abvgdđežzijklmnoprstćufhcčš"))
LATIN.update({"љ": "lj", "њ": "nj", "џ": "dž"})


def latin(line):
    out = ""
    for c in line:
        t = LATIN.get(c.lower())
        if t is None:
            out += c
        else:
            out += t if c == c.lower() else t[0].upper() + t[1:]
    return out


def main():
    lines = open("source/2019/sr_RS/sr_RS.dic", encoding="utf-8").read().split("\n")
    entries = [l for l in lines[1:] if l]
    remove, add = collections.Counter(), []
    for row in open("corrections.tsv", encoding="utf-8"):
        if row.startswith("#") or not row.strip():
            continue
        action, entry = row.rstrip("\n").split("\t")[:2]
        if action == "remove":
            remove[entry] += 1
        else:
            add.append(entry)
    kept = []
    for e in entries:
        if remove[e]:
            remove[e] -= 1
        else:
            kept.append(e)
    missing = [e for e, n in remove.items() if n]
    assert not missing, missing
    assert not set(add) & set(kept), set(add) & set(kept)
    cyrillic = kept + add
    for path, words in (("sr_Cyrl_RS/sr_Cyrl_RS.dic", cyrillic), ("sr_Latn_RS/sr_Latn_RS.dic", [latin(w) for w in cyrillic])):
        open(path, "w", encoding="utf-8").write(f"{len(words)}\n" + "\n".join(words) + "\n")
    print(f"{len(entries)} entries, {len(entries) - len(kept)} removed, {len(add)} added, {len(cyrillic)} now")


if __name__ == "__main__":
    main()
