# Serbian spelling and hyphenation dictionaries

Hunspell spelling dictionaries and Hyphen hyphenation patterns for Serbian, in Cyrillic and Latin script.

| Folder | Script | Spelling | Hyphenation |
|---|---|---|---|
| `sr_Cyrl_RS/` | Cyrillic | `sr_Cyrl_RS.aff`, `sr_Cyrl_RS.dic` | `hyph_sr_Cyrl_RS.dic` |
| `sr_Latn_RS/` | Latin | `sr_Latn_RS.aff`, `sr_Latn_RS.dic` | `hyph_sr_Latn_RS.dic` |

All files are UTF-8. Version 1.0.1; [CHANGELOG.md](CHANGELOG.md) lists what changed, and [INSTALL.md](INSTALL.md) says how to install the files in ONLYOFFICE, InDesign and other programs.

## File names

The names say the script and follow the language tags `sr-Cyrl-RS` and `sr-Latn-RS`. ONLYOFFICE uses the same names for its Serbian dictionaries, and DesignCraft reads them as they are.

InDesign is the exception. Its archive keeps the old names, `sr_RS` (Cyrillic) and `sh_RS` (Latin), because those are the names its settings list. Other names in InDesign are untested.

## Bosnia and Herzegovina, and Montenegro

The same two sets serve all three regions, because the spelling dictionaries hold both ekavian and ijekavian forms.

Ekavian and ijekavian are a free choice, not a matter of region, and the Pravopis doesn't allow mixing them in one text (point 6). A combined dictionary can't catch that. Language tags can mark the choice with the registered variants `ekavsk` and `ijekavsk`, as in `sr-Latn-ijekavsk`. We keep one combined dictionary because it is simpler for every program that uses it. `PLAN-ekavian-ijekavian.md` records how strict lists could be built if they are ever wanted.

| Region | Cyrillic | Latin |
|---|---|---|
| Serbia | `sr-Cyrl-RS` | `sr-Latn-RS` |
| Bosnia and Herzegovina | `sr-Cyrl-BA` | `sr-Latn-BA` |
| Montenegro | `sr-Cyrl-ME` | `sr-Latn-ME` |

File and folder names use `_` in place of `-`. Older files may say `CS`, for the former Serbia and Montenegro.

DesignCraft reads all of these with no extra files. LibreOffice lists only `RS` and `CS` for these dictionaries, in `dictionaries.xcu`. ONLYOFFICE has only `sr_Cyrl_RS` and `sr_Latn_RS` in its language table.

## Building

The Latin spelling dictionary is built from the Cyrillic one, line by line, so a correction is made once, in Cyrillic, in `corrections.tsv`. `source/2019/` holds the July 2019 files this version starts from, as they were. To rebuild both dictionaries, run this in the top folder:

```sh
python3 tools/apply_corrections.py
```

The script doesn't touch the `.aff` files, which differ from the source only by the suggestion tables, or the hyphenation files. `python3 tools/package.py <version>` builds the release archives in `dist/`.

### Porting the corrections to LibreOffice

LibreOffice's `sr/sr.dic` is another generation of the same rule-based dictionary, so its affix classes are numbered differently and some words are built differently. `corrections.tsv` can't be copied into it entry by entry. Instead, `tools/port_libreoffice.py` matches each correction by the word forms it gives: a form a correction touches ends up accepted exactly when `sr_Cyrl_RS` accepts it, and every other form keeps LibreOffice's verdict. It edits both scripts, and adds our `KEY` fix and suggestion tables to the `.aff` files. Run it in the top folder, with a checkout of LibreOffice's [dictionaries](https://git.libreoffice.org/dictionaries) repository, then check the result:

```sh
python3 tools/port_libreoffice.py ../dictionaries
python3 tools/check_libreoffice.py ../dictionaries
```

The check compares `sr/` with the checkout's last commit. It lists the forms of every entry, and asks Hunspell as well when `libhunspell` is installed.

## Contributors

The sources below don't give a complete history, so this list may not be complete. It names everyone the sources name. Corrections are welcome.

**Spelling dictionaries**

- **Milutin Smiljanić:** developer of the rule-based Serbian dictionary that LibreOffice has shipped since 19 April 2019.
- **Goran Rakić:** maintainer of `dict-sr`, `hunspell-sr` and the LibreOffice extension, 2010–2013.
- **Miloš Popović** and **Aleksandar Urošević:** contributions to `dict-sr`.
- **Nikola Smolenski:** merged a personal dictionary into `hunspell-sr`, 2013.
- **Romeo Mlinar:** suggestions merged into `hunspell-sr`, 2013.
- **@krunose (Kruno-S):** `hunspell-sr` conversion table, 2016.
- **The Chromium project:** `sr.dic_delta`, merged into `hunspell-sr` in 2010.
- **The Serbian LibreOffice community:** named as maintainer of the extension.

The source files in `source/2019/` date from July 2019, and 97.1% of their stems are also in LibreOffice's current dictionary. The other 2.9% look like local edits, such as added names (Надал, Федерер) and adjective forms. We don't know who made those edits.

**Hyphenation patterns**

- **Dejan Muhamedagić:** author of the Serbian TeX patterns (1990, 2008), on which all of these files are based.
- **Goran Rakić:** adapted them for the Hyphen library.

The source files date from July 2019 and share about 95% of their patterns with Goran Rakić's. We don't know who made the other changes.

**This version**

- **Mile Vukajlović** (@sociolog)
- **@VladimirCeric:** co-author; testing, word lists and typographic review.

Prepared with Claude Code.

## Licences

These licences come from the sources, so they can't be replaced by another one. Our changes are offered under the same terms.

| Files | Licence | SPDX |
|---|---|---|
| `*.aff`, `*.dic` (spelling) | Your choice of GNU LGPL 3 or later, MPL 2 or later, or GNU GPL 3 or later | `LGPL-3.0-or-later OR MPL-2.0 OR GPL-3.0-or-later` |
| `hyph_*.dic`, `patterns/` (hyphenation) | GNU LGPL 2.1 or later | `LGPL-2.1-or-later` |
| `tools/`, `corrections.tsv` and the documentation | Same as the spelling dictionaries | `LGPL-3.0-or-later OR MPL-2.0 OR GPL-3.0-or-later` |

The spelling terms are those LibreOffice states for Milutin Smiljanić's dictionary. The earlier `hunspell-sr` was offered under LGPL 2.1 or later, MPL 1.1 or later, GPL 2 or later, or CC BY-SA 3.0, and those terms allow the versions above.

The hyphenation terms are those LibreOffice states for the Hyphen form of the patterns. The TeX originals are under the LaTeX Project Public License 1 or later, in [hyph-utf8](https://github.com/hyphenation/tex-hyphen).

Our Latin hyphenation file also meets that licence, in its version 1.3c, as a modified work: it says so in its header, points to the list of changes in `CHANGELOG.md`, and links to the original.

The licence texts are in `LICENSES/`.

## Sources

- LibreOffice dictionaries: <https://github.com/LibreOffice/dictionaries/tree/master/sr>
- Goran Rakić's repositories: <https://github.com/grakic/hunspell-sr>, <https://github.com/grakic/hyphen-sr>, <https://github.com/grakic/dict-sr-oxt>
- hyph-utf8: <https://github.com/hyphenation/tex-hyphen>
