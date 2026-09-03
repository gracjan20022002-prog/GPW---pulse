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
odłożone na później. Część C (automatyzacja) ukończona: `kod/pipeline.bat`
łączy Silver i Gold (`silver.py` → `gold.py`) w jedno zadanie Harmonogramu
Windows — pobieranie danych przejęło w pełni EC2 (patrz Etap 5), więc
lokalnie zostały tylko te dwa kroki. Naprawiony dawno błąd utraty historii
sprzed 3 lat (skrypt scala świeże dane z istniejącym plikiem zamiast go
nadpisywać) — patrz opis Bronze wyżej.
Dalej: Część D — rozbudowa projektu pod portfolio.
Plan: [`notatki/plany/Plan-04-pokazanie-wyniku.md`](notatki/plany/Plan-04-pokazanie-wyniku.md).

**Etap 5 (migracja do AWS):** architektura w pełni ukończona
i zautomatyzowana (01.09). EC2 (Kafka z KRaft, jako usługa `systemd`) →
S3 → Glue → Athena → Silver/Gold. EC2 ma stały adres (Elastic IP) i zostaje
włączone 24/7 (decyzja 31.08). Producent (`kod/data_ingestion.py`)
i Konsument (`kod/kafka_consumer.py`) działają **same, codziennie, przez
`cron` na EC2** (od 01.09) — niezależnie od tego, czy komputer Gracjana
jest włączony; adres brokera przez zmienną `KAFKA_BOOTSTRAP`
(`localhost:9094` wewnątrz EC2), zapis do S3 przez rolę IAM, bez kluczy na
dysku. Historia cen (`bronze/`) wgrana do S3 raz, zamrożona — bieżące dane
niesie już tylko Kafka, do `live/` (obie tabele partycjonowane po spółce,
Glue Crawler + Athena). **Część E:** `silver.py` czyta dane z Athena przez
`pyathena` (zapytanie SQL łączące `bronze` i `live`) zamiast lokalnych
plików spółek. Zostaje jeszcze podłączenie Power BI, odłożone na osobną
sesję. **Część F ukończona:** broker (`systemd`), Producent+Konsument
(`cron` na EC2) i lokalny `pipeline.bat` (od 01.09 tylko `silver.py`
+ `gold.py`, bez lokalnego Producenta — EC2 przejął to zadanie w całości).

**02.09:** harmonogram przesunięty na **po zamknięciu GPW** — `cron` na
EC2 zbiera o 18:00/18:02 polskiego, lokalny Harmonogram (nowy task,
poprzedni się popsuł) o 18:10; wcześniej oba działały o 9:00, w momencie
otwarcia giełdy, ale Yahoo nie miało jeszcze wtedy danych za dany dzień.
Tego samego dnia znaleziony i naprawiony błąd: `live` w Athenie przez
pomyłkę zebrało całą 3-letnią historię zamiast tylko świeżych dni (opisane
w dzienniku 02.09) — posprzątane w S3, `silver.py` dedupuje teraz po dniu
i spółce (nie po pełnym znaczniku czasu), dopisany test regresyjny
w `test_plikow.py`.
Plan: [`notatki/plany/Plan-05-aws-migracja.md`](notatki/plany/Plan-05-aws-migracja.md).

**03.09 — Silver i Gold działają na EC2.** `pandas` i `pyathena`
doinstalowane w `venv` na instancji, rola IAM (`gpw_tracker_ec2_role`)
rozszerzona o `AmazonAthenaFullAccess` — bez tego `silver.py` nie mógł
odpytać Atheny. Oba skrypty dopisane do `cron` jako jedna linijka
o 16:10 UTC (18:10 polskiego): `silver.py && gold.py`, czyli Gold rusza
tylko wtedy, gdy Silver się udał (Gold czyta plik, który tworzy Silver —
bez `&&` policzyłby wczorajsze dane i zapisał jako dzisiejsze). Cały
łańcuch — zbieranie, Silver, Gold — chodzi teraz sam na EC2. Lokalny
Harmonogram zostaje włączony jako wersja zapasowa, do czasu potwierdzenia,
że `cron` działa stabilnie. Tego samego dnia odzyskane 9 wierszy (26.08,
27.08, 31.08 × 3 spółki), które przepadły przy wczorajszym sprzątaniu
w S3 — istniały tam tylko wewnątrz skasowanego zrzutu historii; dane
odtworzone z lokalnych `companies/*.txt` przez Producenta. Tego samego
dnia **ujednolicona godzina w całych danych na `17:00:00`** (fixing na
zamknięcie GPW): `bronze` wgrany na nowo, `live` przebudowany, wcześniej
stały tam trzy różne godziny naraz. Szczegóły w dzienniku 03.09.

