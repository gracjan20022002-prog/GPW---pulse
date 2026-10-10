# Notatka projektowa 09.10: strażnik kompakcji przepuszcza wszystko przy błędzie S3

**Status:** **zatwierdzona 09.10 w całości — wszystkie pięć decyzji w wariancie (a).** Instrukcja przed
kodem: `Notatka-2026-10-09-jak-poprawic-straznika.md`. Skąd: przegląd z 08.10
(`Przeglad-2026-10-08-calosc.md`, punkt 1.2), decyzja 3 z 08.10 w wariancie (a): „tylko »nie ma
takiego pliku« znaczy nową spółkę, każdy inny błąd S3 przerywa bieg przed zapisem”.

## Sedno

1. Kompakcja (`kod/compaction.py`, raz w miesiącu z laptopa) przed nadpisaniem `bronze` pobiera
   z S3 jego starą wersję, liczy wiersze, a strażnik nie pozwala zapisać mniej, niż było.
2. Dziś **każdy** błąd S3 przy tym pobraniu jest brany za „nowa spółka”: stara liczba = 0, więc
   strażnik przepuszcza wszystko — także pół tabeli z Atheny, przed którym miał chronić.
3. Zmiana: zero tylko wtedy, gdy S3 odpowie „nie ma takiego pliku” (kod `404`); każda inna odpowiedź
   zatrzymuje skrypt, zanim cokolwiek zapisze albo skasuje.

## Przykład na innych danych: stan budek z lodami

Trzy budki. `stan_wczoraj(budka)` udaje pobranie z chmury pliku ze wczorajszym stanem:
Kraków ma plik (120 lodów), Gdańsk to nowa budka (pliku nie ma, chmura odpowiada kodem `404`),
w Poznaniu chmura odmawia dostępu (kod `403`).

Dziś:

```python
try:
    stan = stan_wczoraj(budka)
except ClientError:
    stan = 0
```

Po zmianie:

```python
try:
    stan = stan_wczoraj(budka)
except ClientError as e:
    kod = e.response["Error"]["Code"]
    if kod == "404":
        stan = 0
    else:
        raise
```

| Budka | Co odpowiada chmura | Dziś | Po zmianie |
|---|---|---|---|
| Kraków | plik, 120 lodów | `Kraków 120` | `Kraków 120` |
| Gdańsk | `404` — nie ma pliku | `Gdańsk 0` | `Gdańsk 0` |
| Poznań | `403` — brak dostępu | `Poznań 0` ← nieprawda, wcale nie zero | `Traceback`, ostatnia linia: `botocore.exceptions.ClientError: An error occurred (403) when calling the HeadObject operation: Forbidden`; pętla się kończy |

Oba warianty uruchomione 09.10 na laptopie, z udawanymi błędami (bez łączenia z AWS) — wyniki
w tabeli są z tego biegu.

Nowe słowa (pełne wyjaśnienie z przykładami przyjdzie w instrukcji przed kodem):
- `ClientError` — wyjątek z biblioteki `botocore`: S3 odpowiedziało, ale odmówiło; w środku jest kod;
- `except ClientError as e` — `e` to złapany wyjątek (to samo `as e` jest w `control.py`, linia 48);
- `e.response["Error"]["Code"]` — kod odpowiedzi jako **napis**: `"404"`, `"403"`;
- `raise` bez niczego, wewnątrz `except` — „puść ten sam błąd dalej”, czyli skrypt staje tak,
  jakby `try` w ogóle nie było.

## Przykład → projekt

| Przykład | Projekt |
|---|---|
| budka | spółka z `ticker` (`config.py`) |
| `stan_wczoraj(budka)` | `s3.download_file(...)` i `len(pd.read_parquet(kopia))`, linie 29–30 |
| Kraków, 120 | plik jest — po 03.10: 783 wiersze na spółkę |
| Gdańsk, `404` | czwarta spółka, której pliku w `bronze/` jeszcze nie ma |
| Poznań, `403` | brak uprawnień, zły klucz; podobnie `503` (S3 przeciążone, po ponownych próbach biblioteki) |
| `stan = 0` | `poprzedni[t] = 0`, linia 32 |
| `raise` → koniec | skrypt staje przed strażnikiem (linia 37): nic nie zapisane do `bronze`, nic nie skasowane z `live/` |

## Sprostowanie do przeglądu z 08.10

