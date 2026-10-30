#!/usr/bin/env bash
# Odśwież dokładnie dwa obowiązujące PDF-y. Bez GitHub Actions.
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "${1:-}" != "" && "${1:-}" != "--push" ]]; then
  echo "Użycie: bash tools/odswiez_pdf.sh [--push]" >&2
  exit 2
fi

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --disable-pip-version-check --quiet reportlab pymupdf pillow
python tools/build_master.py

python - <<'PY'
from pathlib import Path
import fitz

expected = {
    "Instrukcja_organizatora.pdf": 10,
    "Materialy_do_druku.pdf": 34,
}
for filename, pages in expected.items():
    path = Path(filename)
    with fitz.open(path) as doc:
        assert len(doc) == pages, f"{filename}: {len(doc)} stron zamiast {pages}"
        print(f"OK: {filename} — {len(doc)} stron, {path.stat().st_size:,} bajtów")

with fitz.open("Instrukcja_organizatora.pdf") as doc:
    text = "\n".join(page.get_text() for page in doc)
    assert "5 V" in text and "7294" in text and "USB" in text, "Brak instrukcji silnika USB 5 V"
    assert "NodeMCU" not in text and "L298" not in text, "Nieaktualny opis elektroniki"
with fitz.open("Materialy_do_druku.pdf") as doc:
    text = "\n".join(page.get_text() for page in doc)
    assert "WYMIENNE TARCZE" in text and "WOLNOŚĆ" in text, "Brak tarcz lub zakończenia"
    assert "NodeMCU" not in text and "L298" not in text, "Nieaktualny opis elektroniki"
    assert "WZORY ODBITE LUSTRZANIE" in text, "Brak lustrzanego odbicia tarcz"
    for marker in ["MAPA SIEDMIU ŚWIATÓW", "ETYKIETY NA REKWIZYTY", "STROBOSKOP — OBSŁUGA EKRANU", "CHRONOSKOP — OBSŁUGA"]:
        assert marker in text, f"Brak dodatkowej instrukcji: {marker}"
print("Oba PDF-y zostały odświeżone pod stałymi nazwami.")
PY

if [[ "${1:-}" == "--push" ]]; then
  git add -- Instrukcja_organizatora.pdf Materialy_do_druku.pdf
  if ! git diff --cached --quiet -- Instrukcja_organizatora.pdf Materialy_do_druku.pdf; then
    git commit --only -m "Odśwież dwie obowiązujące publikacje PDF" -- Instrukcja_organizatora.pdf Materialy_do_druku.pdf
    git push
    echo "Nowe PDF-y zapisano na GitHubie."
  else
    echo "PDF-y są już aktualne — bez nowego commita."
  fi
fi
