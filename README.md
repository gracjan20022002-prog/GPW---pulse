# GPW Pulse

Projekt nauki data engineeringu — pobieranie i przetwarzanie danych giełdowych
(GPW) dla wybranych spółek.

**Etap BRONZE (surowe dane):** ukończony. Program pobiera dzienne notowania
trzech spółek GPW (CBF, XTB, SNT) z Yahoo Finance (okno 3 lat od API), doklejane
do istniejącej historii w pliku zamiast ją nadpisywać — dzięki temu ruchome
okno 3 lat nie kasuje starszych dat przy kolejnych odświeżeniach. Program sam
sprawdza, czy zapisane dane są poprawne.

**Etap SILVER (czyszczenie danych, `pandas`):** ukończony. Trzy osobne pliki
spółek są wczytywane, naprawiane (typy danych), sprawdzane pod kątem braków
i duplikatów, łączone w jedną tabelę, sortowane i zapisywane jako jeden
czysty plik: `silver/clean_data.csv`.

**Etap GOLD (liczenie wskaźników, `pandas`):** ukończony. Z czystej tabeli
liczona jest dzienna zmiana procentowa ceny (osobno dla każdej spółki),
całkowita zmiana procentowa za cały okres i miesiąc z największymi wahaniami
cen. Wynik to dwa pliki: `gold/dane_dzienne.csv` (pełne dane dzienne ze
wskaźnikami) i `gold/ranking.csv` (podsumowanie — jeden wiersz na spółkę).

**Etap 4 (pokazanie wyniku):** w toku. Część A (wykresy w Pythonie,
`matplotlib`) ukończona — patrz `wykresy/` niżej. Część B (dashboard
w Power BI — wykres liniowy, wykres słupkowy, filtr) zbudowana, plik
`wykresy/PowerBi_do_dopracowania.pbix`; stylizacja i eksport/publikacja
odłożone na później. Część C (automatyzacja) ukończona: `kod/pipeline.bat` łączy cały łańcuch
(`Data ingestion 2.py` → `silver 1.py` → `gold 1.py`) w jedno zadanie
Harmonogramu Windows (codziennie o 10:25, z opcją dogonienia pominiętego
uruchomienia). Naprawiony błąd utraty historii sprzed 3 lat (skrypt scala
świeże dane z istniejącym plikiem zamiast go nadpisywać) — patrz opis
Bronze wyżej. Zostaje lokalnie, jako działające zabezpieczenie, dopóki
Etap 5 (niżej) nie przejmie go w pełni.
Dalej: Część D — rozbudowa projektu pod portfolio.
Plan: [`notatki/plany/Plan-04-pokazanie-wyniku.md`](notatki/plany/Plan-04-pokazanie-wyniku.md).

**Etap 5 (migracja do AWS):** w toku. Docelowa architektura: EC2 (Kafka
z KRaft) → S3 → Glue → Athena. Zrobione: broker Kafki na EC2 — od 25.08
pod stałym adresem (Elastic IP), koniec z ręczną aktualizacją adresu po
każdym Stop/Start. Producent wysyłający nowe ceny przez Kafkę
(`kod/Data ingestion 2.py`, od 31.08 odporny na brak brokera — brak
połączenia z Kafką jest łapany i logowany, nie przerywa już pobierania
i zapisu lokalnego), Konsument (`kod/kafka_consumer.py`) zapisujący bieżące
dane do S3 z podziałem na spółki (partycje `spolka=TICKER`). Historia cen
wgrana do S3 raz (`bronze/`, przeorganizowana 24.08 pod te same partycje)
— automatyczny codzienny upload do `bronze/` wyłączony, żeby nie dublował
tego, co już niesie Kafka. Glue Crawler + Athena działają na obu tabelach
(`bronze` i `live`). **Część E:** od 31.08 `silver 1.py` czyta dane
z Athena przez `pyathena` (zapytanie SQL łączące `bronze` i `live`) zamiast
lokalnych plików spółek — przetestowane osobno i przez cały `pipeline.bat`.
Zostaje jeszcze podłączenie Power BI, odłożone na osobną sesję. Dalej:
**Część F** — broker jako usługa `systemd`, Producent i Konsument
przeniesione na EC2 i uruchamiane przez `cron`, niezależnie od komputera
Gracjana; szczegółowa rozpiska w planie niżej.
Plan: [`notatki/plany/Plan-05-aws-migracja.md`](notatki/plany/Plan-05-aws-migracja.md).

---

## Struktura folderu

