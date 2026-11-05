#!/usr/bin/env python3
"""Ports corrections.tsv onto LibreOffice's Serbian dictionaries. Run from the top folder of the
repository, with a checkout of LibreOffice's dictionaries repository:

    python3 tools/port_libreoffice.py ../dictionaries

LibreOffice's sr/sr.dic is another generation of the same rule-based dictionary as ours, so its
affix classes are numbered differently and some words are built differently (сип/1125 gives сип
and сипски). Each correction is therefore matched by the word forms it gives, not by its flags:
a form a correction touches ends up accepted exactly when sr_Cyrl_RS accepts it, and every other
form keeps LibreOffice's verdict. sr-Latn.dic is a line-by-line transliteration of sr.dic with
the same classes, so every change is made in both. The .aff files get our KEY fix and our MAP, TRY
and REP tables. tools/check_libreoffice.py checks the result.
"""
import bisect
import collections
import itertools
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_corrections import latin  # noqa: E402

ALPHABET = "абвгдђежзијклљмнњопрстћуфхцчџш"
ORDER = {c: i for i, c in enumerate(ALPHABET)}


def read(path):
    return open(path, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")


def write(path, lines):
    # LibreOffice's Serbian files have Windows line endings.
    open(path, "w", encoding="utf-8", newline="").write("\r\n".join(lines))


def entries(path):
    return [l for l in read(path)[1:] if l]


class Aff:
    """The affix classes of an .aff file, enough to list the forms of an entry. These files use
    FLAG num, cross products and no continuation classes."""

    def __init__(self, lines):
        self.kind, self.rules = {}, collections.defaultdict(list)
        left = {}
        for l in lines:
            f = l.split()
            if not f or f[0] not in ("SFX", "PFX"):
                continue
            if left.get(f[1]):
                # The condition may be left out, which means any word.
                f = f[:5] + ["."] * (5 - len(f))
                strip = "" if f[2] == "0" else f[2]
                add = "" if f[3] == "0" else f[3]
                cond = f[4]
                rx = None if cond == "." else re.compile(("^" + cond) if f[0] == "PFX" else (cond + "$"))
                self.rules[f[1]].append((strip, add, rx, tuple(f[2:5])))
                left[f[1]] -= 1
            else:
                assert f[2] == "Y", f"{l}: only cross products are handled"
                self.kind[f[1]] = (f[0], f[2])
                left[f[1]] = int(f[3])
        assert not any(left.values()), "an affix class has fewer rules than its header says"

    def content(self, flag):
        return (self.kind[flag], tuple(sorted(r[3] for r in self.rules[flag])))

    def forms(self, entry):
        stem, _, fl = entry.partition("/")
        flags = fl.split(",") if fl else []
        sfx, pfx = [stem], []
        for f in flags:
            for strip, add, rx, _ in self.rules[f]:
                if self.kind[f][0] == "PFX":
                    pfx.append((strip, add, rx))
                # As in Hunspell, a rule may not strip the whole stem.
                elif len(stem) > len(strip) and stem.endswith(strip) and (rx is None or rx.search(stem)):
                    sfx.append(stem[: len(stem) - len(strip)] + add)
        out = set(sfx)
        for strip, add, rx in pfx:
            for w in sfx:
                if len(w) > len(strip) and w.startswith(strip) and (rx is None or rx.search(w)):
                    out.add(add + w[len(strip):])
        return out


def key(stem):
    return [ORDER.get(c, 100 + ord(c)) for c in stem.casefold()], stem


def main():
    lo_dir = sys.argv[1] + "/sr"
    ours = Aff(read("sr_Cyrl_RS/sr_Cyrl_RS.aff"))
    lo_aff = read(lo_dir + "/sr.aff")
    lo = Aff(lo_aff)
    dic = entries(lo_dir + "/sr.dic")
    ours_dic = entries("sr_Cyrl_RS/sr_Cyrl_RS.dic")

    by_content = collections.defaultdict(list)
    for k in lo.kind:
        by_content[lo.content(k)].append(k)
    new_classes, next_flag = {}, max(map(int, lo.kind)) + 1

    def lo_flag(stem, f):
        # A class with the same rules; else one that gives this word the same forms, as the rules
        # may be written differently; else a copy of ours.
        nonlocal next_flag
        same = by_content.get(ours.content(f))
        if same:
            return min(same, key=int)
        want = ours.forms(stem + "/" + f)
        same = [k for k in lo.kind if lo.kind[k] == ours.kind[f] and lo.forms(stem + "/" + k) == want]
        if same:
            return min(same, key=int)
        if f not in new_classes:
            new_classes[f] = str(next_flag)
            next_flag += 1
        return new_classes[f]

    def translate(entry):
        stem, _, fl = entry.partition("/")
        return stem + ("/" + ",".join(lo_flag(stem, f) for f in fl.split(",")) if fl else "")

    corrections = []
    for row in open("corrections.tsv", encoding="utf-8"):
        if row.startswith("#") or not row.strip():
            continue
        action, entry = row.rstrip("\n").split("\t")[:2]
        corrections.append((action, entry, ours.forms(entry)))
    touched = set().union(*(w for _, _, w in corrections))
    accepted = set()
    for e in ours_dic:
        accepted |= ours.forms(e) & touched
    gone = touched - accepted
    report, notes = collections.Counter(), []

    # An entry that gives a form to be gone is taken out. What else it gave stays: through the
    # same stem with fewer classes, where that gives only those forms, then through the 1.0.1
    # entries for the rest, and as bare words where no entry gives just them.
    lo_all = set()
    for e in dic:
        lo_all |= lo.forms(e)
    removals, splits = set(), []
    for i, e in enumerate(dic):
        forms = lo.forms(e)
        if not forms & gone:
            continue
        removals.add(i)
        rest = forms - gone
        stem, _, fl = e.partition("/")
        flags = fl.split(",") if fl else []
        narrower = next(
            (c for n in range(len(flags), -1, -1) for sub in itertools.combinations(flags, n)
             for c in [stem + ("/" + ",".join(sub) if sub else "")] if lo.forms(c) <= rest),
            None,
        )
        splits.append((e, [narrower] if narrower else [], rest - (lo.forms(narrower) if narrower else set())))
    # Forms that LibreOffice's other entries still give need nothing in their place.
    left_all = set().union(*(left for _, _, left in splits)) if splits else set()
    still = set()
    for i, e in enumerate(dic):
        if i not in removals:
            still |= lo.forms(e) & left_all
    by_form = collections.defaultdict(list)
    for o in ours_dic:
        for f in ours.forms(o) & (left_all - still):
            by_form[f].append(o)
    replacements = []
    for e, new, left in splits:
        left = left - still
        for f in sorted(left):
            if f not in left:
                continue
            for o in by_form.get(f, []):
                if ours.forms(o) <= lo_all - gone and translate(o) not in new:
                    new.append(translate(o))
                    left -= ours.forms(o)
                    break
            if f in left:
                new.append(f)
                left.discard(f)
        replacements += new
        report["entries taken out"] += 1
        if new:
            report["of them split"] += 1
            notes.append(f"{e} -> {', '.join(new)}")

    keep = [e for i, e in enumerate(dic) if i not in removals]
    lowered = {f[:1].lower() + f[1:] for f in touched}
    present = set()
    for e in keep + replacements:
        present |= lo.forms(e) & (touched | lowered)
    added = list(dict.fromkeys(replacements))
    for action, entry, want in corrections:
        if action != "add":
            continue
        # Hunspell also takes a capitalised word whose lowercase form is in the dictionary.
        if all(f in present or (f[:1].isupper() and f[:1].lower() + f[1:] in present) for f in want):
            report["additions LibreOffice already accepts"] += 1
            continue
        t = translate(entry)
        if t not in added:
            added.append(t)
            present |= want
            report["entries added"] += 1

    extra = []
    for ofl, nfl in new_classes.items():
        t, cross = ours.kind[ofl]
        rules = [r[3] for r in ours.rules[ofl]]
        # A digraph inside a bracket condition wouldn't transliterate letter for letter.
        assert not any("[" in r[2] and re.search("[љњџЉЊЏ]", r[2]) for r in rules), ofl
        extra += ["", f"{t} {nfl} {cross} {len(rules)}"] + [f"{t} {nfl} {' '.join(r[:2] if r[2] == '.' else r)}" for r in rules]

    # Each addition goes beside its neighbours in Serbian alphabetical order.
    keys = [key(e.split("/")[0]) for e in keep]
    out = list(keep)
    for new in sorted(added, key=lambda e: key(e.split("/")[0]), reverse=True):
        i = bisect.bisect_right(keys, key(new.split("/")[0]))
        out.insert(i, new)
        keys.insert(i, key(new.split("/")[0]))

    def new_aff(lines, ours_path, extra):
        tables = [l for l in read(ours_path) if l.split()[:1] in (["KEY"], ["MAP"], ["TRY"], ["REP"])]
        key_line = [t for t in tables if t.startswith("KEY ")][0]
        out = []
        for l in lines:
            # The KEY fix stays where the line is; MAP, TRY and REP go after WORDCHARS.
            out.append(key_line if l.startswith("KEY ") else l)
            if l.startswith("WORDCHARS"):
                out += [t for t in tables if not t.startswith("KEY ")]
        assert any(l.startswith("WORDCHARS") for l in lines)
        while out and out[-1] == "":
            out.pop()
        return out + extra + [""]

    write(lo_dir + "/sr.aff", new_aff(lo_aff, "sr_Cyrl_RS/sr_Cyrl_RS.aff", extra))
    write(lo_dir + "/sr-Latn.aff", new_aff(read(lo_dir + "/sr-Latn.aff"), "sr_Latn_RS/sr_Latn_RS.aff", [latin(l) for l in extra]))
    write(lo_dir + "/sr.dic", [str(len(out))] + out + [""])
    write(lo_dir + "/sr-Latn.dic", [str(len(out))] + [latin(e) for e in out] + [""])
    print(f"{len(dic)} entries, now {len(out)}; new affix classes: {', '.join(new_classes.values()) or 'none'}")
    for k, v in report.items():
        print(f"  {k}: {v}")
    for n in notes:
        print("  " + n)


if __name__ == "__main__":
    main()
