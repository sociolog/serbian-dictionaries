#!/usr/bin/env python3
"""Builds both spelling dictionaries from source/libreoffice/, corrections.tsv, aff-fixes.tsv and
tables/.

source/libreoffice/ holds LibreOffice's Serbian files as they are. corrections.tsv lists entries
to remove from sr.dic and entries to add, with LibreOffice's affix classes. aff-fixes.tsv lists
affix rule lines to correct in sr.aff, and tables/ holds the KEY, MAP, TRY and REP lines for the
.aff files. The Latin dictionary is the Cyrillic one, transliterated line by line, as LibreOffice's
sr-Latn.dic is, so a correction is made once. Run from the top folder of the repository.
"""
import bisect
import collections

LATIN = dict(zip("абвгдђежзијклмнопрстћуфхцчш", "abvgdđežzijklmnoprstćufhcčš"))
LATIN.update({"љ": "lj", "њ": "nj", "џ": "dž"})
ALPHABET = "абвгдђежзијклљмнњопрстћуфхцчџш"
ORDER = {c: i for i, c in enumerate(ALPHABET)}


def latin(line):
    out = ""
    for c in line:
        t = LATIN.get(c.lower())
        if t is None:
            out += c
        else:
            out += t if c == c.lower() else t[0].upper() + t[1:]
    return out


def lines(path):
    return open(path, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")


def key(entry):
    stem = entry.split("/")[0]
    return [ORDER.get(c, 100 + ord(c)) for c in stem.casefold()], stem


def aff_fixes(tr=lambda l: l):
    """The rule lines to correct, as {old: new}, in the script that tr gives. A fix that the
    transliteration makes moot, such as a Latin letter in a Cyrillic ending, is left out."""
    fixes = {}
    for row in open("aff-fixes.tsv", encoding="utf-8"):
        if row.startswith("#") or not row.strip():
            continue
        old, new = row.rstrip("\n").split("\t")[:2]
        if tr(old) != tr(new):
            fixes[tr(old)] = tr(new)
    return fixes


def aff(source, tables, fixes):
    # The KEY line is replaced where it is; MAP, TRY and REP go after WORDCHARS.
    table = [l for l in lines(tables) if l]
    key_line = [l for l in table if l.startswith("KEY ")]
    out, fixed = [], set()
    for l in lines(source):
        if l in fixes:
            fixed.add(l)
            l = fixes[l]
        out.append(key_line[0] if l.startswith("KEY ") and key_line else l)
        if l.startswith("WORDCHARS"):
            out += [t for t in table if not t.startswith("KEY ")]
    assert fixed == set(fixes), set(fixes) - fixed
    return "\n".join(out)


def main():
    entries = [l for l in lines("source/libreoffice/sr.dic")[1:] if l]
    assert [latin(e) for e in entries] == [l for l in lines("source/libreoffice/sr-Latn.dic")[1:] if l]
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
    # Each addition goes beside its neighbours in Serbian alphabetical order.
    keys = [key(e) for e in kept]
    words = list(kept)
    for e in sorted(add, key=key, reverse=True):
        i = bisect.bisect_right(keys, key(e))
        words.insert(i, e)
        keys.insert(i, key(e))
    for d, src, tr in (("sr_Cyrl_RS", "sr", lambda w: w), ("sr_Latn_RS", "sr-Latn", latin)):
        open(f"{d}/{d}.dic", "w", encoding="utf-8").write(f"{len(words)}\n" + "\n".join(map(tr, words)) + "\n")
        open(f"{d}/{d}.aff", "w", encoding="utf-8").write(aff(f"source/libreoffice/{src}.aff", f"tables/{d}.txt", aff_fixes(tr)))
    print(f"{len(entries)} entries, {len(entries) - len(kept)} removed, {len(add)} added, {len(words)} now")


if __name__ == "__main__":
    main()
