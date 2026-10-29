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
python -m pip install --disable-pip-version-check --quiet reportlab pymupdf
python tools/build_master.py

python - <<'PY'
from pathlib import Path
import fitz

expected = {
    "Instrukcja_organizatora.pdf": 10,
    "Materialy_do_druku.pdf": 27,
}
for filename, pages in expected.items():
    path = Path(filename)
    with fitz.open(path) as doc:
        assert len(doc) == pages, f"{filename}: {len(doc)} stron zamiast {pages}"
        print(f"OK: {filename} — {len(doc)} stron, {path.stat().st_size:,} bajtów")

with fitz.open("Instrukcja_organizatora.pdf") as doc:
    text = "\n".join(page.get_text() for page in doc)
    assert "5 V" in text and "7294" in text, "Brak nowej instrukcji silnika 5 V"
with fitz.open("Materialy_do_druku.pdf") as doc:
    text = "\n".join(page.get_text() for page in doc)
    assert "WYMIENNE TARCZE" in text and "WOLNOŚĆ" in text, "Brak tarcz lub zakończenia"
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
