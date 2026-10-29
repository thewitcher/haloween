# 🎃 Klątwa Siedmiu Światów

Kompletna domowa gra escape room dla **Zosi i Emilki** (dwa tablety + laptop z Ubuntu + fizyczne rekwizyty). Siedem światów, 120 minut, dwa zsynchronizowane interfejsy, 60 **prawdziwych** puzzli w finale. Przebieg i odpowiedzi są w `index.html` oraz `server.py`.

## Uruchomienie

```bash
cd ~/haloween
git pull
python3 server.py
```

Adres laptopa: `hostname -I`. Na obu tabletach, połączonych z tym samym Wi-Fi, otwórz `http://ADRES_IP:8000`. Jeden tablet wybiera Strażniczkę I, drugi II. Po wspólnej przysiędze uruchamia się zegar 120 minut. Co 10 minut Morthar może wyświetlać mroczny komunikat bez wpływu na zagadki. Po finałowym słowie zegar się zatrzymuje i aplikacja pokazuje czas gry.

**Reset przed kolejną próbą:** przy uruchomionym serwerze: `python3 reset.py`. Uwaga: usuwa postęp obu graczy; nie używaj go podczas zabawy.

## Dwa obowiązujące PDF-y — bez GitHub Actions

W katalogu głównym używamy **wyłącznie dwóch dokumentów**. Przy kolejnych poprawkach zachowujemy ich nazwy i zastępujemy zawartość:

- **`Instrukcja_organizatora.pdf`** — 10 stron; przygotowanie siedmiu światów, rozwiązania i bezpieczeństwo. **Tylko dla dorosłego.**
- **`Materialy_do_druku.pdf`** — 27 stron; 6 etykiet kopert z nazwami światów, 7 tabliczek na drzwi, karty, pieczęcie, instrukcja Enigmy, cztery wymienne tarcze 10 cm na dwóch kartkach A4, symbole na odwroty, list i dyplomy.

**Ważne:** jeśli PDF-y w repozytorium mają jeszcze starszą treść, trzeba je jednokrotnie odświeżyć lokalnie. Zmiana generatora nie zmienia automatycznie gotowych plików PDF. Nie ma już workflow GitHub Actions.

### Aktualizacja PDF-ów na Ubuntu — jedno polecenie

W terminalu w katalogu repozytorium:

```bash
cd ~/haloween
git pull
bash tools/odswiez_pdf.sh --push
```

Skrypt sam tworzy lokalne środowisko `.venv`, instaluje `reportlab` i `pymupdf`, generuje i kontroluje **te same dwa PDF-y**, a z opcją `--push` zapisuje je do repozytorium GitHub. Jeśli chcesz tylko wygenerować pliki na laptopie, bez wysyłania ich na GitHub, uruchom `bash tools/odswiez_pdf.sh`. Jeśli Ubuntu zgłasza brak modułu `venv`, zainstaluj `python3-venv`.

Nie trzeba niczego klikać w GitHub Actions. Nie tworzymy dodatkowych wersji typu „final”, „nowy”, „5V” czy „poprawiony”.

### Materiały źródłowe a druk

Generator `tools/build_master.py` korzysta z grafik w `assets/zrodla/` oraz z pliku `tarcze_7_2_4_test.pdf` w katalogu głównym. Są to **źródła techniczne**, nie osobne obowiązujące materiały do druku. Tarcza 9 jest odtworzona z sześciu segmentów, a 7, 2A i 4 pochodzą z nowszego zestawu próbnego.

Drukuj `Materialy_do_druku.pdf` na A4 w **skali 100%**. Strona 1 zawiera etykiety sześciu dużych kopert, a strony 2–3 tabliczki na drzwi siedmiu światów. Na etykietach dla dzieci są nazwy magicznych światów, nie nazwy pomieszczeń. Rozmieszczenie: I – salon, II – sypialnia, III – kuchnia, IV – gabinet, V – pokój Emilki, VI – pokój Zosi, VII – garderoba. Nie podpisuj widzialnym tuszem sześciu małych kopert z rezystorami. Do finału używamy jednego **prawdziwego zestawu 60 puzzli**; nie drukujemy papierowych puzzli. Układamy je, nanosimy wspólną wskazówkę na odwrocie tuszem UV, a następnie dzielimy na sześć kopert po dziesięć elementów.

## Układ repozytorium

