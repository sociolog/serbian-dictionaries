#!/bin/sh
# Zamenjuje srpske rečnike OnlyOffice Desktop Editors-a našim ispravljenim (this repository).
# Replaces OnlyOffice Desktop Editors' Serbian dictionaries with our corrected set (this repository).
#
# Pokretanje / run:   sh tools/install-onlyoffice.sh            (install ours, back up the originals)
#                     sh tools/install-onlyoffice.sh --restore  (put OnlyOffice's originals back)
# Traži administratorsku lozinku (sudo). Posle svakog ažuriranja OnlyOffice-a pokrenuti ponovo.
# Asks for the administrator password (sudo). Run it again after every OnlyOffice update.
set -eu

SRC=$(cd "$(dirname "$0")/.." && pwd)
DICTS=/opt/onlyoffice/desktopeditors/dictionaries
BACKUP="$HOME/.local/share/onlyoffice-srpski-backup"

[ -d "$DICTS/sr_Cyrl_RS" ] && [ -d "$DICTS/sr_Latn_RS" ] || { echo "OnlyOffice dictionaries not found in $DICTS" >&2; exit 1; }

# our file -> OnlyOffice's file
MAP="sr_Cyrl_RS/sr_Cyrl_RS.aff:sr_Cyrl_RS/sr_Cyrl_RS.aff
sr_Cyrl_RS/sr_Cyrl_RS.dic:sr_Cyrl_RS/sr_Cyrl_RS.dic
sr_Cyrl_RS/hyph_sr_Cyrl_RS.dic:sr_Cyrl_RS/hyph_sr_Cyrl_RS.dic
sr_Latn_RS/sr_Latn_RS.aff:sr_Latn_RS/sr_Latn_RS.aff
sr_Latn_RS/sr_Latn_RS.dic:sr_Latn_RS/sr_Latn_RS.dic
sr_Latn_RS/hyph_sr_Latn_RS.dic:sr_Latn_RS/hyph_sr_Latn_RS.dic"

if [ "${1:-}" = "--restore" ]; then
    [ -d "$BACKUP" ] || { echo "No backup in $BACKUP" >&2; exit 1; }
    while IFS=: read -r ours theirs; do
        sudo install -m 644 "$BACKUP/$theirs" "$DICTS/$theirs"
    done <<EOF
$MAP
EOF
    echo "OnlyOffice's own Serbian dictionaries are back. Restart OnlyOffice."
    exit 0
fi

while IFS=: read -r ours theirs; do
    [ -f "$SRC/$ours" ] || { echo "Missing $SRC/$ours" >&2; exit 1; }
done <<EOF
$MAP
EOF

# Back up OnlyOffice's originals once (a second run keeps the first backup).
if [ ! -d "$BACKUP" ]; then
    while IFS=: read -r ours theirs; do
        mkdir -p "$BACKUP/$(dirname "$theirs")"
        cp -p "$DICTS/$theirs" "$BACKUP/$theirs"
    done <<EOF
$MAP
EOF
    echo "Originals backed up to $BACKUP"
fi

while IFS=: read -r ours theirs; do
    sudo install -m 644 "$SRC/$ours" "$DICTS/$theirs"
    echo "  $ours -> $DICTS/$theirs"
done <<EOF
$MAP
EOF
echo "Done. Restart OnlyOffice; Serbian (Cyrillic) and Serbian (Latin) now use our dictionaries."
