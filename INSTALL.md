# Installing

Each program wants the files in its own place and, for InDesign, under its own names. Download the archive for your program from the [releases](https://github.com/sociolog/serbian-dictionaries/releases), or use the folders in this repository directly.

| Program | Archive | Status |
|---|---|---|
| ONLYOFFICE Desktop Editors (Linux) | `serbian-dictionaries-<version>.zip` | Script below |
| Adobe InDesign | `serbian-dictionaries-<version>-indesign.zip` | Steps below |
| DesignCraft | `serbian-dictionaries-<version>.zip` | Once its Serbian support is merged |
| WordCraft | `serbian-dictionaries-<version>.zip` | Once its Serbian support is merged |
| LibreOffice | — | Not packaged yet |

`sr_Cyrl_RS` is Cyrillic and `sr_Latn_RS` is Latin. Both serve Serbia, Bosnia and Herzegovina, and Montenegro (see the README).

## ONLYOFFICE Desktop Editors (Linux)

ONLYOFFICE already has Serbian dictionaries under these names. The script replaces them with this set and keeps the originals.

1. Unpack `serbian-dictionaries-<version>.zip`.
2. In the unpacked folder, run:

   ```sh
   sh tools/install-onlyoffice.sh
   ```

   It asks for the administrator password, because the files are in `/opt/onlyoffice/desktopeditors/dictionaries/`. The originals go to `~/.local/share/onlyoffice-srpski-backup/`.
3. Restart ONLYOFFICE.

An ONLYOFFICE update brings its own files back, so run the script again after one. To go back to ONLYOFFICE's own dictionaries:

```sh
sh tools/install-onlyoffice.sh --restore
```

## Adobe InDesign

InDesign has no Serbian of its own. It takes the dictionaries through its Hunspell plug-in, which needs two folders and two lines in its settings file. These steps come from InDesign 2020 on Windows. Other versions keep the files in the same place inside their own folder, but check before you replace anything.

1. Unpack `serbian-dictionaries-<version>-indesign.zip`. It has two folders: `sr_RS` (Cyrillic) and `sh_RS` (Latin). Keep these names: they are the ones InDesign knows.
2. Close InDesign.
3. Copy both folders into the plug-in's dictionary folder:

   ```text
   C:\Program Files\Adobe\Adobe InDesign 2020\Resources\Dictionaries\LILO\Linguistics\Providers\Plugins2\AdobeHunspellPlugin\Dictionaries
   ```

4. One folder up, in `AdobeHunspellPlugin`, make a copy of `Info.plist` as a backup. Then open `Info.plist` in a text editor. It has a list of languages under each of three keys: `SpellingService`, `HyphenationService` and `UserDictionaryService`. Add these two lines to each list, for example after `<string>ru_RU</string>`:

   ```xml
   <string>sr_RS</string>
   <string>sh_RS</string>
   ```

   Only add lines. The file belongs to InDesign, so don't replace it with a copy from another version.
5. Start InDesign. The language list now has **Serbian (Cyrillic)** and **Serbian (Latin)**.

An InDesign update may replace `Info.plist`. If Serbian disappears from the list, add the lines again.

## DesignCraft

DesignCraft reads these files as they are, under their names in this repository. Serbian support is waiting to be merged ([hyphenation](https://github.com/storytold/designcraft/pull/1874), [spelling](https://github.com/storytold/designcraft/pull/1875)). Once it is, copy the folders `sr_Cyrl_RS` and `sr_Latn_RS` into DesignCraft's `dictionaries` folder:

| System | Folder |
|---|---|
| Linux | `~/.config/designcraft/dictionaries/` |
| macOS | `~/Library/Application Support/DesignCraft/dictionaries/` |
| Windows | `%APPDATA%\DesignCraft\dictionaries\` |

Then restart DesignCraft.

## WordCraft

Serbian support for WordCraft is waiting to be merged ([wordcraft#4447](https://github.com/storytold/wordcraft/pull/4447)). These instructions will follow once it is.

## LibreOffice

LibreOffice ships an older version of these dictionaries. It takes new dictionaries as an extension (`.oxt`), which this repository doesn't build yet.