Przegląd zaliczył „przerwę w sieci” do błędów łapanych w linii 31. Sprawdzone 09.10 w bibliotece na
laptopie (`botocore` 1.43.75): błędy sieci (`EndpointConnectionError`, `ConnectTimeoutError`,
`ReadTimeoutError`) i brak kluczy (`NoCredentialsError`) **nie są** `ClientError`, więc już dziś
zatrzymują skrypt. Linia 31 łapie tylko odpowiedzi S3 z kodem błędu. Wada zostaje, węższa.

## Co może pójść źle

- S3 odpowie `403` zamiast `404` na brak pliku (tak robi, gdy użytkownik nie ma prawa listowania
  bucketu) → nowa spółka zablokowana, głośno. Sprawdzimy jedną komendą przed kodem.
- Porównanie z liczbą `404` zamiast z napisem `"404"` → nigdy równe, każdy brak pliku zatrzyma
  skrypt. Głośno; wyłapie to sprawdzenie na nieistniejącym pliku.
- Plik `bronze` skasowany przez pomyłkę wygląda jak nowa spółka → strażnik porówna z zerem. Zmiana
  tego nie łapie (decyzja 3).
- Athena zwraca pół tabeli → to łapie strażnik; po zmianie kopia albo się pobrała, albo skrypt stoi.
- Skrypt odpalony dwa razy → jak dziś: drugi bieg ma `stara = nowa`, kasuje 0 plików, ale nadpisuje
  kopię w `bronze/poprzedni/` stanem już po kompakcji (decyzja 4).
- Zła godzina (17:55–18:35, w trakcie biegów `cron`) → zmiana nic tu nie zmienia, zasada zostaje.
- Czwarta spółka → `404` → 0 → przechodzi, jak dziś (zamierzone); warunek „przed dodaniem spółki”
  (partycja w Athenie, okno `range=3y`) dalej obowiązuje.
- Za miesiąc → pierwsza kompakcja na nowym kodzie na początku listopada; jeśli S3 czymś odpowie,
  skrypt stanie, `bronze` i `live/` zostaną nietknięte, wystarczy powtórzyć po usunięciu przyczyny.

## Jak sprawdzimy

1. **Przed kodem** — komenda `python -c` na laptopie (Gracjan): pobranie nieistniejącego pliku
   z naszego bucketu → przewidywane `404`; to samo ze zmyślonymi kluczami → przewidywane `403`.
   Potwierdza, że warunek patrzy na właściwy kod.
2. **Po kodzie, ścieżka błędu na prawdziwym skrypcie** (przy decyzji 2a): `compaction.py` ze
   zmyślonymi kluczami → `Traceback` z `(403) … HeadObject`, przed zapytaniem do Atheny; `bronze/`
   i `live/` w S3 bez zmian (odczyt `aws s3 ls` przed i po). Lokalna kopia zostaje — sprawdzone 09.10
   na udawanym S3: nieudane pobranie nie rusza starego pliku na dysku.
3. **Ścieżka zwykła — kompakcja w listopadzie.** Przewidywania liczone z Atheny przed biegiem
   (`stara ilosc` 783 na spółkę, `nowa_ilosc` 783 + sesje października, `Usunięto N plików`),
   potwierdzone po biegu. Laptop jest miejscem, gdzie kompakcja działa, więc tam warunek (d).

## Decyzje (rekomendacja pogrubiona)

1. Jak rozpoznać „nie ma pliku”: **(a) kod `"404"` w `except`** (wzór z dokumentacji `boto3`, kilka
   linii); (b) przed pętlą lista plików w `bronze/` (`list_objects_v2`), bez `try` — więcej nowego.
2. Kolejność w skrypcie: **(a) pobranie kopii (linie 25–32) przed zapytaniem do Atheny (linia 20)**
   — ścieżkę błędu da się wtedy pokazać na prawdziwym skrypcie zmyślonymi kluczami, bez ryzyka dla
   danych; (b) bez zmiany kolejności — ścieżka błędu udowodniona tylko komendą z punktu 1.
3. Skasowany plik `bronze` = „nowa spółka”: **(a) zostawić i opisać w README przy warunku „przed
   dodaniem spółki”**; (b) brak pliku też zatrzymuje, nową spółkę zgłasza się zmienną środowiskową.
4. Jedno pokolenie kopii w `bronze/poprzedni/`: **(a) zostawić** (inne ryzyko niż w tym punkcie);
   (b) osobny folder na każdy bieg, z datą i godziną w nazwie.
5. Termin: **(a) kod i sprawdzenia 1–2 w październiku**, prawdziwy bieg na początku listopada (nie
   między 17:55 a 18:35); (b) wszystko tuż przed listopadową kompakcją.
