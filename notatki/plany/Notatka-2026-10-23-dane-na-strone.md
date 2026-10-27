# Notatka projektowa: jak dane z Golda trafią na stronę (23.10.2026)

*Notatka przed kodem (zasada 10). **Zatwierdzona przez Gracjana 23.10 ze wszystkimi rekomendacjami
D1–D6 (wariant a).** Numery linii i komendy pojawią się dopiero w krokach.*

## Sedno w trzech zdaniach

1. Szkic strony ma dziś ceny i daty wpisane na sztywno w kodzie strony, a część z nich (od 18.09)
   przepisana z wcześniejszego szkicu, nie z drogi danych.
2. Nowy skrypt w Pythonie (piszesz go Ty) pobiera z S3 dwa pliki Golda, sprawdza je i zapisuje jeden
   plik `dane.js` z datami, cenami i rankingiem; strona (piszę ją ja) tylko ten plik czyta i rysuje.
3. Pierwszy etap działa na laptopie: uruchamiasz skrypt ręcznie i otwierasz stronę z dysku;
   publikacja w internecie (GitHub Pages) to osobny, późniejszy etap z własną notatką.

## Przykład na innych danych: pogoda

**Wejście 1** — pomiary w długiej tabeli (jak `dane_dzienne.csv`: data z godziną, liczba z szumem
w końcówce, nazwa z dopiskiem):

| data | temp | miasto |
|---|---|---|
| 2026-10-20 12:00:00 | 11.300000190734863 | KRK.PL |
| 2026-10-21 12:00:00 | 9.899999618530273 | KRK.PL |
| 2026-10-22 12:00:00 | 12.100000381469727 | KRK.PL |
| 2026-10-20 12:00:00 | 10.199999809265137 | GDA.PL |
| 2026-10-21 12:00:00 | 8.699999809265137 | GDA.PL |
| 2026-10-22 12:00:00 | 9.300000190734863 | GDA.PL |

**Wejście 2** — podsumowanie (jak `ranking.csv`):

| miasto | najcieplejszy | zmiana_okres |
|---|---|---|
| KRK.PL | 2026-10-22 | 7.079642 |
| GDA.PL | 2026-10-20 | -8.823531 |

**Wyjście** — plik `dane.js` (uruchomione 23.10, wynik skopiowany):

```
window.DANE = {"daty": ["2026-10-20", "2026-10-21", "2026-10-22"], "temp": {"GDA": [10.2, 8.7, 9.3], "KRK": [11.3, 9.9, 12.1]}, "podsumowanie": [{"miasto": "KRK", "najcieplejszy": "2026-10-22", "zmiana_okres": 7.08}, {"miasto": "GDA", "najcieplejszy": "2026-10-20", "zmiana_okres": -8.82}]};
```

i linia na ekranie: `Pogoda: 3 dni (2026-10-20 – 2026-10-22), miasta: GDA, KRK`.

Co się stało po drodze: data bez godziny, nazwa bez dopisku `.PL`, tabela „obrócona” tak, że każde
miasto ma jedną listę liczb ułożoną według dat, liczby zaokrąglone, przed zapisem sprawdzenie, że
każde miasto ma pomiar z każdego dnia (inaczej skrypt przerywa pracę z komunikatem).

| Przykład | Projekt |
|---|---|
| `pomiary` (długa tabela) | `gold/dane_dzienne/dane_dzienne.csv` z S3 |
| `podsumowanie` | `gold/ranking/ranking.csv` z S3 |
| `KRK.PL` → `KRK` | `CBF.WA` → `CBF` |
| `2026-10-20 12:00:00` → `2026-10-20` | `2026-10-22 17:00:00` → `2026-10-22` |
| zaokrąglenie do 1 miejsca | zaokrąglenie cen do 2 miejsc (grosze), zmian do 2 miejsc |
| `temp` — lista na miasto | `ceny` — lista na spółkę, ułożona według `daty` |
| `najcieplejszy`, `zmiana_okres` | `miesiac` (najbardziej zmienny pełny miesiąc), `zmiana_caly_okres` |
| linia `Pogoda: 3 dni …` | linia `Strona: N sesji (od … do …), ostatnie ceny …, ranking …` |

## Co strona bierze z pliku, a co zostaje w kodzie strony