**Dalsze kroki:** zebrane w
[`notatki/plany/Plan-06-domkniecie-i-strona.md`](notatki/plany/Plan-06-domkniecie-i-strona.md)
— domknięcie Etapu 4 Część D, decyzja gdzie docelowo mają **lądować**
wyniki Silver/Gold (dziś: pliki na dysku EC2, niewidoczne z zewnątrz),
system przenoszący co jakiś czas starsze dane z `live` do `bronze`
(dziś `bronze` zmienia się tylko przy ręcznym wgraniu, a `live` rośnie
bez końca), i nowy kierunek: strona internetowa pokazująca wynik
projektu. Na razie szkic z otwartymi pytaniami.

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
| `data_ingestion.py` | Główny skrypt — pobiera dane trzech spółek z Yahoo Finance (`requests`), scala je ze starą historią w pliku (żeby ruchome okno 3y nie kasowało starszych dat), pomija ceny, których Yahoo nie zwróciło (`null` — dzień jeszcze nierozliczony, zdarza się wszystkim spółkom naraz), zamiast zapisywać je jako błędny tekst, zapisuje do `companies/{TICKER}.txt`, błędy loguje do `companies/errors.log` (`try/except` + `logging`). Wysyła nowe ceny przez Kafkę (`kafka-python`) na topic `gpw_tracker` — połączenie z brokerem też w `try/except`, brak Kafki nie przerywa pobierania/zapisu lokalnego. Od 01.09 uruchamiany codziennie przez `cron` na EC2 (nazwa do 01.09: `Data ingestion 2.py`) |
| `kafka_consumer.py` | Konsument Kafki: odbiera nowe ceny z topicu `gpw_tracker` (kończy nasłuch po 5s ciszy, nie działa w nieskończoność), grupuje po spółce, zapisuje do S3 partiami (`s3.put_object`, format JSON Lines) pod ścieżką partycjonowaną `live/spolka={TICKER}/...`. Od 01.09 uruchamiany codziennie przez `cron` na EC2, kilka minut po `data_ingestion.py` |
| `test_plikow.py` | Dwa testy: `test_dzialania` sprawdza pobrane pliki `companies/*.txt` (istnieją, poprawny format wiersza, wystarczająco dużo danych); `test_powtorek` (02.09) sprawdza `silver/clean_data.csv` pod kątem duplikatów — czy nie ma dwóch wierszy z tym samym dniem i tą samą spółką |
| `config.py` | Jedno miejsce na listę spółek (`["CBF.WA", "XTB.WA", "SNT.WA"]`) — importowana przez pozostałe skrypty zamiast powielania w kilku plikach |
| `silver.py` | Etap Silver — czyta dane z Athena przez `pyathena` (SQL łączące `bronze` i `live`), naprawia typy (`to_datetime`, `to_numeric`), sprawdza braki, usuwa duplikaty po dniu+spółce, nie po pełnym znaczniku czasu (`bronze` i `live` potrafią zapisać ten sam dzień z inną godziną — błąd znaleziony i naprawiony 02.09, patrz dziennik), sortuje po spółce i dacie, zapisuje do `silver/clean_data.csv` (nazwa do 01.09: `silver 1.py`). Od 03.09 uruchamiany codziennie przez `cron` na EC2 o 16:10 UTC, w jednej linijce z `gold.py` (`&&`); do odpytania Atheny potrzebuje polityki `AmazonAthenaFullAccess` na roli instancji |
| `gold.py` | Etap Gold — wczytuje `silver/clean_data.csv`, liczy dzienną zmianę procentową (`groupby`+`pct_change`), całkowitą zmianę i najbardziej zmienny miesiąc na spółkę (`groupby`+`std`), łączy w tabelę rankingu (`merge`), zapisuje `gold/dane_dzienne.csv` i `gold/ranking.csv` (nazwa do 01.09: `gold 1.py`). Od 03.09 uruchamiany przez `cron` na EC2 zaraz po `silver.py` — i **tylko wtedy, gdy tamten się udał** (`&&`), bo czyta plik, który Silver dopiero tworzy |
| `wykresy.py` | Etap 4, Część A — wczytuje `gold/dane_dzienne.csv`, rysuje cenę wszystkich trzech spółek w czasie (`matplotlib`, `plt.plot` w pętli po spółkach, legenda), zapisuje `wykresy/wykres3spolek.png` |
| `ranking.py` | Etap 4, Część A — wczytuje `gold/ranking.csv`, rysuje wykres słupkowy całkowitej zmiany procentowej spółek (oś Y sformatowana jako „%"), zapisuje `wykresy/ranking.png` |
| `pipeline.py` | Etap 4, Część C — testowy skrypt do sprawdzenia Harmonogramu zadań Windows: dopisuje datę/godzinę uruchomienia do `kod/pipeline.txt` |
| `pipeline.bat` | Łączy kroki Silver i Gold (`silver.py`, `gold.py`) w jedno zadanie Harmonogramu; dwie niezależne linie bez `&&` (łączenie przez `&&`/`^` powodowało, że `silver 1.py` cicho nie zapisywał danych mimo że `gold 1.py` i tak się uruchamiał — porzucone na rzecz pewności działania). Do 01.09 uruchamiał jako pierwszy krok też pobieranie danych — od Etapu 5 Części F to zadanie przejęło EC2. Od 03.09 **wersja zapasowa**: to samo liczy się już na EC2 przez `cron`, a lokalny Harmonogram zostaje włączony do czasu potwierdzenia, że tamto działa stabilnie |
| `pyathena_silver_test.py` | Szkic/materiał referencyjny z Etapu 5, Części E — pierwsza wersja zapytania SQL do Athena przez `pyathena`, zanim trafiła do `silver.py`. Zachowany jako własna notatka, nie wpięty w `pipeline.bat` |

### Dane w `companies/`

Jeden plik `.txt` na spółkę, jeden wiersz na dzień notowania:
```
2023-07-24 09:00:00, 12.34
```
`errors.log` zbiera błędy pobierania (np. nieistniejący ticker) — nie trafia
na GitHub (patrz `.gitignore`).

Godzina w znaczniku to **`17:00:00` — fixing na zamknięcie GPW**, czyli
moment, w którym ustala się kurs zamknięcia (a właśnie ten kurs zapisujemy).
Ujednolicone 03.09 w całych danych, razem z `bronze` i `live` w S3.

**Naprawiony błąd (03.09):** te pliki służą Producentowi za pamięć „co już
wysłałem", a porównywał on wcześniej **pełny tekst daty z godziną**.
Godzina brała się z `datetime.fromtimestamp()`, czyli ze strefy czasowej
maszyny: Windows w Polsce zapisywał `09:00`, EC2 stojące w UTC — `07:00`
dla tej samej chwili. Ponieważ pliki są jednocześnie trzymane w gicie,
każda operacja gita podmieniająca ten plik na EC2 sprawiała, że Producent
nie rozpoznawał żadnej daty i wysyłał całą trzyletnią historię do Kafki
od nowa (tak stało się 01.09). Od 03.09 klucz porównawczy liczony jest
z **samej daty**, a godzina doklejana dopiero przy zapisie i wysyłce —
dzięki temu strefa czasowa maszyny nie ma już znaczenia.

### Dane w `silver/`

Jedna tabela, wszystkie trzy spółki razem, z nagłówkiem:
```
data,cena,spolka
2023-07-24 09:00:00,78.800003,CBF.WA
```

### Dane w `gold/`

Dwa pliki, wynik etapu Gold.

`dane_dzienne.csv` — pełna tabela dzienna, ta sama co
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
3. [[Plan-04-pokazanie-wyniku]] — Etap 4, Część D wciąż w toku
4. [[Plan-05-aws-migracja]] — Etap 5, architektura ukończona
5. [[Plan-06-domkniecie-i-strona]] — co dalej: domknięcie, Silver/Gold, strona
6. [[Slownik]] — zaglądaj, gdy spotkasz nieznane słowo

---

## Zasady prowadzenia notatek

**Dziennik pisze Claude, na koniec każdej sesji, w całości** (od 01.09 —
wcześniej robił to Gracjan sam) — łącznie z rubryką „czego się
nauczyłem", pisaną w pierwszej osobie na podstawie tego, co faktycznie
było nowe w danej sesji. Żadnych pustych placeholderów do uzupełnienia.

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
- [[Plan-06-domkniecie-i-strona]]
- [[Codzienna-rutyna]]
- [[Stare-repo-co-to-bylo]]
- [[Slownik]]
- [[Zrodla]]
