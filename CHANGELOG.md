# Changes

Each version lists what changed from the one before. Version 1.0 lists what changed from the July 2019 files of Milutin Smiljanić's Korektor, which were in `source/2019/` until 1.1.

## 1.1.1

- **Spelling:** eight entries that 1.1 added are out again: `адхерентност`, `Надал`, `Ноле`, `Федерер` (two entries each for the names) and `РСД`. Their stems and forms were taken from Korektor's files, which are under GNU GPL 3 and LGPL 3 only, so they don't belong in a dictionary offered under the three licences. These words are rejected again, as in LibreOffice; everything else is as in 1.1. `corrections.tsv` now has 147 entries out and 348 in.

## 1.1

- **Base and licence:** the spelling dictionaries are now built on LibreOffice's Serbian dictionary, version 2019.04.19 (LibreOffice dictionaries commit 4f1df64, in `source/libreoffice/`), which Milutin Smiljanić offers under GNU LGPL 3 or later, MPL 2 or later, or GNU GPL 3 or later.
  - 1.0 and 1.0.1 were built on the July 2019 files of his Korektor ([msmiljan/korektor](https://github.com/msmiljan/korektor), commit e56d916), byte for byte. He offers those under GNU GPL 3 (the repository) and GNU LGPL 3 (its LibreOffice extension) only.
  - The README of those versions gave them the three licences of the LibreOffice version, which their source doesn't state. The 2.9% of stems it called of unknown origin are his own later edits.
- **Spelling:** everything 1.0.1 accepts is still accepted, in both scripts. Newly accepted are 5,027 lowercase forms of place names that 1.0.1 has capitalised (`земун`, `дармштат`), as LibreOffice accepts them, and 16 lowercase place-name stems (`каспиј`, `лакадив`).
- **Corrections:** `corrections.tsv` now lists edits on LibreOffice's file, with its affix classes: 147 entries out, 356 in. That covers:
  - every correction of 1.0.1. LibreOffice's file already had some of them, such as the 90 capitalised place names, which it accepts through their lowercase entries;
  - 15 entries that keep the correct forms of entries taken out (`сип/1125` gave `сипски`; `сип` stays);
  - fixes for errors in LibreOffice's file that Korektor no longer has:
    - a Latin `o` in the instrumental ending of nouns in -ац (`Барајевцoм`), corrected in `aff-fixes.tsv`, and a Latin letter in `корејa` and `папратиштe`;
    - misspellings: `изказати` (for `исказати`), `монофизтски`, `унитаризција`, `америћки`, and `Емпедоклетов` (for `Емпедоклов`);
    - forms it lacked: the case forms of `папратиште`, `адхерентност`, and `Надал`, `Федерер`, `Ноле` and `РСД`.
- **Hyphenation:** unchanged. These files are Smiljanić's too, from Korektor, and their licence is now given as that of his extension, GNU LGPL 3. The Latin file's header named LibreOffice's file as its original; it now names Korektor's.
- **Tools:** `tools/apply_corrections.py` builds the spelling dictionaries from `source/libreoffice/`, `corrections.tsv`, `aff-fixes.tsv` and `tables/`. `tools/port_libreoffice.py` applies the same corrections to a checkout of LibreOffice's dictionaries, matching them by word forms, and `tools/check_libreoffice.py` checks the result.

## 1.0.1

- **Spelling:** 90 place names are in, in the nominative only: `Требевић`, `Бјелашница`, `Зрмања`, `Шолта`, `Ладога`, `Лузон`, `Хиспањола` and others. LibreOffice's dictionary accepts them, and 1.0 accepted only their adjectives (`требевићки`, `ладошки`). LibreOffice has them in lowercase, which also lets `требевић` through; here they are capitalised. Their case forms, such as `Требевића`, are still marked, as in LibreOffice.
- **Suggestions:** the `KEY` line in both `.aff` files had a Latin `s` among the Cyrillic letters (`sџцвбнм`, and `sdžcvbnm` in the Latin file). It is gone. LibreOffice's file has the same error.

## 1.0

- **Hyphenation, Latin:** 35 root patterns mark the words where `nj` or `dž` is two letters (`kon-ju-ga-ci-ja`, `nad-ži-ve-ti`, `pod-že-lu-dač-ni`), while words such as `kanjon` and `odžak` keep one letter. They add 512 lines to the file, and `patterns/sr-latn-additions.pat` holds them in raw form.
- **Hyphenation, Cyrillic:** unchanged.
- **File names:** `sr_Cyrl_RS` and `sr_Latn_RS` in place of `sr_RS` and `sh_RS` (see the README). The InDesign archive keeps the old names.
- **Spelling:** 139 entries removed and 364 added, each listed in `corrections.tsv` with its source:
  - Forms it doesn't accept are gone: `кљешта`, `гњездо`, `раздјел`, `мршавети`, and the long-stem comparatives such as `лијепши`.
  - Dictionary errors are gone: `онјлајн`, `онлјан`, `понједељак`.
  - 100 misspelled words found in a review of rare words are gone, such as `изашто`, `сипски`, `раденик` and `објезбеђење`. Each was read by a Serbian speaker.
  - Spellings with `њ` for `нј` are gone from Cyrillic: `коњугација`, `коњунктив` and their relatives, 11 entries.
  - Missing words are in: `бијел`, `цијел`, `рјеђи`, `бједнији`, `тјешњи`, `сњегови`, `инјунктив`, `предио` and others.
  - 72 ijekavian forms are in, each the twin of an ekavian word already here and confirmed by the Rečnik srpskoga jezika (Matica srpska, 2011). Only the marked pairs were compared.
  - 186 standard words are in, chosen by hand from the Rečnik headwords the dictionary rejected: words it lacked (`динозаур`, `егида`, `козле`, `страван`) and common nouns it had only capitalised (`љубица`, `копар`, `калина`). Names and rare and regional words stayed out.
  - Common words it rejected are in: `итекако`, `лејди`, `вебсајт`, and the forms `мишем`, `венцем`, `вијенцем`, `шоуа`.
  - No text from the Rečnik is included.
- **Suggestions:** both `.aff` files now have `MAP`, `TRY` and `REP` tables, so a misspelled word gets a better suggestion. `racunar` now offers `računar` first, `skola` offers `škola`, and `djak` offers `đak`. Spell-checking itself doesn't change, only the suggestions. The rules and word forms in these files are as they were.
  - `MAP` lists letters people swap: `c`, `č`, `ć` and the like, with capitals, because many people type Latin without diacritics. Each group uses single letters only, because not every program reads grouped letters such as `(dj)`.
  - `TRY` lists the letters by how often they occur in this dictionary.
  - `REP` covers `dj` for `đ`, `dz` for `dž`, and `ije` for `je` and the reverse.