| Folder | Co w nim jest |
|---|---|
| **kod/** | skrypty Pythona projektu (patrz tabela niżej) |
| **companies/** | pobrane dane spółek (pliki `.txt`, jeden na spółkę) + `errors.log` |
| **silver/** | wynik etapu Silver — jedna czysta tabela ze wszystkich spółek (`clean_data.csv`) |
| **gold/** | wynik etapu Gold — dzienne dane ze wskaźnikami (`dane_dzienne.csv`) i ranking spółek (`ranking.csv`) |
| **wykresy/** | wykresy z Etapu 4, Część A (Python/`matplotlib`) — pliki `.png`; Część B — dashboard Power BI (`PowerBi_do_dopracowania.pbix`) |
| **notatki/** | notatki do nauki i projektu (patrz niżej) |
| **aws/** | klucz SSH do EC2 i notatki połączenia — poza gitem (`.gitignore`), zawiera dane dostępowe |
| **CLAUDE.md** | zasady pracy z asystentem nad tym projektem |

### Skrypty w `kod/`

| Plik | Co robi |
|---|---|
| `Data ingestion 2.py` | Główny skrypt — pobiera dane trzech spółek z Yahoo Finance (`requests`), scala je ze starą historią w pliku (żeby ruchome okno 3y nie kasowało starszych dat), pomija ceny, których Yahoo nie zwróciło (`null` — dzień jeszcze nierozliczony, zdarza się wszystkim spółkom naraz), zamiast zapisywać je jako błędny tekst, zapisuje do `companies/{TICKER}.txt`, błędy loguje do `companies/errors.log` (`try/except` + `logging`). Etap 5: wysyła nowe ceny przez Kafkę (`kafka-python`) na topic `gpw_tracker`. Jednorazowy upload historii do S3 (`boto3`) zrobiony 20.08, kod od 24.08 zakomentowany — `bronze/` w S3 zostaje zamrożoną historią, nie odświeżaną co dzień |
| `kafka_consumer.py` | Etap 5, Część C — Konsument Kafki: odbiera nowe ceny z topicu `gpw_tracker`, grupuje po spółce, zapisuje do S3 partiami (`s3.put_object`, format JSON Lines) pod ścieżką partycjonowaną `live/spolka={TICKER}/...` |
| `test_plikow.py` | Sprawdza pobrane pliki: czy istnieją, czy mają poprawny format wiersza, czy jest wystarczająco dużo danych, czy dane da się odczytać jako data i liczba |
| `Data ingestion.py` | Wczesna eksploracja odpowiedzi API Yahoo Finance (Sesja 3) — materiał referencyjny, nieużywany przez resztę programu |
| `silver 1.py` | Etap Silver — od 31.08 (Etap 5, Część E) czyta dane z Athena przez `pyathena` (zapytanie SQL łączące tabele `bronze` i `live`) zamiast lokalnych plików spółek, naprawia typy (`to_datetime`, `to_numeric`), sprawdza braki i duplikaty, sortuje po spółce i dacie, zapisuje do `silver/clean_data.csv` |
| `gold 1.py` | Etap Gold — wczytuje `silver/clean_data.csv`, liczy dzienną zmianę procentową (`groupby`+`pct_change`), całkowitą zmianę i najbardziej zmienny miesiąc na spółkę (`groupby`+`std`), łączy w tabelę rankingu (`merge`), zapisuje `gold/dane_dzienne.csv` i `gold/ranking.csv` |
| `wykresy.py` | Etap 4, Część A — wczytuje `gold/dane_dzienne.csv`, rysuje cenę wszystkich trzech spółek w czasie (`matplotlib`, `plt.plot` w pętli po spółkach, legenda), zapisuje `wykresy/wykres3spolek.png` |
| `ranking.py` | Etap 4, Część A — wczytuje `gold/ranking.csv`, rysuje wykres słupkowy całkowitej zmiany procentowej spółek (oś Y sformatowana jako „%"), zapisuje `wykresy/ranking.png` |
| `pipeline.py` | Etap 4, Część C — testowy skrypt do sprawdzenia Harmonogramu zadań Windows: dopisuje datę/godzinę uruchomienia do `kod/pipeline.txt` |
| `pipeline.bat` | Etap 4, Część C — łączy trzy kroki (`Data ingestion 2.py`, `silver 1.py`, `gold 1.py`) w jedno zadanie Harmonogramu; trzy niezależne linie bez `&&` (łączenie przez `&&`/`^` powodowało, że `silver 1.py` cicho nie zapisywał danych mimo że `gold 1.py` i tak się uruchamiał — porzucone na rzecz pewności działania) |

### Dane w `companies/`

Jeden plik `.txt` na spółkę, jeden wiersz na dzień notowania:
```
2023-07-24 09:00:00, 12.34
```
`errors.log` zbiera błędy pobierania (np. nieistniejący ticker) — nie trafia
na GitHub (patrz `.gitignore`).

### Dane w `silver/`

Jedna tabela, wszystkie trzy spółki razem, z nagłówkiem:
```
data,cena,spolka
2023-07-24 09:00:00,78.800003,CBF.WA
```

### Dane w `gold/`

Dwa pliki, wynik etapu Gold.

`dane_dzienne.csv` — pełna tabela dzienna (2268 wierszy), ta sama co
w `silver/`, plus dzienna zmiana procentowa i miesiąc (pierwszy dzień każdej
spółki ma pusty `zmiana_proc` — nie ma dnia wcześniej, z czym porównać):
```
data,cena,spolka,zmiana_proc,max_zmienny_miesiac
2023-07-24 09:00:00,78.800003,CBF.WA,,2023-07
```

`ranking.csv` — podsumowanie, jeden wiersz na spółkę: pierwsza i ostatnia
cena, zmiana za cały okres, najbardziej zmienny miesiąc i jego odchylenie
standardowe:
```
spolka,max_zmienny_miesiac,zmiana_proc,pierwsza_cena,ostatnia_cena,zmiana_caly_okres
SNT.WA,2025-06,4.086839,70.800003,360.0,408.474554
```

### Wyniki w `wykresy/`

Dwa wykresy z Części A Etapu 4, wygenerowane przez `kod/wykresy.py` i
`kod/ranking.py`:

- `wykres3spolek.png` — cena wszystkich trzech spółek w czasie, jedna linia
  na spółkę, z legendą.
- `ranking.png` — wykres słupkowy: całkowita zmiana procentowa każdej
  spółki za cały okres (24.07.2023–24.07.2026).

---

## Notatki (`notatki/`)

| Folder/plik | Co w nim jest |
|---|---|
| **plany/** | plany projektu i codzienna rutyna |
| **lekcje/** | notatki z tego, czego się uczysz |
| **dziennik/** | co zrobiłeś każdego dnia, jeden plik na sesję — **prywatny, nie trafia na GitHub** (patrz `.gitignore`) |
| **Slownik.md** | trudne słowa wyjaśnione po ludzku |
| **Zrodla.md** | linki, materiały, dokumentacja |

### Jak to otworzyć w Obsidianie

1. Otwórz Obsidian
2. Ikona sejfu w lewym dolnym rogu → **Open another vault** → **Open folder as vault**
3. Wskaż folder: `GPW - pulse` → `notatki`
4. Gotowe

---

## Od czego zacząć

1. [[Plan-ogolny]] — zobacz całość projektu
2. [[Codzienna-rutyna]] — przejdź część A, jednorazową
3. [[Plan-04-pokazanie-wyniku]] — Etap 4, aktualnie w toku
4. [[Plan-05-aws-migracja]] — Etap 5, aktualnie w toku
5. [[Slownik]] — zaglądaj, gdy spotkasz nieznane słowo

---

## Zasady prowadzenia notatek

**Dziennik uzupełniasz sam, po każdej sesji.**
Claude może pomóc, ale najważniejsza jest rubryka
„czego się nauczyłem" — pisana **Twoimi słowami**.

Jeśli nie potrafisz czegoś zapisać własnymi słowami — to znaczy,
że jeszcze tego nie rozumiesz. To dobry sprawdzian.

**Nowy plik w dzienniku dla każdej sesji.** Nazwa: data, np. `2026-07-22.md`.

**Podwójne kwadratowe nawiasy tworzą link** między notatkami.
Napisz `[[Slownik]]`, a Obsidian sam zrobi odnośnik.

**Nie znasz słowa? Dopisz je do [[Slownik]]** od razu, gdy je spotkasz.

---

## Powiązane notatki

- [[Plan-ogolny]]
- [[Plan-01-bronze]]
- [[Plan-02-silver]]
- [[Plan-03-gold]]
- [[Plan-04-pokazanie-wyniku]]
- [[Plan-05-aws-migracja]]
- [[Codzienna-rutyna]]
- [[Stare-repo-co-to-bylo]]
- [[Slownik]]
- [[Zrodla]]