| Z `dane.js` (Twój skrypt) | W kodzie strony (ja) |
|---|---|
| daty sesji od 14.08.2023 | wygląd, zakładki, animacje |
| ceny zamknięcia trzech spółek | nazwy i kolory spółek |
| z rankingu Golda: najbardziej zmienny miesiąc i zmiana za cały okres | kalendarz wydarzeń (ręcznie, z raportów ESPI) |
| data i godzina wygenerowania pliku | słownik pojęć |
| | rzeczy liczone z cen w przeglądarce: zmiana dzienna, statystyki wybranego okresu (w tym „Najwyższa” i „Najniższa”), mapa miesięcy, średnia 20 sesji, „od Twojej ostatniej wizyty”, siatka 3D od 18.03.2026 |

Statystyki okresu muszą zostać w przeglądarce, bo zależą od zakresu wybranego suwakiem. Ranking strona
bierze z Golda, a nie liczy sama, żeby pokazywała dokładnie te liczby, które sprawdza kontrola.

## Co może pójść źle i co wtedy

- **S3 nie odpowiada albo brak uprawnień** — skrypt kończy się błędem, stary `dane.js` zostaje nietknięty.
- **Uruchomienie w trakcie biegu (18:00–18:15)** — Gold może wysyłać pliki właśnie wtedy; skrypt
  sprawdza spójność, a zasada brzmi: nie uruchamiać przed 18:15.
- **Plik niepełny** (brak spółki, spółki z różną liczbą dni, pusta cena, daty nie rosną, data
  z przyszłości) — skrypt przerywa pracę z komunikatem przed zapisem, jak `silver.py` w liniach 20–22.
- **Mniej sesji niż w poprzednim `dane.js`** — skrypt przerywa pracę (ochrona przed „pół tabeli”).
- **Skrypt uruchomiony dwa razy** — ten sam wynik, nic się nie psuje.
- **Uruchomienie przed biegiem** — strona pokaże wczorajszą sesję; data ostatniej sesji jest na
  stronie, więc widać to od razu.
- **Czwarta spółka** — skrypt porówna spółki z listą `ticker` z `config.py` i przerwie pracę; nowa
  spółka to świadoma zmiana w `config.py` i na stronie (nazwa, kolor).
- **Brak pliku `dane.js`** — strona pokazuje komunikat „Brak danych” zamiast pustych wykresów.
- **Nagłówek `ranking.csv` ma stare nazwy** (`pierwsza_cena`, `ostatnia_cena`) — skrypt czyta tylko
  `spolka`, `miesiac`, `zmiana_caly_okres`, które się nie zmieniły.

## Jak sprawdzimy (liczby przed biegiem)

Przed pierwszym uruchomieniem zapisujemy z kontroli tego samego dnia: `Kontrola: Dane M wierszy` →
sesji M / 3; pierwsza data 2023-08-14; ostatnia data = dzisiejsza sesja; ostatnie ceny = archiwum GPW;
ranking = linie rankingu z bloku Golda w `errors.txt`. Po biegu skrypt wypisuje te same liczby w jednej
linii, a strona otwarta z dysku pokazuje je w kartach i w rankingu. Przykład na dziś (23.10, jeśli bieg
będzie zgodny z tabelą przewidywań): 2400 wierszy → 800 sesji, od 2023-08-14 do 2026-10-23.

## Co to zmieni za miesiąc i dalej

- Plik rośnie o ok. 3 ceny i 1 datę na dzień giełdowy; przy 800 sesjach ma ok. 30 KB.
- 01.11 Gold przeliczy pełne miesiące (117/111 się zmieni) — ranking na stronie zmieni się sam.
- Kompakcja nie dotyczy `gold/`, więc skryptu nie rusza.
- 19.02.2027 (koniec darmowego AWS): skrypt nie pobierze plików i zakończy się błędem; strona zostanie
  z ostatnimi danymi.

## Decyzje do podjęcia (rekomendacja pierwsza)

- **D1. Jak strona dostaje dane:** (a) skrypt pisze `dane.js` obok `index.html` — działa z pliku
  otwartego wprost i na GitHub Pages, kod strony i dane osobno · (b) skrypt wkleja dane do HTML —
  jeden plik, ale Python musi znać kod strony i każda poprawka wyglądu idzie przez skrypt ·
  (c) `dane.json` czytany przez stronę — przeglądarka blokuje to przy pliku otwartym z dysku.
