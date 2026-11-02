# Plan: strict ekavian and ijekavian lists

Status: set aside on 2026-10-31. We keep one combined dictionary, which is simpler for every program that uses it. This plan stays only as a record, in case mixing checks are wanted later.

## Why

The Pravopis treats ekavian and ijekavian as equal and leaves the choice free, but it doesn't allow mixing them in one text, outside artistic works (point 6). The current dictionaries accept both, so `млеко` in an ijekavian text gets no warning.

Separate lists are the more robust solution for that one job. They don't replace the combined dictionary: it stays as the default, because it can't reject a correct word for the wrong pronunciation. Strict lists are an option a writer turns on.

## What we already know

- The Latin dictionary is an exact transliteration of the Cyrillic one, so there is one source and two outputs.
- A simple rule pairs 5,681 ijekavian stems with an ekavian twin among LibreOffice's 163,565, and samples look right. This counts stems, not forms, and uses the LibreOffice list.
- The dictionary also has mixed entries, such as `бјелосветски` and `блиједети`. These are errors in either list.
- Hyphenation needs no change: `ије` is two syllables (point 8а).

## Design

Each entry in the Cyrillic source gets one of three marks, kept in a data file beside `corrections.tsv`:

- **Common:** the same in both, such as `бреза`, `срећа`, `кисео`.
- **Ekavian only:** such as `млеко`.
- **Ijekavian only:** such as `млијеко`.

The build then writes:

| Set | Tag | Contents |
|---|---|---|
| Combined | `sr-Cyrl`, `sr-Latn` | Everything, as now |
| Ekavian | `sr-Cyrl-ekavsk`, `sr-Latn-ekavsk` | Common and ekavian |
| Ijekavian | `sr-Cyrl-ijekavsk`, `sr-Latn-ijekavsk` | Common and ijekavian |

Unmarked entries count as common, so a word never disappears from a list by accident. A missed pair only means one mix goes uncaught.

## Steps

1. **Classify.** Extend the rule to the Pravopis patterns: `ије`/`е`, `је`/`е`, `ље`/`ле`, `ње`/`не`, `ио`/`ео`, `ија`/`еја`, and `пре-`/`прије-`.
2. **Handle the exceptions:**
   - Foreign words where `ије` isn't jat (`ентеријер`, `бомбонијера`) stay common.
   - Words that are the same in both (point 8д) stay common.
   - Doublets the Pravopis allows stay in the ijekavian list (points 8е, 9, 10), such as `вијекови` and `вјекови`.
   - Forms it allows in both (point 11) stay common, such as `првенство` and `кисео`.
   - Entries with mixed forms are fixed or removed.
3. **Handle names.** Names keep their own form (point 12: `Београд`, `Бијељина`, `Пријепоље`), so they stay common.
4. **Review.** Group the pairs by rule and check samples first. Ask Vladimir to review the uncertain groups, and you to spot-check the rest.
5. **Build and test.** Every Pravopis example must pass in the right list, and the other pronunciation's forms must be flagged. Run real texts of each pronunciation and count false alarms.
6. **Connect to programs:**
   - DesignCraft needs two new language entries and a dictionary choice by variant. It already reads the tags as Serbian.
   - WordCraft: to be checked once #4447 is settled.
   - LibreOffice and OnlyOffice: to be checked. Neither lists these tags today, so they would be new requests.

## Done means

- Mixed test text is flagged in both directions, in both scripts.
- A real text in one pronunciation gets almost no false alarms. We'd set the exact limit after the first measurement.
- The combined dictionary behaves as before.
- Contributors, licences and every change stay recorded.

## Open questions

- How should a program choose by default? The Pravopis ties the choice to the writer, not the region, so we'd default to combined everywhere and not assume `BA` or `ME` means ijekavian.
- Montenegrin usage: point 8д notes widespread ekavian forms there, such as `речник`, beside the standard `рјечник`. Should the ijekavian list warn about these?
- Do we also want a report that says which pronunciation a text uses and where it departs, rather than only marking words?
