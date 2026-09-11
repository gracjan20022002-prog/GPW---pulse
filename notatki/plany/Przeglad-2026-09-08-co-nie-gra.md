# Przegląd całego projektu — co nie gra i jak to zmienimy

Data: 2026-09-08. Napisane na żądanie Gracjana po tym, jak nazwał
problem wprost: codziennie nowa sesja, codziennie nowy błąd do naprawy,
projekt nie idzie do przodu — a pomysłodawcą kolejnych rzeczy jest
Claude, więc to Claude nie przewiduje skutków. Ten plik jest odpowiedzią:
uczciwy spis tego, co dziś nie działa, co nie będzie pasować do planu,
skąd się to wzięło, i jak od dziś pracujemy.

Podstawa: przeczytany od nowa cały kod (`kod/*.py`, `pipeline.bat`),
wszystkie 24 wpisy dziennika (21.07–07.09), wszystkie plany, README,
`requirements.txt`, `.gitignore`, historia 52 commitów, pamięć projektu.
Nic poniżej nie jest napisane z pamięci — każdy punkt ma odnośnik do
pliku i linii albo do daty w dzienniku.

---

## Część 1 — Skąd się wzięły te błędy (odpowiedzialność Claude'a)

Gracjan ma rację co do mechanizmu. Prawie każda naprawa z ostatnich
dwóch tygodni naprawiała coś, co Claude wcześniej zaproponował,
zbudował krok po kroku razem z nim i **nazwał ukończonym**. Konkretnie,
z datami:

| Data | Co Claude zaproponował lub przepuścił | Co to kosztowało |
|---|---|---|
| 20.08 | Upload do `bronze/` wpisany na stałe do skryptu zamiast jednorazowo | Gracjan sam zauważył 24.08, że to sprzeczne z planem |
| 21.08 | Pamięć Producenta „co już wysłałem" oparta na pliku `.txt` z **pełnym znacznikiem czasu** jako kluczem | Zalew Kafki całą historią 01.09, cała sesja 02.09 na sprzątanie, 3 dni danych utracone, naprawa 03.09 |
| 21.08 | `auto_offset_reset='latest'` w Konsumencie — wygoda przy testach (pominąć stare wiadomości testowe) wpisana do kodu produkcyjnego | Zostało do dziś, patrz punkt 2.3 |
| 31.08 | „Naprawa" `KafkaProducer` przez `try/except` i `producer = None` — a zapis pliku pamięci został **bezwarunkowy** | Producent po cichu oznacza dni jako wysłane, choć nic nie wysłał. Nazwane naprawą. Pułapkę zauważoną 03.09 zapisano w notatkach, ale nie naprawiono. Sprawdzone dziś na żywo: 12 wierszy oznaczonych jako wysłane, zero wysłanych |
| 01.09 | `cron` na 9:00 polskiego — moment **otwarcia** GPW | Yahoo nie miało jeszcze świecy dziennej. Przesunięte 02.09 |
| 01.09 | Rekomendacja `git stash` przy konflikcie `git pull` na EC2 | To `stash` podmienił pamięć Producenta i odpalił zalew 01.09 |
| 03.09 | Propozycja samej daty bez godziny w pliku spółki | Położyłoby `silver.py` (`to_datetime` na mieszance formatów). Gracjan złapał przed wdrożeniem |
| 04.09 | Propozycja `DROP TABLE` przy wyniku 405 w Athenie | Crawler jeszcze pracował; tabela była dobra. `SELECT * LIMIT 5` uratował od kasowania działającej tabeli |
| 04.09 | Przykład dydaktyczny z wymyślonymi datami przekleił się do skryptu | Błąd do wyjaśnienia, pół godziny |
| 07.09 | `python -m pip freeze` podane bez informacji, że `venv` musi być włączone | `requirements.txt` nadpisany listą Pythona systemowego |
| 07.09 → 08.09 | README i notatki opisują `data_ingestion.py` jako działający i ukończony; dziś ten sam plik ma cztery poważne wady | Utrata zaufania do słowa „ukończone" |
| 01.09 → 08.09 | Sześć razy przypisane Gracjanowi autorstwo dziennika, który pisze Claude | Sześć poprawek tej samej rzeczy |
| 10.08–25.08 | **Dziesięć wpisów dziennika** ma zamiast „Czego się nauczyłem" pusty szablon „(do uzupełnienia przez Gracjana)" — Gracjan nigdy tego nie pisał i nie miał pisać | Dziennik jest w jednej trzeciej niedokończony |

Wzorzec pod spodem jest jeden i Claude go nazywa wprost: **zamykanie
etapu podsumowaniem, które mówi „ukończone", zanim rzecz została
sprawdzona w warunkach, w których ma działać.** „Działa, kiedy odpalę
ręcznie" było traktowane jak „działa". Pierwszy prawdziwy sprawdzian —
`cron` bez nadzoru, `git pull` na drugiej maszynie, awaria brokera —
przychodził sesję albo dwie później i wyglądał jak nowy błąd. To nie
były nowe błędy. To były stare decyzje, których skutków nikt nie policzył.

Drugi wzorzec: **zasady pracy ustalane w rozmowie ginęły po jednej
sesji**, bo `CLAUDE.md` był celowo skrócony do 300 słów i nie mieścił
ich, a pamięć Claude'a między sesjami okazała się zawodna. Od dziś
`CLAUDE.md` jest tak długi, jak musi być.

---

## Część 2 — Co dziś nie działa albo działa źle

Uporządkowane wzdłuż drogi danych. **Waga:** 🔴 kasuje lub fałszuje
dane · 🟠 ukryta awaria, nikt się nie dowie · 🟡 brud, dług, mylące ·
⚪ drobiazg.

### 2.1 Producent — `kod/data_ingestion.py`

