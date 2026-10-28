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

## Dwa dokumenty w katalogu głównym — wersja obowiązująca

W katalogu głównym znajdują się **dwa dokumenty do używania przy grze**:

- **`Instrukcja_organizatora.pdf`** – 10 stron: przygotowanie domu, kryjówki, wyposażenie, odpowiedzi, zasilanie urządzeń, kontrola przed startem. **Tylko dla dorosłego — zawiera rozwiązania.**
- **`Materialy_do_druku.pdf`** – 25 stron: tylko fizyczne elementy potrzebne do rozstawienia i wręczenia: karty sześciu bestii, trzy lustrzane wiadomości, papierowa instrukcja budowania Enigmy i etykiety jej części, dwie strony z czterema wymiennymi tarczami (7, 4, 2A, 9) i symbole do naklejenia na odwrotach, symbole sześciu książek, siedem pieczęci, etykiety kopert, list Morthara, kartka z zaklęciem i dwa dyplomy.

**Nie drukujemy osobno** planszy puzzli (korzystamy z prawdziwego zestawu 60 elementów) ani opowieści, poradników do mikroskopu, tabel barw rezystorów, dwóch przykładów liczenia oporności, dzienników notatek ani dodatkowych podpowiedzi. Te informacje są na odpowiednich tabletach. Wyjątek: obrazkowa instrukcja montażu Enigmy jest rekwizytem zadania, dlatego zostaje na papierze.

**Wersja obowiązująca:** `Instrukcja_organizatora.pdf` ma 10 stron, a `Materialy_do_druku.pdf` ma 25 stron. Dwie aktualne wersje znajdują się bezpośrednio w katalogu głównym. Nie ma już duplikatów z końcówką `-1`.

### Jak odtworzyć oba PDF-y na Ubuntu

Źródłem do generowania jest `tools/build_master.py`. **Siedem starszych materiałów źródłowych** znajduje się w `assets/zrodla/` (sześć oryginalnych PDF-ów z grafikami i jeden plik PNG). Nowe tarcze 7, 2A i 4 pochodzą z `tarcze_7_2_4_test.pdf` w katalogu głównym; sprawdzona dziewiątka jest odtworzona w generatorze z sześciu odcinków. To zasoby techniczne generatora, **nie są przeznaczone do osobnego drukowania**. Wszystkie starsze wersje wydruków zostały usunięte z katalogów światów.

```bash
cd ~/haloween
git pull
python3 -m venv .venv
source .venv/bin/activate
pip install reportlab pymupdf
HALLOWEEN_ASSET_DIR=. HALLOWEEN_OUT_DIR=. python3 tools/build_master.py
```

Powstaną/odświeżą się pliki `Instrukcja_organizatora.pdf` (10 stron) i `Materialy_do_druku.pdf` (**25 stron**) w katalogu głównym. Nie trzeba przeglądać ani drukować PDF-ów z `assets/zrodla/`. Służą wyłącznie do automatycznego odtwarzania aktualnego pakietu.

Aby zapisać aktualne wersje także na GitHubie:

```bash
git add Instrukcja_organizatora.pdf Materialy_do_druku.pdf
git commit -m "Komplet dokumentów: instrukcja i rekwizyty"
git push
```

Wydruk: A4, rzeczywista skala **100%**, jednostronnie. Przygotuj **prawdziwe puzzle z dokładnie 60 elementów** (nie drukuj ani nie wycinaj papierowych). Ułóż całość, odwróć ją między dwiema sztywnymi tekturami i napisz na rewersie zagadkę o Kasprowym Wierchu atramentem UV. Po wyschnięciu wymieszaj elementy i rozłóż **po 10 prawdziwych puzzli** w kopertach I–VI. Karty z magicznym słowem i list Morthara włóż do skrzyni, nie pozostawiaj ich na widoku.

GitHub Actions może automatycznie regenerować dokumenty, ale jeśli workflow nie ma przydzielonego działającego runnera, należy wykonać polecenia lokalnie. **Najważniejsze są dwa pliki PDF w katalogu głównym**, nie pośrednie dokumenty ani stare wersje.

## Układ repozytorium

- `Instrukcja_organizatora.pdf`, `Materialy_do_druku.pdf` — dwa zbiorcze dokumenty do gry (w materiałach: cztery tarcze 10 cm na dwóch stronach A4).\n- `tarcze_7_2_4_test.pdf` — źródłowy zestaw próbny, w tym rezerwowa dwójka B; nie drukuj go, jeśli korzystasz z pakietu zbiorczego.
- `index.html`, `server.py`, `reset.py` — aplikacja i obsługa stanu gry.
- `Enigma_Doktora_Morsea.ino`, `Mechanizm_Zatrzymanego_Czasu_NodeMCU.ino` — programy mikrokontrolerów (Świat IV: jeden silnik na D1/ENA).
- `tools/build_master.py` — generator obu dokumentów.
- `assets/zrodla/` — źródłowe grafiki, wyłącznie techniczne; **nie drukować osobno**.

## Świat IV — nowa obsługa tarcz\n\nW gabinecie jest **jeden silnik**. Dzieci wybierają jedną z czterech tarcz i sprawdzają **symbol na odwrocie** (Księżyc = 7, Kruk = 2, Klucz = 9, Klepsydra = 4 — przyporządkowanie tylko dla organizatora). Dorosły przy wyłączonym silniku mocuje tarczę taśmą i zamyka osłonę. Po uruchomieniu odczytują cyfrę przy pomocy stroboskopu i zapisują ją obok symbolu. Przed wymianą tarczy dorosły wyłącza zasilanie i czeka na całkowite zatrzymanie. Cztery odczyty przekazują Strażniczce II, która układa symbole według zagadki; **kolejność wymiany tarcz nie jest kolejnością kodu**.\n\n**Stan testów:** tarcza 9 (sześć fragmentów co 60°) była czytelna; tarcze 7, 2A i 4 z najnowszego PDF-u wymagają końcowego sprawdzenia na jednym silniku. Jeśli 2A okaże się nieczytelna, wariant 2B znajduje się na drugiej stronie źródłowego PDF-u. Przed grą przetestuj każdą tarczę; nie zakładaj jednej uniwersalnej częstotliwości błysków.\n\n## Przebieg siedmiu światów

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
