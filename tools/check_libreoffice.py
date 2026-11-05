#!/usr/bin/env python3
"""Checks LibreOffice's Serbian dictionaries after tools/port_libreoffice.py. Run from the top
folder of the repository:

    python3 tools/check_libreoffice.py ../dictionaries [base]

It compares the files in sr/ with those at the base commit (HEAD by default), in both scripts:
a word's verdict may change only where a correction touches it, and there it must match
sr_Cyrl_RS and sr_Latn_RS. The forms of every entry are listed, and Hunspell is asked too when
libhunspell is installed: about the corrected words, as written, capitalised and in capitals, and
about 100,000 other forms chosen at random. It exits with 1 if anything differs.
"""
import ctypes
import ctypes.util
import os
import random
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_corrections import latin  # noqa: E402
from port_libreoffice import Aff, read  # noqa: E402

SCRIPTS = (("Cyrillic", "sr", "sr_Cyrl_RS/sr_Cyrl_RS", lambda e: e), ("Latin", "sr-Latn", "sr_Latn_RS/sr_Latn_RS", latin))


def accepted(f, forms):
    # Hunspell also takes a capitalised word whose lowercase form is in the dictionary.
    return f in forms or (f[:1].isupper() and f[:1].lower() + f[1:] in forms)


def all_forms(aff, dic):
    a, out = Aff(aff), set()
    for e in dic[1:]:
        if e:
            out |= a.forms(e)
    return out


def hunspell():
    name = ctypes.util.find_library("hunspell") or ctypes.util.find_library("hunspell-1.7")
    for n in [name, "libhunspell-1.7.so.0", "libhunspell-1.7.0.dylib"]:
        try:
            lib = ctypes.CDLL(n)
        except (OSError, TypeError):
            continue
        lib.Hunspell_create.restype = ctypes.c_void_p
        lib.Hunspell_create.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        lib.Hunspell_spell.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        return lib
    return None


def main():
    lo, base = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    lib, failed = hunspell(), False
    rows = [r.rstrip("\n").split("\t")[:2] for r in open("corrections.tsv", encoding="utf-8") if r.strip() and not r.startswith("#")]
    tmpdir = tempfile.TemporaryDirectory()
    tmp = tmpdir.name
    for name, lo_name, ours_base, tr in SCRIPTS:
        old = {}
        for ext in ("aff", "dic"):
            text = subprocess.run(["git", "-C", lo, "show", f"{base}:sr/{lo_name}.{ext}"], capture_output=True, check=True).stdout
            open(f"{tmp}/{lo_name}.{ext}", "wb").write(text)
            old[ext] = text.decode("utf-8").replace("\r\n", "\n").split("\n")
        new = {ext: read(f"{lo}/sr/{lo_name}.{ext}") for ext in ("aff", "dic")}
        ours_aff = Aff(read(ours_base + ".aff"))
        touched = set()
        for _, e in rows:
            touched |= ours_aff.forms(tr(e))
        words = touched | {f[:1].upper() + f[1:] for f in touched}
        O, P = all_forms(old["aff"], old["dic"]), all_forms(new["aff"], new["dic"])
        U = all_forms(read(ours_base + ".aff"), read(ours_base + ".dic"))
        changed = {f for f in (O ^ P) | {f[:1].upper() + f[1:] for f in O ^ P} if accepted(f, O) != accepted(f, P)}
        outside = changed - words
        disagree = {f for f in words if accepted(f, P) != accepted(f, U)}
        print(f"{name}: {len(O):,} forms, now {len(P):,}; {len(changed):,} verdicts changed, {len(outside)} outside the corrections")
        print(f"  {len(words):,} corrected words, {len(disagree)} unlike {ours_base}")
        failed |= bool(outside or disagree)
        if lib:
            h = {k: lib.Hunspell_create(f"{p}.aff".encode(), f"{p}.dic".encode())
                 for k, p in (("old", f"{tmp}/{lo_name}"), ("new", f"{lo}/sr/{lo_name}"), ("ours", ours_base))}
            spell = lambda k, w: bool(lib.Hunspell_spell(h[k], w.encode()))
            test = words | {w.upper() for w in words}
            unlike = [w for w in test if spell("new", w) != spell("ours", w)]
            random.seed(1)
            others = random.sample(sorted(O - words), min(100_000, len(O - words)))
            moved = [w for w in others if spell("new", w) != spell("old", w)]
            print(f"  Hunspell: {len(unlike)} of {len(test):,} corrected words unlike {ours_base}; "
                  f"{len(moved)} of {len(others):,} other forms changed")
            failed |= bool(unlike or moved)
            for w in sorted(unlike + moved)[:10]:
                print("    " + w)
        for w in sorted(outside | disagree)[:10]:
            print("    " + w)
    if not lib:
        print("libhunspell not found: only the listed forms were compared")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