- ✅ **NAPRAWIONE 08.09** — `send(...).get(timeout=10)`, flaga per
  spółka, zapis pliku pod `if flaga`. Sprawdzone lokalnie z martwym
  brokerem (plik nietknięty) i prawdziwym biegiem `cron` na EC2
  (767 wierszy, Silver 2301). Poniżej opis stanu sprzed naprawy:
  ~~🔴~~ **Zapisuje „już wysłałem" bez wysłania.** Linie 65–67 nadpisują
  `companies/{spółka}.txt` wszystkimi datami niezależnie od tego, czy
  wysyłka (62–64) się odbyła. Gdy broker nie odpowiada (`producer =
  None`, linia 26) dni znikają z kolejki na zawsze. Zdarzyło się
  naprawdę 25–31.08 (3 dni odzyskiwane ręcznie 03.09). Sprawdzone dziś
  z martwym adresem brokera: 762 → 766 wierszy w każdym pliku, zero
  wiadomości. Do tego `producer.send()` (64) nie czeka na potwierdzenie,
  a `flush()` (73) stoi **za** pętlą, czyli po zapisaniu wszystkich
  plików — błąd dostarczenia też nie cofnie zapisu.
- 🔴 **Cena z trwającej sesji zapisana jako kurs zamknięcia.** Skrypt
  pobiera „dziś" o każdej porze i dokleja `17:00:00` (linie 64, 67).
  Uruchomiony przed 17:00 zapisuje cenę bieżącą z etykietą fixingu.
  Dziś o 16:43: CBF `194.5` jako „zamknięcie 08.09". Pilnuje tego
  wyłącznie godzina w `crontab`, nie kod.
- 🟠 **Okno na pobranie kursu zamknięcia ma najwyżej kwadrans zapasu —
  zmierzone 11.09, wcześniej nikt tego nie liczył.** Tego dnia o 17:45
  lokalny bieg Producenta z martwym brokerem znalazł **siedem** nowych
  dni, nie osiem: Yahoo nie oddawało jeszcze świecy za 11.09 albo
  oddawało ją z pustą ceną, którą kod pomija warunkiem `c is not None`.
  Bieg `cron` o 18:00 już ją miał — pliki spółek 769 → 770,
  `Odebrano 3 wiadomości`, Silver `(2310, 3)`. Odstęp między publikacją
  u źródła a naszym biegiem wynosi więc **najwyżej piętnaście minut**.

  Skutek, gdyby Yahoo kiedyś spóźniło się bardziej: wieczorny bieg nie
  znajduje nowych dni, Konsument wypisuje `Odebrano 0`, a Silver o 18:10
  liczy dzień bez dzisiejszych notowań i **nic tego nie sygnalizuje**.
  Dane nie giną, bo Producent dośle brakujący dzień nazajutrz, ale wynik
  wieczorny jest przez dobę cichy i nieprawdziwy.

  Razem z czerwonym punktem wyżej znaczy to, że pora biegu jest ściśnięta
  z obu stron: za wcześnie daje cenę z trwającej sesji podpisaną jako
  zamknięcie, za późno nie daje nic. To podnosi wagę `CRON_TZ` (2.10) —
  po zmianie czasu **bez** niego bieg przesunie się na 17:00 polskiego,
  czyli dokładnie w stronę czerwonego błędu.

- 🟠 **Korekty Yahoo nie docierają do S3.** Yahoo zmienia ceny za dni
  już opublikowane (CBF 01.09: 191,30 → 191,40; SNT 01.09: 329,60 →
  327,00). Plik lokalny po cichu bierze nową wartość (linia 59), ale
  ten dzień nie jest w `nowe_daty`, więc korekta nigdy nie leci do
  Kafki. `bronze` i `live` trzymają cenę z pierwszego pobrania.
- 🟨 **Komunikat w logu kłamie — połowa naprawiona 08.09.** Linia 25
  mówi dziś „Wystąpił błąd łączenia z brokerem" razem z adresem, zamiast
  dawnego „Wystąpił błąd przy pobieraniu danych spółki". Potwierdzone
  10.09 przy czytaniu `errors.log` na EC2: osiem zachowanych wpisów
  z 31.08 ma jeszcze starą treść, bez nazwy spółki i z kropką na końcu.
  **Wciąż otwarte:** `except` w linii 78 łapie razem z błędami sieci
  także `TypeError` i `KeyError`, czyli **błędy w kodzie** — dwa razy
  (13.08, 21.08) prawdziwy błąd programisty był logowany jako „błąd
  pobierania".
- 🟠 **Adres brokera na sztywno** (linia 18: publiczny IP). Na EC2
  nadpisuje go zmienna z `crontab`; przy ręcznym uruchomieniu przez SSH
  jej nie ma → publiczny IP → hairpin NAT → `producer = None` → punkt
  pierwszy. Ręczny bieg na EC2 bez `KAFKA_BOOTSTRAP=localhost:9094`
  gubi dane.
- 🟠 **Jedno źródło danych, nieoficjalne, bez planu B.** Yahoo `v8/finance/chart`
  z podrobionym `User-Agent` (linia 48). Stooq już raz zablokował
  (23.07). Jeśli Yahoo zmieni format albo zacznie blokować, cały projekt
  staje. Odpowiedź Yahoo nie jest też stała między wywołaniami — dziś
  brakowało 07.09, choć wczoraj było.
- 🟨 Martwy kod: zakomentowany import `boto3` i blok wysyłki do S3
  **usunięte 10.09**. Zostają dwa `print`-y (ścieżka i `response.url`) —
  świadomie, bo są dziś jedynym śladem Producenta w `errors.txt`;
  zastąpi je jedna linia podsumowania, gdy da się ją sprawdzić z żywym
  brokerem (10.09 się nie dało, bo wysyłka zepsułaby sprawdzenie 3b).
- ✅ **NAPRAWIONE 10.09** — `requests.get` bez `timeout` (linia 49).
  Wpisane `timeout=(10, 30)`. Sprawdzone lokalnie obiema drogami:
  z `timeout=0.001` trzy wpisy „błąd przy pobieraniu" w `errors.log`
  w odstępie 30 ms i pliki spółek nietknięte (762 wiersze), z wartością
  docelową trzy adresy Yahoo i zero wpisów o błędzie. Najgorszy przypadek
  dla trzech spółek to 120 s przy 600 s odstępu do Silvera. **Na EC2
  dopiero po `git pull` 11.09.** Poniżej opis stanu sprzed naprawy:
  ~~🟠~~ Gdy Yahoo przyjmie połączenie i zamilknie, Producent czeka bez
  końca: Konsument w tej samej linii `cron` nie ruszy, Silver o 16:10
  policzy wczorajszy stan, a jutrzejszy `cron` uruchomi drugiego
  Producenta obok wiszącego.