- `Instrukcja_organizatora.pdf`, `Materialy_do_druku.pdf` — dwa zbiorcze dokumenty do gry (w materiałach: cztery tarcze 10 cm na dwóch stronach A4).
- `tarcze_7_2_4_test.pdf` — źródłowy zestaw próbny, w tym rezerwowa dwójka B; nie drukuj go, jeśli korzystasz z pakietu zbiorczego.
- `index.html`, `server.py`, `reset.py` — aplikacja i obsługa stanu gry.
- `Enigma_Doktora_Morsea.ino` — program Arduino UNO używanego w Świecie III.
- `Mechanizm_Zatrzymanego_Czasu_NodeMCU.ino` — zachowany archiwalny skecz, **niepotrzebny w aktualnej wersji Świata IV**.
- `tools/build_master.py` — generator obu dokumentów.
- `assets/zrodla/` — źródłowe grafiki, wyłącznie techniczne; **nie drukować osobno**.

## Świat IV — nowa obsługa tarcz

W gabinecie jest **jeden silnik DC 3–6 V zasilany bezpośrednio z 5 V** — bez NodeMCU i L298N. Można dodać prosty wyłącznik o parametrach odpowiednich do prądu silnika. Schemat: **+5 V → opcjonalny wyłącznik → + silnika**, a **– silnika → GND zasilacza**. Zasilacz powinien zapewnić prąd rozruchowy silnika. Przewody zabezpiecz przed zwarciem. Dzieci wybierają jedną z czterech tarcz i sprawdzają **symbol na odwrocie** (Księżyc = 7, Kruk = 2, Klucz = 9, Klepsydra = 4 — przyporządkowanie tylko dla organizatora). Dorosły przy odłączonym zasilaniu i zatrzymanym silniku mocuje tarczę taśmą i zamyka osłonę. Po uruchomieniu odczytują cyfrę przy pomocy stroboskopu i zapisują ją obok symbolu. Przed wymianą tarczy dorosły wyłącza zasilanie i czeka na całkowite zatrzymanie. Cztery odczyty przekazują Strażniczce II, która układa symbole według zagadki; **kolejność wymiany tarcz nie jest kolejnością kodu**.

**Stan testów:** tarcza 9 (sześć fragmentów co 60°) była czytelna; tarcze 7, 2A i 4 z najnowszego PDF-u wymagają końcowego sprawdzenia na jednym silniku. Jeśli 2A okaże się nieczytelna, wariant 2B znajduje się na drugiej stronie źródłowego PDF-u. Przed grą przetestuj każdą tarczę; nie zakładaj jednej uniwersalnej częstotliwości błysków.

## Przebieg siedmiu światów

| Świat | Pokój | Mechanika |
| --- | --- | --- |
| I | Salon | Karty sześciu bestii i kod 7219. |
| II | Sypialnia | Lustrzane kartki i zdanie NOC MA OCZY. |
| III | Kuchnia | Arduino UNO, alfabet Morse’a, terminal i hasło BURZA. |
| IV | Gabinet | Jeden osłonięty silnik, cztery wymienne tarcze z symbolami na odwrotach, stroboskop i kod 7294. |
| V | Pokój Emilki | Sześć ksiąg, rozumowanie, atrament UV, imię MORWENA. |
| VI | Pokój Zosi | Sześć kopert UV, mikroskop, rezystory i hasło PRĄDEM. |
| VII | Garderoba | 60 prawdziwych puzzli, Kasprowy Wierch, kłódka 1987, skrzynia i słowo WOLNOŚĆ. |

Każda z pierwszych sześciu kopert ze zdobywaną pieczęcią zawiera **dokładnie 10 kawałków puzzli**. W finale układanka złożona z 60 kawałków, po odwróceniu i oświetleniu UV, ujawnia wskazówkę do zamka.

## Bezpieczeństwo

Cała gra pracuje tylko w zaufanej sieci domowej, nie publikuj portu 8000 w Internecie. Dorośli sprawdzają elektronikę przy odłączonym zasilaniu. Wirujący silnik z tarczą ma osłonę; tarcze wymienia dorosły dopiero po wyłączeniu i całkowitym zatrzymaniu, mocując je taśmą; nie kierujemy migającego stroboskopu ani światła UV w oczy. Małe elementy nie są przeznaczone do wkładania do ust. Jeśli uczestniczka jest wrażliwa na błyski, zrezygnuj ze stroboskopu i przygotuj alternatywne ujawnienie cyfr.

Repozytorium jest publiczne. Nie zapisuj w nim danych wrażliwych ani haseł z domowych usług.
