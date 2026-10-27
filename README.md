# Klątwa Siedmiu Światów — etap 1

Lokalna gra dla dwóch tabletów Android i laptopa Ubuntu. Ten etap zawiera: tworzenie postaci, wybór rasy i awatara, naprzemienne czytanie sześciu fragmentów historii, wspólną przysięgę i zsynchronizowany zegar 120 minut. **Zagadki siedmiu światów będą dodawane w kolejnych etapach.**

## Pierwsze uruchomienie (Ubuntu)

W terminalu:

```bash
sudo apt update
sudo apt install -y git python3
git clone https://github.com/thewitcher/haloween.git
cd haloween
python3 server.py
```

Sprawdź adres laptopa: `hostname -I`. Na dwóch tabletach podłączonych do tej samej sieci Wi-Fi otwórz `http://ADRES_LAPTOPA:8000` (np. `http://192.168.1.100:8000`). Tablet 1 wybiera Strażniczkę I, tablet 2 Strażniczkę II.

## Aktualizowanie gry

Zatrzymaj serwer przez Ctrl+C, a potem:

```bash
cd haloween
git pull
python3 server.py
```

## Reset testu

Zatrzymaj grę, następnie w drugim terminalu (gdy serwer jest uruchomiony) wpisz `python3 reset.py`. Możesz też zatrzymać serwer i usunąć lokalny plik `stan_wprowadzenia.json`.

## Bezpieczeństwo

Repozytorium jest publiczne. Nie umieszczaj tutaj danych dzieci ani sekretów. Domyślne hasło resetu jest tylko do lokalnych testów; przed właściwą grą ustaw własne, np. `SWIATY_HASLO='silne-losowe-haslo' python3 server.py`. Nie udostępniaj portu 8000 do Internetu. Gra nie jest jeszcze zabezpieczona przed podszywaniem się pod drugą rolę — służy do testów w zaufanej sieci domowej.