### 2.2 Kafka — broker na EC2

- 🟠 **Wiadomości żyją w topicu 7–14 dni** (domyślna retencja Kafki
  7 dni, ale kasowanie idzie całymi segmentami — sprawdzone 09.09 na
  dysku brokera, patrz 2.3). Jeśli
  Konsument nie zadziała przez tydzień (zepsuty `venv` po `git pull`,
  pełny dysk, cokolwiek), Producent dalej wysyła i oznacza jako wysłane,
  a broker po tygodniu kasuje nieodebrane. Dane do S3 nie trafią nigdy,
  a jedyna kopia zostanie w pliku pamięci Producenta na EC2. Nikt się
  nie dowie — patrz 2.7.
- 🟡 `t3.micro`, 913 MB RAM, swap 2 GB. Broker + trzy skrypty Pythona +
  `pandas` naraz. Działa, ale bez zapasu; historia 31.08 (SSH przestało
  odpowiadać) pokazuje, gdzie jest granica.

### 2.3 Konsument — `kod/kafka_consumer.py`

- ✅ **NAPRAWIONE 08.09** — `'earliest'`; zakładka grupy 2330/2330,
  LAG 0. **Zwykła ścieżka sprawdzona 09.09** prawdziwym biegiem `cron`
  (`Odebrano 3 wiadomości`, 2333/2333, LAG 0). **Poprawka 09.09 do
  „retencja 7 dni":** broker kasuje całymi segmentami, nie pojedynczymi
  wiadomościami — wiadomość żyje 7–14 dni. Sprawdzone na dysku brokera:
  `earliest` = 22, `latest` = 2330, zalew z 01.09 (offsety 22–2326) leży
  w zamkniętym segmencie `...0022.log` z ostatnią wiadomością z 07.09
  16:00 UTC i zniknie około 14.09 16:00 UTC. **Test „zakładki nie ma"
  dopiero po tym** (termin do wyboru Gracjana: 14.09 po 18:15 albo 15.09
  przed 18:00; najpierw `kafka-get-offsets.sh --time earliest` ma pokazać
  2327), inaczej Konsument wlałby zalew drugi raz. Stan sprzed naprawy:
  ~~🟠~~ **`auto_offset_reset='latest'`** (linia 11). Gdy grupa
  `gpw_consumer` straci zapisaną pozycję (Kafka kasuje offsety grupy po
  7 dniach bez aktywności; albo ktoś zmieni `group_id`), Konsument
  wystartuje od „teraz" i **po cichu pominie** wszystko, co Producent
  wysłał wcześniej. Wybrane 21.08, żeby nie łapać wiadomości testowych
  — powód dawno nieaktualny. Właściwa wartość dla potoku: `'earliest'`.
- ✅ **WDROŻONE 09.09, sprawdzenie 10.09** — Producent i Konsument
  w jednej linii `crontab` o 16:00 UTC, rozdzielone `;` (decyzja
  Gracjana: Konsument rusza zawsze, bo zależy od tego, co leży w Kafce,
  nie od kodu wyjścia Producenta; Producent i tak prawie zawsze kończy
  zerem, bo łapie swoje awarie w `except`; `&&` w jedynej sytuacji,
  w której coś zmienia — Producent wybuchł po zapisaniu pliku pierwszej
  spółki — zostawiłoby jej wiadomości w Kafce na śmierć). Każdy skrypt
  ze swoim `>> errors.txt 2>&1`, w stylu linii `10 16`. Kopia sprzed
  edycji: `~/crontab-kopia-0909.txt` na EC2. Liczby na 10.09: adresy
  Yahoo w logu **przed** `Odebrano 3 wiadomości`, `(2307, 3)` ×2,
  769 wierszy, pozycja 2336. Ścieżka „Producent wybuchł, Konsument
  ruszył" sprawdzona czytaniem, nie biegiem. Stan sprzed zmiany:
  ~~🟠~~ **Sprzężenie przez minuty w `crontab`.** Producent 16:00, Konsument
  16:02, timeout 5 s ciszy (linia 13). Jeśli Yahoo odpowie wolno albo
  broker się zamyśli, Konsument kończy z „Odebrano 0 wiadomości",
  wiadomości czekają do jutra, a `silver.py` o 16:10 liczy wczorajszy
  stan i zapisuje jako dzisiejszy. Nikt się nie dowie.
- 🟡 Pole `spółka` (z `ł`) w treści wiadomości jest potrzebne
  Konsumentowi (linia 19 grupuje po nim), ale zapisane do JSON-a dubluje
  partycję `spolka=` w ścieżce → w tabeli `live` w Athenie martwa
  kolumna. `SELECT *` z `UNION` wywala się na różnicy liczby kolumn
  (już raz 25.08).
- 🟡 Adres brokera na sztywno (linia 7), jak w Producencie.

### 2.4 S3 / Glue / Athena

- 🟠 **Nowa spółka = niewidoczna partycja.** Athena widzi nowe pliki
  w istniejących partycjach sama, ale **nową partycję** (`live/spolka=NOWA/`)
  dopiero po `MSCK REPAIR TABLE` albo ponownym biegu crawlera (dokładnie
  to zablokowało XTB i SNT 25.08). „Więcej spółek" to punkt 1 na liście
  „co dalej" — dodanie czwartej do `config.py` da poprawny Producent,
  poprawny Konsument, poprawne pliki w S3 i **tabelę bez tej spółki**,
  bez żadnego błędu.
- 🟡 Nazwa bucketa, region i nazwa bazy wpisane na sztywno w trzech
  plikach (`silver.py:7–9`, `compaction.py:11–13, 28, 39`,
  `kafka_consumer.py:28`). `config.py` trzyma tylko listę spółek.
- 🟡 Rola IAM użytkownika `gpw-tracker-admin` ma `IAMFullAccess` — zostało
  po walce z crawlerem 24.08, nie jest potrzebne do niczego dziś.

### 2.5 Silver — `kod/silver.py`

