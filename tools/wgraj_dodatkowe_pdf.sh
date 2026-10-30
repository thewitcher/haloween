#!/usr/bin/env bash
# Przenosi cztery dodatkowe PDF-y z ZIP-a z rozmowy do repozytorium.
# Uwaga: repozytorium jest publiczne. Mapa pokazuje układ domu i domyślnie NIE jest publikowana.
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ${1:-} == "" ]]; then
  echo "Użycie: bash tools/wgraj_dodatkowe_pdf.sh /sciezka/Dodatkowe_instrukcje_Siedem_Swiatow.zip [--z-mapa]" >&2
  exit 2
fi
ZIP_PATH="$(realpath "$1")"
[[ -f "$ZIP_PATH" ]] || { echo "Nie znaleziono ZIP: $ZIP_PATH" >&2; exit 1; }
INCLUDE_MAP=false
if [[ ${2:-} == "--z-mapa" ]]; then INCLUDE_MAP=true; fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python3 -m zipfile -e "$ZIP_PATH" "$TMP"
mkdir -p dodatkowe_instrukcje

FILES=(
  "Etykiety_Chronoskop_i_Skrzynia.pdf"
  "Instrukcja_Stroboskopu.pdf"
  "Instrukcja_Chronoskopu.pdf"
)
if [[ "$INCLUDE_MAP" == true ]]; then
  echo "UWAGA: repozytorium jest PUBLICZNE, a mapa ujawnia rozkład pomieszczeń domu."
  read -r -p "Aby opublikować mapę, wpisz DOKLADNIE 'TAK': " APPROVE
  [[ "$APPROVE" == "TAK" ]] || { echo "Anulowano publikowanie mapy."; exit 1; }
  FILES+=("Mapa_Siedmiu_Swiatow.pdf")
else
  echo "Mapa pominięta ze względu na prywatność. Aby ją opublikować, użyj --z-mapa."
fi

for name in "${FILES[@]}"; do
  [[ -f "$TMP/$name" ]] || { echo "Brak pliku $name w ZIP-ie" >&2; exit 1; }
  [[ "$(head -c 4 "$TMP/$name")" == "%PDF" ]] || { echo "Nieprawidłowy PDF: $name" >&2; exit 1; }
  cp "$TMP/$name" "dodatkowe_instrukcje/$name"
done

git add -- "${FILES[@]/#/dodatkowe_instrukcje/}"
if git diff --cached --quiet -- "${FILES[@]/#/dodatkowe_instrukcje/}"; then
  echo "Dokumenty w repozytorium są już aktualne."
else
  git commit -m "Dodaj dodatkowe instrukcje i etykiety Siedmiu Światów" -- "${FILES[@]/#/dodatkowe_instrukcje/}"
  git push
  echo "Dokumenty przesłano na GitHub."
fi
