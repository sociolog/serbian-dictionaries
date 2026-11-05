#!/usr/bin/env python3
"""Builds the release archives in dist/. Run from the top folder of the repository.

    python3 tools/package.py 1.1

serbian-dictionaries-<version>.zip holds the two folders as they are. The -indesign archive holds
the same files under the names InDesign's Info.plist lists, sr_RS (Cyrillic) and sh_RS (Latin).
"""
import os
import sys
import zipfile

COMMON = ["README.md", "INSTALL.md", "CHANGELOG.md", "tools/install-onlyoffice.sh"] + [f"LICENSES/{f}" for f in sorted(os.listdir("LICENSES"))]
SETS = {"sr_Cyrl_RS": "sr_RS", "sr_Latn_RS": "sh_RS"}


def write(path, files):
    # A fixed date keeps the archives the same from one build to the next.
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, src in files:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, open(src, "rb").read())
    print(path)


def main():
    version = sys.argv[1]
    top = f"serbian-dictionaries-{version}"
    os.makedirs("dist", exist_ok=True)
    common = [(f"{top}/{f}", f) for f in COMMON]
    plain = [(f"{top}/{d}/{f}", f"{d}/{f}") for d in SETS for f in (f"{d}.aff", f"{d}.dic", f"hyph_{d}.dic")]
    write(f"dist/{top}.zip", plain + common)
    indesign = [
        (f"{top}-indesign/{old}/{f.replace(new, old)}", f"{new}/{f}")
        for new, old in SETS.items()
        for f in (f"{new}.aff", f"{new}.dic", f"hyph_{new}.dic")
    ]
    write(f"dist/{top}-indesign.zip", indesign + [(f"{top}-indesign/{f}", f) for f in COMMON])


if __name__ == "__main__":
    main()