- 🟠 **Niedeterministyczny wybór ceny przy rozbieżnych duplikatach.**
  Sortowanie po `["spolka", "data"]` (linia 15), potem
  `drop_duplicates(keep="first")` po dniu i spółce (17). Gdy ten sam
  dzień jest w `bronze` i w `live` z **różną ceną** (korekta Yahoo,
  punkt 2.1), oba wiersze mają identyczny klucz sortowania — który
  będzie „pierwszy", zależy od tego, jak `sort_values` ułożył równe
  elementy, a domyślnie nie jest to stabilne. To jest źródło wczorajszej
  zagadki 327 / 329,60.
- 🟡 Sprawdzenia w liniach 20–22 są po części tautologią: `assert
  dane.duplicated().sum() == 0` **po** `drop_duplicates` zawsze przejdzie.
  Nie ma sprawdzenia, ile wierszy ubyło, ani czy liczba dni na spółkę
  jest taka sama dla wszystkich trzech.
- ✅ Zakomentowana stara wersja (26–35) **usunięta 10.09**; przepis
  „Silver bez Atheny" zostaje w historii gita i w dzienniku 10.09.
- 🟡 `print(dane.shape)` (19) — jedyny ślad w logu EC2, bez daty.
  **Zostaje świadomie** (decyzja 10.09): to jedyny dowód, że Silver się
  uruchomił, i liczba, którą sprawdzamy wieczorem.
- ✅ Adres bucketa, region, baza i folder wyników Atheny **przeniesione
  do `config.py` 10.09**; sprawdzone biegiem — `git diff` na `silver/`
  pusty, plik identyczny co do bajta.

### 2.6 Gold — `kod/gold.py`

- 🔴 **„Najbardziej zmienny miesiąc" jest liczony źle dla bieżącego
  miesiąca.** Odchylenie standardowe (linia 21) z pięciu dni września
  konkuruje z pełnymi miesiącami po 20+ dni. Dziś `ranking.csv` mówi,
  że najbardziej zmienny miesiąc XTB to `2026-09` — bo ma 5 obserwacji,
  w tym −9,8 %. Ta liczba trafi na stronę i będzie nieprawdziwa
  przez pierwszy tydzień każdego miesiąca.

  **Uzupełnienie 11.09 — jest gorzej, niż mówiło zdanie wyżej.** Wynik
  nie jest po prostu zły przez pierwszy tydzień, on **miga z dnia na
  dzień**. Trzy odczyty tej samej komórki dla XTB: 08.09 `2026-09`,
  10.09 `2025-01`, 11.09 znowu `2026-09` z odchyleniem 3,77 wobec 3,70
  dla stycznia 2025. Niedokończony miesiąc przechodzi nad pełnym
  i z powrotem, ilekroć dojdzie jeden mocniejszy dzień — dziś XTB
  skoczyło ze 144,34 na 148,50. Do tego 11 września to dziewiąty dzień
  notowań miesiąca, czyli **dawno po pierwszym tygodniu**; ograniczenie
  „przez pierwszy tydzień" było za łagodne. Na stronie oznaczałoby to
  liczbę, która zmienia się bez powodu widocznego dla czytelnika.
- 🟡 Kolumna `max_zmienny_miesiac` (18) w `dane_dzienne.csv` to po prostu
  miesiąc każdego wiersza, nie „najbardziej zmienny" — nazwa myli
  każdego, kto zobaczy plik bez kodu. W `ranking.csv` kolumna
  `zmiana_proc` to odchylenie standardowe, a w `dane_dzienne.csv` ta
  sama nazwa to zmiana dzienna (decyzja z 06.08, świadoma — ale na
  stronie to będzie wymagało tłumaczenia).