- **D2. Skąd skrypt bierze dane:** (a) dwa pliki CSV z S3 przez `boto3` (`download_file`, para do
  znanego `upload_file`) — te same pliki, które czyta Athena, bez kosztu zapytań · (b) Athena przez
  `pyathena`, jak `wykresy.py` — zapytania płatne i wyniki w `athena-results/` · (c) pliki `gold/`
  na EC2 — wymagałoby wysyłania strony z EC2.
- **D3. Czy `dane.js` w gicie:** (a) nie, w `.gitignore`, jak `silver/` i `gold/` — plik generowany ·
  (b) tak.
- **D4. Liczby w zakładce Projekt:** (a) liczba sesji i data ostatniej sesji z `dane.js`, reszta na
  stałe z 22.10 — inaczej od jutra „Ostatni bieg: 22.10” będzie nieprawdą · (b) wszystko na stałe
  (decyzja 22.10 bez zmian).
- **D5. Gdzie pliki:** (a) skrypt `kod/strona_dane.py`, strona `strona/index.html` i `strona/dane.js`
  · (b) folder `docs/` zamiast `strona/` (GitHub Pages umie publikować `docs/` bez dodatkowej
  konfiguracji, ale to decyzja drugiego etapu).
- **D6. Kiedy przegląd całości (zasada 16, po naprawach 1 i 2 jeszcze go nie było):** (a) przed
  kodem tego skryptu · (b) po pierwszym etapie strony.

## Kolejność pracy po zatwierdzeniu

1. Notatka-instrukcja dla Ciebie (zasada 3): nowe pojęcia (`download_file`, `pivot`, `json.dumps`,
   `strftime`), przykład uruchomiony, pułapki, kolejność.
2. Piszesz `kod/strona_dane.py` i testy funkcji, które obracają tabelę i sprawdzają dane (na
   zmyślonych danych, bez S3).
3. Ja przerabiam szkic na `strona/index.html`, który czyta `dane.js` zamiast danych na sztywno.
4. Pierwsze uruchomienie po 18:15 w dniu z kontrolą: liczby przed, liczby po, porównanie ze stroną.

**Zrobione (zasada 9) dla pierwszego etapu znaczy:** skrypt działa na prawdziwych plikach z S3,
liczby zgadzają się z kontrolą i archiwum GPW, błędne dane kończą się komunikatem, a strona
otwarta z laptopa pokazuje te same liczby. Internet, odświeżanie codzienne i warunki Yahoo dla
publicznej strony (niesprawdzone) — drugi etap.

## Dopisek 27.10: pierwszy etap zamknięty

- **„Daty nie rosną”** (lista „Plik niepełny” wyżej) — **nie dodajemy** (decyzja Gracjana 27.10). Ten
  przypadek pokrywają `sort_values(["spolka", "dzien"])` w linii 73 `kod/data_stream.py` i `pivot` w
  `zbuduj_dane` (linia 37). Sprawdzone 27.10 na prawdziwym pliku Golda z 26.10 przetasowanym losowo:
  daty w wyniku rosnąco (`2023-08-14` … `2026-10-26`); bez sortowania `sprawdz_pliki` zgłasza 3
  problemy (np. `CBF.WA: ostatnia cena: 111.5, w rankingu: 194.8`), po sortowaniu `[]`. Dodatkowe
  sprawdzenie nigdy by nie zadziałało (martwy kod, jak `assert` w `silver.py`, linie 21–22).
- **Błędne dane kończą się komunikatem — sprawdzone na prawdziwym biegu 27.10:** podstawiony poprzedni
  `dane.js` z 900 udawanymi sesjami → `Strona: problem - Mniej sesji niż poprzednio: 802 < 900`, kod 1,
  plik nienadpisany, pliki z S3 pobrane (161161 i 336 B); po przywróceniu `802 sesji, poprzednio 801`.
- Do tego 5 testów zapisu i odczytu `dane.js` (`tmp_path`), `pytest kod/ -v` → `53 passed`.
- **Pierwszy etap zamknięty 27.10** — wszystkie warunki z akapitu „Zrobione” wyżej. Następny krok:
  przegląd całości (D6 b).
