# Changes

Each version lists what changed from the one before. Version 1.0 lists what changed from the July 2019 files in `source/2019/`.

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