- ✅ **Dziewięć** `print()` (6, 7, 10, 12, 13, 16, 19, 20, 23 — ta lista
  miała dziewięć numerów przy słowie „osiem"; poprawione 10.09), z czego
  sześć to rusztowanie z sierpnia. **Sześć usuniętych 10.09**, zostały
  trzy: kształt tabeli, ranking całego okresu i `sp_rank`. Sprawdzone
  biegiem, `git diff` na `gold/` pusty.

  **Poprawka 11.09 do liczby linii.** Zdanie „log Golda z czterdziestu
  linii zszedł do trzech" myliło wywołania `print` z liniami wyjścia:
  dwa z trzech pozostałych `print` wypisują tabelę, nie jedną wartość.
  Zmierzone na EC2 11.09: blok Golda **37 → 11 linii**, a cały blok
  jednego biegu 49 → 23. Trzy to liczba wywołań, nie linii.
- ✅ Komentarz w linii 1 (odwołania do `Data ingestion 2`, `silver 1`,
  `gold 1`) **usunięty 10.09**.

### 2.7 Wynik i jego brak

- 🔴 **Łańcuch urywa się na dysku EC2.** `silver.py:23`, `gold.py:24–25`
  zapisują CSV do folderu repozytorium na instancji. Nic ich nie
  zabiera. Power BI, strona, ktokolwiek — nie mają skąd czytać.
  Dane wchodzą do chmury i wychodzą z niej z powrotem na jeden dysk za
  SSH.
- 🟠 **Dwie maszyny liczą to samo i obie wersje trafiają do gita.**
  Lokalny Harmonogram (18:10) uruchamia `pipeline.bat` → `silver.py` +
  `gold.py` na Windowsie, wynik ląduje w `silver/` i `gold/`, które są
  śledzone przez git. 17 z 52 commitów rusza `gold/dane_dzienne.csv`.
  EC2 ma własną, inną wersję → każdy `git pull` na EC2 wymaga
  `git checkout -- silver/ gold/`. Wczorajsza zagadka SNT wzięła się
  dokładnie z tego: lokalny ręczny bieg zapisał parę plików z dwóch
  różnych chwil.
- 🟡 **Trzy ostrzeżenia co wieczór w `errors.txt`** (sprawdzone 09.09,
  linie 324–330): `kafka-python` o `value_deserializer` jako `lambda`,
  `boto3` o Pythonie 3.9 (wsparcie skończyło się 29.04.2026), `pandas`
  o `read_sql` z połączeniem `pyathena`. Żadne nie jest błędem, ale
  sygnał awarii (krok 8) będzie musiał odróżniać ostrzeżenie od
  `Traceback`.
- 🟠 **Nikt się nie dowie, że coś padło.** `companies/errors.txt` na EC2
  to całe `stdout` + `stderr` obu skryptów, bez jednej daty. Prawdziwy
  `Traceback` leży tam, dopóki ktoś nie wejdzie przez SSH i nie
  przeczyta. Lokalny `errors.log` przez tydzień (25–31.08) zbierał
  `KafkaTimeoutError` i nikt nie patrzył.
- 🟠 **Log jest podwójny i czytamy tylko jedną połowę** (zauważone
  10.09 przy notatce do sprzątania). `logging.basicConfig`
  w Producencie pisze do `companies/errors.log`, a `cron` przekierowuje
  wypisy obu skryptów do `companies/errors.txt`. To dwa różne pliki.
  Wszystko, co Producent zgłasza przez `logging.error` — nieudane
  połączenie z brokerem, błąd pobierania, błąd dostarczenia wiadomości —
  trafia do `errors.log`, do którego przez cały wrzesień nikt nie
  zajrzał na EC2. W `errors.txt`, który sprawdzamy co wieczór, są tylko
  `print`-y i niezłapane `Traceback`. Do tego `basicConfig` ustawia log
  dla całego Pythona, więc do `errors.log` dopisują się też biblioteki
  (08.09 `kafka-python` dołożył tam cztery linie o zerwanym
  połączeniu). Do rozstrzygnięcia w kroku 8: jeden plik czy dwa,
  i który z nich jest tym, na który patrzymy.
  **Przeczytany po raz pierwszy 10.09:** `errors.log` na EC2 ma osiem
  linii i jedną datę, 31.08, z dwóch ręcznych biegów bez
  `KAFKA_BOOTSTRAP` (adres publiczny, hairpin NAT). Od 31.08 ani jednego
  wpisu — cisza prawdziwa, nie zepsuty zapis, bo ten sam kod zapisał
  10.09 cztery wpisy na Windowsie. Okoliczność łagodząca, przypadkowa:
  od 09.09 Konsument stoi w jednej linii z Producentem po średniku, więc
  awaria Producenta objawi się w `errors.txt` jako `Odebrano 0
  wiadomości` zamiast trójki. To nie jest sygnał awarii, tylko efekt
  uboczny.
- 🟠 **`pipeline.bat` bez `&&`** (dwie niezależne linie, decyzja z 13.08
  po tym, jak `&&` cicho gubiło krok Silver) — a `crontab` na EC2 ma
  `silver.py && gold.py`. Dwie maszyny, dwie różne semantyki tego samego
  łańcucha; Harmonogram Windows raportuje sukces po kodzie wyjścia
  ostatniej linii, więc awaria Silver jest niewidoczna.

### 2.8 Kompakcja — `kod/compaction.py`

- ✅ **NAPRAWIONE 08.09** — kopia obecnego `bronze` z S3 do
  `bronze/poprzedni/` (`download_file`, `except ClientError` → 0 dla
  nowej spółki) i `assert` per spółka „nowa liczba ≥ poprzednia" przed
  pierwszym zapisem. Obie ścieżki sprawdzone biegiem: zwykły bieg
  761/761, granica `2026-08-01` → `AssertionError … 761 … 740`, nic nie
  zapisane. Stan sprzed naprawy:
  ~~🔴~~ **Brak sprawdzenia przed nadpisaniem i kasowaniem.** Skrypt czyta
  z Atheny, **nadpisuje** trzy pliki `bronze` w S3 (linia 28) i **kasuje**
  pliki z `live` (39). Nie porównuje liczby wierszy z poprzednim
  stanem `bronze`. 04.09 Athena zwróciła 405 zamiast 2283 bez żadnego
  błędu (crawler w trakcie pracy). Gdyby kompakcja trafiła na taki
  moment, nadpisałaby `bronze` jedną piątą danych i skasowała `live`
  — bo `HAVING` też pyta Athenę. Bez kopii. Pierwszy prawdziwy bieg:
  1 października.
- 🟠 Uruchamiana ręcznie, z Windowsa, na kluczach lokalnego użytkownika
  IAM. „Raz w miesiącu" zależy od tego, czy Gracjan pamięta. `pyarrow`
  na EC2 celowo niezainstalowany, więc na EC2 się nie uruchomi.
- 🟡 `print` diagnostyczne (20, 30, 31), w tym testowy odczyt Parquetu
  zostawiony z sesji 04.09.

### 2.9 Testy — `kod/test_plikow.py`

- 🟠 **Testy sprawdzają rzeczy obok potoku, nie potok.** `test_dzialania`
  sprawdza `companies/*.txt` — od 07.09 to pamięć Producenta, nie
  źródło danych. `test_powtorek` sprawdza lokalny `silver/clean_data.csv`
  — na Windowsie to kopia z gita, nie świeży wynik. Prawdziwa droga
  (Athena → Silver → Gold) nie ma żadnego testu. Nie ma testu, który
  powiedziałby „dziś brakuje jednej spółki" albo „w `live` jest dzień
  z przyszłości".
- ✅ `print` ścieżki (6) **usunięty 10.09**; cztery testy dalej zielone.

### 2.10 Środowisko i wdrożenie

- 🟠 **`requirements.txt` nie odtworzy środowiska EC2.** Pin
  `pandas==3.0.5` — na EC2 03.09 `pip` tej wersji nie znalazł
  (zainstalowano 2.3.3). Lokalnie `pandas` 3.0.5 pokazuje typ `str`,
  EC2 pokazuje `object`; dziś to kosmetyka, jutro różnica w zachowaniu.
  EC2 ma Pythona 3.9, którego `boto3` już nie wspiera (ostrzeżenie od
  31.08).
- 🟠 **Wdrożenie = `git pull` + ręczna pamięć.** Zmiana nazwy pliku
  wymaga ręcznej edycji `crontab` (01.09 — przeoczone, cały wieczór
  bez danych). `git pull` wymaga rytuału `git checkout -- silver/ gold/`.
  Nic nie sprawdza, że kod na EC2 to ten sam, co na GitHubie.
- 🟡 **Zmiana czasu** — koniec października `crontab` z 16:00/16:10
  na 17:00/17:10 UTC (od 09.09 dwie linie, nie trzy), ręcznie,
  z pamięci. `CRON_TZ=Europe/Warsaw`
  na górze `crontab` załatwiłoby to raz na zawsze.

  **Sprawdzone 10.09, cztery odczyty na EC2, nic nie zmienialiśmy:**
  cronie 1.5.7 (`rpm -q cronie`), napis `CRON_TZ` obecny w samym
  `/usr/sbin/crond` (`grep -a -c` → 1), strefa systemu UTC
  (`timedatectl`), definicja `Europe/Warsaw` obecna (2654 bajty).
  Warunki spełnione. To poszlaka, nie dowód działania — ostatecznym
  będzie bieg o właściwej godzinie.

  **PUŁAPKA, bez której ta zmiana psuje dane:** samo dopisanie
  `CRON_TZ=Europe/Warsaw` przesunęłoby bieg o dwie godziny wstecz, bo
  cron przeczytałby dotychczasowe `0 16` i `10 16` jako szesnastą
  **polską**. Producent pobierałby cenę o 16:00, godzinę przed
  zamknięciem GPW, i zapisywał ją jako kurs zamknięcia (wada 2.1,
  czerwona). Strefa i godziny muszą pójść **jednym ruchem**:
  `CRON_TZ` na górze, godziny przepisane z `16` na `18`.

  Korzyść uboczna: dziś EC2 liczy o 18:00 polskiego, a Harmonogram
  Windows o 18:10 polskiego. Po zmianie czasu **bez** `CRON_TZ` EC2
  przesunęłoby się na 17:00, a Windows został na 18:10 — maszyny
  rozjechałyby się o godzinę. Z `CRON_TZ` zostają zgrane.

  Termin: nie w dniu, w którym inny bieg ma coś potwierdzać. Rytuał jak
  09.09 — najpierw `crontab -l > ~/crontab-kopia-RRMM.txt`, praca na
  drugiej kopii, `diff` przed wgraniem.
- 🟨 Pliki-śmieci: `kod/pipeline.py`, `kod/pipeline.txt`,
  `kod/pyathena_silver_test.py` i `.claude/settings.local.json`
  **usunięte 10.09** (plików w `kod/` w gicie: 12 → 10).
  `kod/pipeline.bat` **zostaje** — to jego uruchamia Harmonogram Windows
  o 18:10, znika dopiero w kroku 6. `wykresy/*.png` z 10.08 zostają,
  wracamy do nich przy wykresach.
- ⚪ Klucz `.pem` w `aws/` w folderze synchronizowanym przez OneDrive.
  Poza gitem, ale w chmurze Microsoftu.

### 2.11 Dokumentacja

- 🟠 **README obiecuje więcej, niż jest.** Dziewięć razy „ukończony /
  w pełni / zautomatyzowana" w pierwszych 128 liniach. Góra README to
  chronologiczna kronika, 120 linii przed strukturą folderu — nie opis
  projektu.
- 🟠 **Dziesięć wpisów dziennika z pustym „Czego się nauczyłem"**
  (21.07, 10.08, 12.08, 13.08, 17.08, 19.08, 20.08, 21.08, 24.08,
  25.08). Do napisania przez Claude'a, z treści tych wpisów.
- 🟡 `CLAUDE.md` przez miesiąc za krótki, żeby unieść ustalenia — stąd
  gubienie zasad. Od dziś przepisany.
- 🟡 Plany: Plan-04 i Plan-05 mają sekcje przekreślone i „nieaktualne
  od…" obok aktualnych; Plan-06 numeruje wątki 1–10 i wymaga tłumaczenia
  „co jest czym" przy każdym użyciu.

---

## Część 3 — Co nie będzie pasować do planu

Plan Gracjana (Plan-ogólny + rozmowa 01.09 + dziś): idealnie czysty
i działający łańcuch `data_ingestion → Kafka → S3/Athena → silver →
gold` → wynik na stronie internetowej; potem więcej spółek, ESPI,
kategoryzacja AI. Poniżej to, co z dzisiejszego stanu **zderzy się**
z każdym z tych kroków.

| Krok planu | Co się zderzy | Punkt wyżej |
|---|---|---|
| Strona z codzienną aktualizacją | Wynik Golda leży na dysku EC2, nie ma go skąd czytać | 2.7 |
| Strona pokazuje „najbardziej zmienny miesiąc" | Liczba jest błędna przez pierwszy tydzień miesiąca | 2.6 |
| Strona pokazuje dane „aktualne na dziś" | Nikt nie wie, czy dzisiejszy bieg się udał — brak sygnału awarii | 2.7, 2.2, 2.3 |
| Power BI → Athena | Wymaga sterownika ODBC i kluczy AWS na maszynie z Power BI; „Publish to web" jest publiczne — pytanie o prywatność strony nierozstrzygnięte od 01.09 | Plan-06 |
| Więcej spółek (3 → 30) | Nowa partycja niewidoczna w Athenie bez crawlera; 30 plików pamięci Producenta; 30 × 3 lata przez Kafkę przy pierwszym biegu; `t3.micro` | 2.4, 2.2 |
| ESPI / AI | Nowe źródło danych obok Yahoo — a już jedno jest bez planu B i bez testu drogi | 2.1, 2.9 |
| Kompakcja w `cron` | Bez sprawdzenia przed kasowaniem to zautomatyzowana utrata danych; `pyarrow` na EC2 | 2.8 |
| Pokazanie pracodawcy | README-kronika, „ukończone" obok znanych wad, dziennik z dziurami | 2.11 |
| Praca na dwóch maszynach przez kolejne miesiące | Każdy `pull` z rytuałem, `crontab` z pamięci, środowiska rozjeżdżają się | 2.10 |

---

## Część 4 — Jak od dziś pracujemy

To są zasady, nie sugestie. Zapisane też w `CLAUDE.md`.

### 4.1 Najpierw naprawa, potem budowa

Żadnej nowej funkcji, żadnego nowego narzędzia, dopóki lista z Części 2
nie jest zamknięta w kolejności ustalonej z Gracjanem. Wykresy, README
pod pracodawcę, Power BI, strona — **po** czystym łańcuchu. Gracjan
wybiera, co bierzemy; Claude nie narzuca tematu.

### 4.2 Definicja „zrobione"

Claude nie napisze „ukończone", „działa", „zautomatyzowane" o niczym,
co nie spełnia **wszystkich pięciu** warunków:

1. Działa na prawdziwej drodze danych, nie w teście ręcznym obok niej.
2. Ma sprawdzenie, które to udowadnia (liczba wierszy policzona **przed**
   uruchomieniem i potwierdzona po; `assert`; test).
3. Awaria jest **głośna**: kod błędu, wyjątek, wpis z datą — nie `pass`,
   nie `producer = None` i jazda dalej.
4. Wdrożone tam, gdzie ma działać (EC2), i sprawdzone **tam**, nie
   tylko lokalnie.
5. Opisane w README i w planie zgodnie z prawdą — łącznie z tym, czego
   jeszcze nie ma.

Jeśli któryś warunek nie jest spełniony, Claude pisze, który i dlaczego.

### 4.3 Zanim powstanie kod — notatka projektowa

Przed każdą zmianą mechanizmu (nowy skrypt, nowa tabela, nowy `cron`,
nowe narzędzie) Claude pisze krótką notatkę: **co** robimy, **po co**,
**co może pójść źle** (z listą: co się stanie, gdy broker nie odpowie,
gdy Athena zwróci pół tabeli, gdy skrypt odpali się dwa razy, gdy odpali
się o złej godzinie, gdy dojdzie czwarta spółka), **jak sprawdzimy**,
że działa, i **co to zepsuje za miesiąc**. Gracjan czyta i zatwierdza.
Dopiero potem kod. To jest odpowiedź na „nie przewidujesz".

### 4.4 Każda instrukcja — tak samo

- Kroki ponumerowane, w kolejności wykonania, jeden numer = jedna rzecz.
- Każda komenda z etykietą **maszyny i środowiska**: `[lokalny
  PowerShell, (.venv) włączone]` albo `[EC2, przez SSH]` — zawsze, także
  ostatnia komenda dnia, także `git`.
- Przy każdym kroku: gdzie jesteś (plik + linia albo maszyna), co
  robisz, **co masz zobaczyć**, żeby wiedzieć, że się udało.
- Analiza i tło w osobnej sekcji, nie wplecione między kroki.

### 4.5 Każde tłumaczenie — tak samo

- Nowe słowo, funkcja, moduł, wyrażenie — wyjaśnione **przy pierwszym
  użyciu**, prostym językiem, bez zakładania, że Gracjan je zna.
- Zawsze przykład na **innych danych** (lody, pogoda, SMS-y — nie
  spółki), z pokazanym wejściem **i** wyjściem, nie tylko opisem.
- Kod projektu pisze Gracjan. Claude pokazuje kształt na obcym
  przykładzie i pyta, zamiast podawać linijkę do wklejenia.
- Nowe pojęcia trafiają do `Slownik.md` tego samego dnia.

### 4.6 Decyzje należą do Gracjana

Claude przedstawia możliwości z konsekwencjami i mówi, którą by wybrał
i dlaczego. Nie wybiera za Gracjana, nie rozpisuje planu dla tematu,
którego Gracjan nie wybrał, nie prowadzi ku końcowi sesji. Sesja kończy
się, gdy Gracjan to powie.

### 4.7 Bez żargonu numerów

„Wątek 3 punkt 2", „Część D", „Etap 5 E" — nie używamy bez powiedzenia
w tym samym zdaniu, co to jest. Lepiej: „wynik Golda poza EC2" niż
„punkt 2 Wątku 3".

### 4.8 Dokumentację pisze Claude

Dziennik (cały, łącznie z „Czego się nauczyłem"), README, `CLAUDE.md`,
plany, słownik — Claude, na koniec sesji, gdy Gracjan powie, że
kończymy. Gracjan nie pisze w dzienniku i nigdy nie pisał; Claude nie
cytuje dziennika jako słów Gracjana.

### 4.9 Sprawdzać, nie zakładać

Przed każdym stwierdzeniem o stanie plików, danych, gita, EC2 — Claude
czyta, liczy, sprawdza. Gdy nie może sprawdzić (EC2, AWS), podaje
Gracjanowi komendę i czeka na wynik. Przewidywany wynik pisany
**przed** uruchomieniem.

### 4.10 Przegląd całości raz na jakiś czas

Taki przegląd jak ten — cały kod, wszystkie notatki, od początku — nie
raz na miesiąc po awarii, tylko po zamknięciu każdego większego kawałka
i zawsze na prośbę Gracjana. Wynik: ten plik zaktualizowany, punkty
zamknięte przekreślone, nowe dopisane.

---

## Część 5 — Kolejność napraw (zatwierdzona 08.09)

**Stan realizacji** (aktualizowany na koniec każdej sesji):

| # | Krok | Stan |
|---|---|---|
| 1 | Producent przestaje gubić dane | ✅ 08.09 — sprawdzone lokalnie i przez `cron` na EC2 |
| 2 | Zabezpieczenie kompakcji | ✅ 08.09 — obie ścieżki sprawdzone biegiem |
| 3a | Konsument `'earliest'` | ✅ 08.09 wdrożone; zwykła ścieżka potwierdzona 09.09 przez `cron`; test „zakładki nie ma" przełożony na po 14.09 — zalew z 01.09 wciąż w topicu (2.3) |
| 3b | Producent i Konsument w jednej linii `crontab` | ✅ **10.09 sprawdzone biegiem `cron` na EC2.** Wszystkie cztery liczby przewidziane 09.09 trafione: w `errors.txt` ścieżka i trzy adresy Yahoo **przed** `Odebrano 3 wiadomości` (dowód, że przekierowanie łapie oba skrypty), `(2307, 3)` dwa razy, 769 wierszy w plikach spółek, pozycja grupy 2336/2336 przy LAG 0. Niezależne potwierdzenie z Windowsa: lokalny Silver o 18:10 wyciągnął z Atheny 2307 wierszy z dzisiejszą datą dla wszystkich trzech spółek. Kopia sprzed edycji `~/crontab-kopia-0909.txt` zostaje na EC2 |
| 4 | Sprzątanie kodu i konfiguracji | ✅ **11.09 wdrożone na EC2 i sprawdzone biegiem `cron`.** Zakres zrobiony 10.09 lokalnie: `timeout=(10, 30)`, martwy kod i cztery pliki-śmieci, `config.py` na bucket/region/bazę/adres Atheny, siedem `print`-ów, martwy import `ticker` w Konsumencie. Notatka: [[Notatka-2026-09-10-sprzatanie-kodu]]. **Dowód z 11.09, wszystkie sześć liczb policzonych przed biegiem i trafionych:** `errors.txt` 417 → 440, blok jednego biegu 49 → 23 linie, sam blok Golda 37 → 11 linii, pliki spółek 770, `errors.log` dalej 8, pozycja grupy 2339/2339 przy LAG 0. W bloku ani jednego `dtype:`, ani wiersza z twardych numerów 748–752, ani samotnej liczby `38`. Potwierdzenie niezależne z Windowsa: lokalny `silver/clean_data.csv` 2311 linii i ranking identyczny co do ostatniej cyfry, mimo trzynastu różnic w pakietach i dwóch wersji Pythona. Z pięciu warunków „zrobione" spełnia cztery; piąty, głośna awaria, nie jest zadaniem tego kroku i czeka na krok 8. Świadomie odłożone poza ten krok: `CRON_TZ` |
| 4a | Podsumowanie w Producencie | 🟨 **11.09 napisane i sprawdzone lokalnie.** Zdjęte ze sprzątania 10.09, bo wymagało żywego brokera. Notatka z czterema decyzjami i dwoma testami: [[Notatka-2026-09-11-podsumowanie-w-producencie]]. Test z martwym brokerem zdany: `nowych dni 7, wysłane 0, stan nietknięte` na spółkę, pliki nietknięte przy 762 wierszach, `errors.log` +4. **Na EC2 nie trafiło 11.09 celowo**, bo wieczorny bieg potwierdzał krok 4. Zostaje test na EC2 zwykłym biegiem `cron`: oczekiwane `nowych dni 1, wysłane 1, stan zapisane` i długość bloku bez zmian, cztery linie za cztery |
| 4b | Spisy wymagań dla dwóch maszyn | ✅ **11.09 zmierzone i rozdzielone.** `requirements.txt` → `requirements-lokalny.txt` przez `git mv` (32 paczki, Python 3.14.2), nowy `requirements-ec2.txt` (19 paczek, Python 3.9.25), oba czystym `pip freeze` bez komentarzy, żeby porównanie działało jedną komendą. Notatka: [[Notatka-2026-09-11-wymagania-dwie-maszyny]]. Wynik pomiaru: czternastu paczek na EC2 brakuje i **wszystkie czternaście mają wyjaśnienie** — siedem ciągnie `matplotlib`, cztery `pytest`, plus te dwa narzędzia i `pyarrow`; jedyna nadwyżka `pytz` to zależność pandas 2. Nic nie brakuje przypadkiem. Dwie paczki są na EC2 **nowsze** niż na laptopie. README (104) poprawiony: twierdził, że bez `pyarrow` projekt nie ruszy, co jest nieprawdą od 04.09. `compaction.py` ma komentarz „wyłącznie lokalnie" |
| 5–10 | reszta | ⬜ |

Uzasadnienie kolejności przy każdej pozycji: dlaczego tu, a nie gdzie
indziej.

1. **Producent przestaje gubić dane** (2.1, pierwsze dwa punkty) —
   jedyne, co dziś kasuje dane; niezależne od reszty; rozpoczęte 08.09
   (test wykonany, poprawka do napisania).
2. **Zabezpieczenie kompakcji** (2.8) — 1 października nadchodzi;
   bez sprawdzenia liczby wierszy przed nadpisaniem to bomba z zegarem.
   Mała zmiana, duża stawka.
3. **Konsument: `earliest` i łańcuch w `crontab`** (2.3) — dwie
   linijki, zamykają dwie ciche dziury. (09.09: łańcuch z `;`, nie
   `&&` — uzasadnienie w 2.3.)
4. **Sprzątanie kodu i konfiguracji** (2.1 martwy kod, 2.5, 2.6
   `print`, 2.9 `print`, 2.10 śmieci, `config.py` dla bucketa/regionu/
   bazy, `CRON_TZ`) — zanim ruszymy strukturę, żeby kolejne zmiany były
   widoczne jako zmiany.
5. **Wynik Golda do S3 i do Atheny** (2.7) — największy kawałek,
   domyka łańcuch, umożliwia stronę; wymaga notatki projektowej (4.3)
   przed kodem.
6. **Wyłączenie lokalnego Harmonogramu, `silver/` i `gold/` poza gitem**
   (2.7) — dopiero gdy wynik jest w S3, bo wtedy git przestaje być
   jedynym miejscem, gdzie widać wynik.
7. **Test prawdziwej drogi** (2.9) — pisany na końcu, gdy kształt
   łańcucha jest ostateczny.
8. **Sygnał awarii** (2.7 `errors.txt`) — na końcu, bo to, na co
   reagujemy, zależy od ostatecznego kształtu.
9. **Gold: pełne miesiące w rankingu** (2.6) — przed stroną, bo strona
   to pokaże.
10. **Dokumentacja** (2.11) — dziesięć wpisów dziennika, README od nowa,
    plany posprzątane — równolegle, przez Claude'a, w tle każdej sesji.

Poza kolejnością, do decyzji Gracjana kiedyś: plan B dla źródła danych
(2.1), `IAMFullAccess` (2.4), Python 3.9 na EC2 (2.10).

---

## Powiązane notatki

- [[Plan-06-domkniecie-i-strona]] — dotychczasowa lista wątków; punkty
  z niej, które są tu, zostają tam jako historia
- [[Plan-05-aws-migracja]] — architektura, do której odnoszą się punkty 2.2–2.4
- [[Slownik]] — pojęcia z tego przeglądu: retencja, offset, `earliest`,
  segment, kod wyjścia, `;`/`&&` — dopisane 09.09; idempotentność —
  przy pierwszym użyciu w sesji
