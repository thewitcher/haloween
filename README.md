# 🎃 Klątwa Siedmiu Światów

Kompletna domowa gra escape room dla **Zosi i Emilki** (dwa tablety + laptop z Ubuntu + fizyczne rekwizyty). Siedem światów, 120 minut, dwa zsynchronizowane interfejsy, 60 fragmentów finałowej układanki. Przebieg i odpowiedzi są w `index.html` oraz `server.py`.

## Uruchomienie

```bash
cd ~/haloween
git pull
python3 server.py
```

Adres laptopa: `hostname -I`. Na obu tabletach, połączonych z tym samym Wi-Fi, otwórz `http://ADRES_IP:8000`. Jeden tablet wybiera Strażniczkę I, drugi II. Po wspólnej przysiędze uruchamia się zegar 120 minut. Co 10 minut Morthar może wyświetlać mroczny komunikat bez wpływu na zagadki. Po finałowym słowie zegar się zatrzymuje i aplikacja pokazuje czas gry.

**Reset przed kolejną próbą:** przy uruchomionym serwerze: `python3 reset.py`. Uwaga: usuwa postęp obu graczy; nie używaj go podczas zabawy.

## Jedna dokumentacja i jeden komplet do druku

Docelowy zestaw zawiera dokładnie dwa dokumenty:

- **`01_INSTRUKCJA_ORGANIZATORA.pdf`** – wszystkie kryjówki, przygotowanie urządzeń, odpowiedzi i kontrola przed startem (tylko dla dorosłego).
- **`02_MATERIALY_DO_DRUKU.pdf`** – karty bestii, lustra, etykiety Enigmy, tarcze, symbole książek, karty mikroskopu i rezystorów, pieczęcie I–VII, 60 puzzli, list Morthara, zaklęcie oraz dyplomy.

Źródło odtwarzalne tych dokumentów: **`tools/build_master.py`**. Dopóki oba wygenerowane PDF-y nie zostaną bezpiecznie skopiowane do folderu `docs/` w repozytorium, **stare PDF-y w katalogach światów stanowią materiały źródłowe i nie wolno ich usuwać**.

Wersja lokalna / odtworzenie PDF-ów:

```bash
cd ~/haloween
python3 -m venv .venv
source .venv/bin/activate
pip install reportlab pymupdf
mkdir -p docs
HALLOWEEN_ASSET_DIR=. HALLOWEEN_OUT_DIR=docs python3 tools/build_master.py
```

Efekt: `docs/01_INSTRUKCJA_ORGANIZATORA.pdf` (10 stron) i `docs/02_MATERIALY_DO_DRUKU.pdf` (37 stron). Drukowanie: format A4, **skala 100%**, najlepiej pojedynczo. Stronę puzzli drukuj na kartonie i potnij dopiero **po naniesieniu i wyschnięciu tekstu UV na odwrocie**.

Możesz zapisać wynik w repozytorium:

```bash
git add docs/01_INSTRUKCJA_ORGANIZATORA.pdf docs/02_MATERIALY_DO_DRUKU.pdf
git commit -m "Dwa kompletne PDF-y na wszystkie światy"
git push
```

**Uwaga dotycząca automatyzacji:** Workflow `.github/workflows/build-materials.yml` jest przygotowany do generowania PDF-ów, ale wymaga działających runnerów GitHub Actions. Jeśli Actions nie przydziela runnera, użyj powyższej metody lokalnej. Nie usuwaj plików źródłowych przed zweryfikowaniem wyniku.

## Przebieg siedmiu światów

| Świat | Pokój | Mechanika |
| --- | --- | --- |
| I | Salon | Karty sześciu bestii i kod 7219. |
| II | Sypialnia | Lustrzane kartki i zdanie NOC MA OCZY. |
| III | Kuchnia | Arduino UNO, alfabet Morse’a, terminal i hasło BURZA. |
| IV | Gabinet | Cztery silniki, papierowe tarcze, stroboskop i kod 7294. |
| V | Pokój Emilki | Sześć ksiąg, rozumowanie, atrament UV, imię MORWENA. |
| VI | Pokój Zosi | Sześć kopert UV, mikroskop, rezystory i hasło PRĄDEM. |
| VII | Garderoba | 60 puzzli, Kasprowy Wierch, kłódka 1987, skrzynia i słowo WOLNOŚĆ. |

Każda z pierwszych sześciu kopert ze zdobywaną pieczęcią zawiera **dokładnie 10 kawałków puzzli**. W finale układanka złożona z 60 kawałków, po odwróceniu i oświetleniu UV, ujawnia wskazówkę do zamka.

## Bezpieczeństwo

Cała gra pracuje tylko w zaufanej sieci domowej, nie publikuj portu 8000 w Internecie. Dorośli sprawdzają elektronikę przy odłączonym zasilaniu. Silniki mają osłony; nie kierujemy migającego stroboskopu ani światła UV w oczy. Małe elementy nie są przeznaczone do wkładania do ust. Jeśli uczestniczka jest wrażliwa na błyski, zrezygnuj ze stroboskopu i przygotuj alternatywne ujawnienie cyfr.

Repozytorium jest publiczne. Nie zapisuj w nim danych wrażliwych ani haseł z domowych usług.
