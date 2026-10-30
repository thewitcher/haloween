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
- **`Materialy_do_druku.pdf`** — 34 strony; mapa siedmiu światów, małe etykiety Chronoskopu i Skrzyni Morthara, instrukcja stroboskopu (2 strony), obrazkowa instrukcja Chronoskopu (3 strony), 6 etykiet kopert z nazwami światów, 7 tabliczek na drzwi, karty, pieczęcie, instrukcja Enigmy, cztery wymienne tarcze 10 cm na dwóch kartkach A4, symbole na odwroty, list i dyplomy.

**Ważne:** jeśli PDF-y w repozytorium mają jeszcze starszą treść, trzeba je jednokrotnie odświeżyć lokalnie. Zmiana generatora nie zmienia automatycznie gotowych plików PDF. Nie ma już workflow GitHub Actions.

### Aktualizacja PDF-ów na Ubuntu — jedno polecenie

W terminalu w katalogu repozytorium:

```bash
cd ~/haloween
git pull
bash tools/odswiez_pdf.sh --push
```

**Ważne:** siedem dodatkowych stron (mapa, etykiety, instrukcje) znajduje się wewnątrz głównego `Materialy_do_druku.pdf`. Generator zachowuje je z już istniejącego 34-stronicowego dokumentu. Dlatego najpierw należy jednorazowo wgrać do repozytorium kompletne dwa PDF-y z tej rozmowy. Potem każde kolejne uruchomienie generatora zachowuje te strony bez osobnych plików.

Skrypt sam tworzy lokalne środowisko `.venv`, instaluje `reportlab` i `pymupdf`, generuje i kontroluje **te same dwa PDF-y**, a z opcją `--push` zapisuje je do repozytorium GitHub. Jeśli chcesz tylko wygenerować pliki na laptopie, bez wysyłania ich na GitHub, uruchom `bash tools/odswiez_pdf.sh`. Jeśli Ubuntu zgłasza brak modułu `venv`, zainstaluj `python3-venv`.

Nie trzeba niczego klikać w GitHub Actions. Nie tworzymy dodatkowych wersji typu „final”, „nowy”, „5V” czy „poprawiony”.

### Materiały źródłowe a druk

Generator `tools/build_master.py` korzysta z grafik w `assets/zrodla/` oraz z pliku `tarcze_7_2_4_test.pdf` w katalogu głównym. Są to **źródła techniczne**, nie osobne obowiązujące materiały do druku. Tarcza 9 jest odtworzona z sześciu segmentów, a 7, 2B i 4 pochodzą z zestawu próbnego. W teście 2A była widoczna jako 5, a 2B jako prawidłowa 2. **Wydrukowane wzory wszystkich czterech tarcz (7, 2B, 9, 4) są teraz odbite lustrzanie dla ustalonego kierunku obrotów silnika.** Podpisy, etykiety i symbole na odwrocie pozostają normalne. Po zmianie wzorów wymagany jest ponowny test stroboskopowy każdej tarczy.

Drukuj `Materialy_do_druku.pdf` na A4 w **skali 100%**. Strona 1 zawiera etykiety sześciu dużych kopert, strony 2–3 tabliczki na drzwi siedmiu światów, strona 4 mapę, a strona 5 małe etykiety na Chronoskop i Skrzynię Morthara. Strony 21–22 to instrukcja stroboskopu, a strony 23–25 — obrazkowa instrukcja Chronoskopu. Na etykietach dla dzieci są nazwy magicznych światów, nie nazwy pomieszczeń. Rozmieszczenie: I – salon, II – sypialnia, III – kuchnia, IV – gabinet, V – pokój Emilki, VI – pokój Zosi, VII – garderoba. Nie podpisuj widzialnym tuszem sześciu małych kopert z rezystorami. Do finału używamy jednego **prawdziwego zestawu 60 puzzli**; nie drukujemy papierowych puzzli. Układamy je, nanosimy wspólną wskazówkę na odwrocie tuszem UV, a następnie dzielimy na sześć kopert po dziesięć elementów.

## Układ repozytorium

- `Instrukcja_organizatora.pdf`, `Materialy_do_druku.pdf` — dwa zbiorcze dokumenty do gry (w materiałach: cztery tarcze 10 cm na dwóch stronach A4).
- `tarcze_7_2_4_test.pdf` — źródłowy zestaw próbny, w tym rezerwowa dwójka B; nie drukuj go, jeśli korzystasz z pakietu zbiorczego.
- `index.html`, `server.py`, `reset.py` — aplikacja i obsługa stanu gry.
- `Enigma_Doktora_Morsea.ino` — program Arduino UNO używanego w Świecie III.
- `tools/build_master.py` — generator obu dokumentów.
- `assets/zrodla/` — źródłowe grafiki, wyłącznie techniczne; **nie drukować osobno**.

## Świat IV — obsługa Chronoskopu

W gabinecie stoi **Chronoskop Zegarmistrza** z jednym osłoniętym silnikiem zasilanym z USB 5 V. Zasilacz USB 5 V podłącz do gniazdka. Silnik uruchamia dorosły, **wkładając wtyk USB przewodu maszyny do zasilacza**. Zatrzymuje go przez **wyjęcie wtyku USB z zasilacza**. Przed dotknięciem lub wymianą tarczy należy poczekać na całkowite zatrzymanie osi.

Do próby mocujemy taśmą jedną z czterech tarcz o średnicy 10 cm. Na odwrocie każdej jest symbol: KSIĘŻYC = 7, KRUK = 2, KLUCZ = 9, KLEPSYDRA = 4. Dziewczynki odczytują cyfry stroboskopem, a potem ustalają kolejność symboli z zagadki. **Kolejność wymiany tarcz nie jest kolejnością kodu**. Kod świata IV: 7294.

Wszystkie cztery wzory tarcz w wydruku są odbite lustrzanie dla ustalonego kierunku obrotów silnika. W pakiecie jest wariant 2B. Przed grą sprawdź czytelność każdej cyfry. Stroboskop wyświetla częstotliwość **błysków na minutę**; przykładowo 3000 1/min = 50 błysków na sekundę. Szczegółowa instrukcja z Twoim zrzutem ekranu i dwoma rysunkami maszyny jest wewnątrz głównego PDF-u do druku.

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
