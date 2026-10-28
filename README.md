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

## Dwa dokumenty w katalogu głównym — wersja obowiązująca

W katalogu głównym znajdują się **dwa dokumenty do używania przy grze**:

- **`Instrukcja_organizatora.pdf`** – 10 stron: przygotowanie domu, kryjówki, wyposażenie, odpowiedzi, zasilanie urządzeń, kontrola przed startem. **Tylko dla dorosłego — zawiera rozwiązania.**
- **`Materialy_do_druku.pdf`** – 27 stron: tylko fizyczne elementy potrzebne do rozstawienia i wręczenia: karty sześciu bestii, trzy lustrzane wiadomości, papierowa instrukcja budowania Enigmy i etykiety jej części, cztery tarcze i symbole, symbole sześciu książek, siedem pieczęci, etykiety kopert, list Morthara, kartka z zaklęciem i dwa dyplomy.

**Nie drukujemy osobno** planszy puzzli (korzystamy z prawdziwego zestawu 60 elementów) ani opowieści, poradników do mikroskopu, tabel barw rezystorów, dwóch przykładów liczenia oporności, dzienników notatek ani dodatkowych podpowiedzi. Te informacje są na odpowiednich tabletach. Wyjątek: obrazkowa instrukcja montażu Enigmy jest rekwizytem zadania, dlatego zostaje na papierze.

**Uwaga po aktualizacji generatora:** jeżeli `Materialy_do_druku.pdf` ma jeszcze **37 lub 28 stron**, jest starszą wersją. Uruchom generator poniżej albo podmień PDF na aktualną wersję **27-stronicową**. Nie korzystaj z obu wersji jednocześnie.

### Jak odtworzyć oba PDF-y na Ubuntu

Źródłem do generowania jest `tools/build_master.py`. Stare PDF-y w katalogach poszczególnych światów są **wejściowymi zasobami graficznymi generatora** — nie usuwaj ich, dopóki generator z nich korzysta, nawet jeśli nie trzeba ich osobno drukować.

```bash
cd ~/haloween
git pull
python3 -m venv .venv
source .venv/bin/activate
pip install reportlab pymupdf
HALLOWEEN_ASSET_DIR=. HALLOWEEN_OUT_DIR=. python3 tools/build_master.py
```

Powstaną/odświeżą się pliki `Instrukcja_organizatora.pdf` (10 stron) i `Materialy_do_druku.pdf` (**27 stron**) w katalogu głównym. Nie trzeba otwierać ani drukować pozostałych PDF-ów z podkatalogów.

Aby zapisać aktualne wersje także na GitHubie:

```bash
git add Instrukcja_organizatora.pdf Materialy_do_druku.pdf
git commit -m "Komplet dokumentów: instrukcja i rekwizyty"
git push
```

Wydruk: A4, rzeczywista skala **100%**, jednostronnie. Przygotuj **prawdziwe puzzle z dokładnie 60 elementów** (nie drukuj ani nie wycinaj papierowych). Ułóż całość, odwróć ją między dwiema sztywnymi tekturami i napisz na rewersie zagadkę o Kasprowym Wierchu atramentem UV. Po wyschnięciu wymieszaj elementy i rozłóż **po 10 prawdziwych puzzli** w kopertach I–VI. Karty z magicznym słowem i list Morthara włóż do skrzyni, nie pozostawiaj ich na widoku.

GitHub Actions może automatycznie regenerować dokumenty, ale jeśli workflow nie ma przydzielonego działającego runnera, należy wykonać polecenia lokalnie. **Najważniejsze są dwa pliki PDF w katalogu głównym**, nie pośrednie dokumenty ani stare wersje.

## Przebieg siedmiu światów

| Świat | Pokój | Mechanika |
| --- | --- | --- |
| I | Salon | Karty sześciu bestii i kod 7219. |
| II | Sypialnia | Lustrzane kartki i zdanie NOC MA OCZY. |
| III | Kuchnia | Arduino UNO, alfabet Morse’a, terminal i hasło BURZA. |
| IV | Gabinet | Cztery silniki, papierowe tarcze, stroboskop i kod 7294. |
| V | Pokój Emilki | Sześć ksiąg, rozumowanie, atrament UV, imię MORWENA. |
| VI | Pokój Zosi | Sześć kopert UV, mikroskop, rezystory i hasło PRĄDEM. |
| VII | Garderoba | 60 prawdziwych puzzli, Kasprowy Wierch, kłódka 1987, skrzynia i słowo WOLNOŚĆ. |

Każda z pierwszych sześciu kopert ze zdobywaną pieczęcią zawiera **dokładnie 10 kawałków puzzli**. W finale układanka złożona z 60 kawałków, po odwróceniu i oświetleniu UV, ujawnia wskazówkę do zamka.

## Bezpieczeństwo

Cała gra pracuje tylko w zaufanej sieci domowej, nie publikuj portu 8000 w Internecie. Dorośli sprawdzają elektronikę przy odłączonym zasilaniu. Silniki mają osłony; nie kierujemy migającego stroboskopu ani światła UV w oczy. Małe elementy nie są przeznaczone do wkładania do ust. Jeśli uczestniczka jest wrażliwa na błyski, zrezygnuj ze stroboskopu i przygotuj alternatywne ujawnienie cyfr.

Repozytorium jest publiczne. Nie zapisuj w nim danych wrażliwych ani haseł z domowych usług.
