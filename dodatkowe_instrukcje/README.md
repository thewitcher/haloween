# Dodatkowe instrukcje i etykiety — Klątwa Siedmiu Światów

W tej części repozytorium znajdują się osobne, uzupełniające materiały. Nie zastępują dwóch głównych PDF-ów w katalogu głównym.

## Cztery pliki do wydruku

1. `Mapa_Siedmiu_Swiatow.pdf` — mapa trasy między siedmioma komnatami. **Uwaga: mapa przedstawia układ prywatnego domu, a to repozytorium jest publiczne.** Zalecamy przechowywać ją wyłącznie lokalnie, nie w repozytorium.
2. `Etykiety_Chronoskop_i_Skrzynia.pdf` — małe naklejki z grubą linią cięcia: „CHRONOSKOP” i „SKRZYNIA MORTHARA” (po dwie).
3. `Instrukcja_Stroboskopu.pdf` — opis interfejsu i częstotliwości: 3000 1/min = 50 błysków na sekundę; + zwiększa, − zmniejsza, ×2 podwaja, ÷2 dzieli przez dwa.
4. `Instrukcja_Chronoskopu.pdf` — obsługa jednego silnika DC 5 V, montaż i wymiana tarcz oraz dwa ilustracyjne rysunki maszyny.

## Jak dodać PDF-y do GitHuba

Pobierz ZIP z czterema dokumentami z rozmowy. Następnie na Ubuntu:

```bash
cd ~/haloween
git pull
bash tools/wgraj_dodatkowe_pdf.sh ~/Pobrane/Dodatkowe_instrukcje_Siedem_Swiatow.zip
```

Polecenie domyślnie przesyła trzy pliki, **bez mapy domu**. Jeśli świadomie chcesz opublikować również plan pomieszczeń w publicznym repozytorium, dodaj `--z-mapa`; skrypt poprosi o dodatkowe potwierdzenie.

## Zasady bezpiecznego używania

- Przed każdą wymianą tarczy odłącz zasilanie 5 V i poczekaj na pełne zatrzymanie silnika.
- Tarcze powinny być wyważone i osłonięte.
- Nie kieruj stroboskopu w oczy; zrezygnuj z błysków przy nadwrażliwości na światło.
- Wskazanie stroboskopu to liczba błysków na minutę, nie pewny pomiar obrotów silnika.
- Dzieci nie obsługują przewodów, zasilania ani zmiany wirujących tarcz.

Dokumenty drukuj na A4 w skali 100%.
