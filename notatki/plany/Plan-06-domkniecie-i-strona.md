# Plan-06 — Domknięcie starych wątków i strona internetowa

Data utworzenia: 2026-09-01

---

## Skąd ten plan

Sesja 01.09 skończyła Część F Etapu 5 (`cron` na EC2, F3+F4) — całe
zbieranie danych działa teraz samo, bez udziału Gracjana. Przy okazji
rozmowy „co dalej" wyszło kilka osobnych wątków naraz: stare zaległości
(Część D Etapu 4, Część E Etapu 5), nowy pomysł na porządki w nazewnictwie,
pytanie o to, gdzie powinny mieszkać Silver/Gold, i duży, nowy kierunek —
strona internetowa. Ten plik zbiera je wszystkie w jednym miejscu, żeby nie
zgubić żadnego.

**Ten plan jest żywy**, tak jak Plan-04 i Plan-05 — część wątków (1, 2, 5)
jest już dobrze zdefiniowana, część (3, 4) to na razie szkic z otwartymi
pytaniami, dopisywany w miarę postępu.

---

## Osiem wątków, różny stopień gotowości

| # | Wątek | Status |
|---|---|---|
| 1 | Domknięcie Etapu 4, Część D (README, wnioski, porządki) | opisane w Plan-04, nietknięte |
| 2 | Spójność projektu — nazewnictwo, porządki w plikach | ✅ zrobione 01.09 |
| 3 | Dokąd trafiają Silver/Gold (zostają lokalnie? EC2? S3?) | 🔶 punkt 1 (gdzie działa kod) ✅ zrobiony 03.09; punkt 2 (gdzie ląduje wynik) wciąż otwarty |
| 4 | **Etap 6 — strona internetowa** | wstępny szkic, duży, nowy obszar |
| 5 | Etap 5, Część E — Power BI → Athena | świadomie odłożone (dziś: „jeszcze trochę") |
| 6 | Dalsza mapa (więcej spółek, ESPI, AI) | już w `Plan-ogolny.md`, później |
| 7 | Pułapka ze strefami czasu w `companies/*.txt` | ✅ znaleziona i naprawiona 03.09 |
| 8 | Przenoszenie starszych danych z `live` do `bronze` | nowy pomysł 03.09, nierozpoczęty |

---

## Wątek 1 — Domknięcie Etapu 4 (Część D)

Pełny opis w [[Plan-04-pokazanie-wyniku]], sekcja „Część D". Trzy sesje,
żadna jeszcze nieodbyta:

- **D1** — rozbudowa górnej części `README.md` pod kątem pracodawcy, jeden
  zapisany wykres jako obrazek.
- **D2** — `notatki/Wnioski.md` (nowy plik — sprawdzone 01.09, jeszcze nie
  istnieje): kilka zdań po ludzku, które wnioski płyną z danych.
- **D3** — przegląd `kod/` (zbędne `print()`, nazewnictwo — patrz Wątek 2
  niżej), finalny commit+push.

---

## Wątek 2 — Spójność: nazewnictwo i porządki ✅ zrobione 01.09

`kod/` ujednolicone do `snake_case` (`data_ingestion.py`, `silver.py`,
`gold.py`, `pyathena_silver_test.py`); stary, nieużywany
`Data ingestion.py` usunięty, nie przemianowany (kolizja nazw ze
`data_ingestion.py`). `pipeline.bat` i `crontab` na EC2 zaktualizowane.
Po drodze znaleziony i naprawiony konflikt `git pull` na EC2 — szczegóły
w dzienniku 01.09 i [[project-etap5-part-f-plan]].

Opis poniżej zostawiony jako zapis stanu sprzed zmiany:

Przed zmianą w `kod/` mieszały się dwa style nazw:

- Ze spacjami i wielką literą: `Data ingestion.py`, `Data ingestion 2.py`,
  `gold 1.py`, `silver 1.py`, `pyathena silver test.py`
- `snake_case`, bez spacji: `kafka_consumer.py`, `config.py`, `wykresy.py`,
  `ranking.py`, `pipeline.py`, `test_plikow.py`

**Uwaga na koszt zmiany, zanim zaczniecie:** `Data ingestion 2.py` to
akurat ten plik, którego nazwę dziś bardzo dokładnie wpisaliście do
`crontab` na EC2 (z cudzysłowem wokół spacji) i do `pipeline.bat`. Zmiana
tej jednej nazwy oznacza wejście z powrotem w oba te miejsca i poprawienie
ścieżki — nie jest to duże, ale to prawdziwa, dodatkowa robota, nie tylko
„zmień nazwę pliku". Pliki bez zewnętrznych odniesień (np. `pyathena
silver test.py` — czysto referencyjny) są bezpieczniejsze do ruszenia
najpierw.

**Zakres do ustalenia w sesji:** ujednolicić na `snake_case` (np.
`data_ingestion.py`, `data_ingestion_2.py` albo lepsza nazwa,
`gold_1.py`→`gold.py`, `silver_1.py`→`silver.py`), zaktualizować wszystkie
miejsca, które odwołują się do starych nazw: `pipeline.bat`, `crontab` na
EC2, ewentualnie Harmonogram Windows (jeśli wskazuje bezpośrednio na plik,
nie tylko na `pipeline.bat`).

---

## Wątek 3 — Dokąd trafiają Silver i Gold

Pytanie z dzisiejszej rozmowy: „przenieść silver/gold na S3?" Zanim
zdecydujemy, jedno rozróżnienie: **S3 przechowuje dane, nie uruchamia
kodu.** To dwa osobne pytania, które łatwo zlać w jedno:

1. **Gdzie fizycznie działa kod** `silver 1.py`/`gold 1.py` — dziś lokalnie
   (Windows, Harmonogram). Mogłyby zamiast tego działać na EC2 (jak
   Producent/Konsument, przez `cron`) — wtedy nie potrzebują Twojego
   komputera w ogóle.
2. **Gdzie ląduje wynik** — dziś lokalne pliki (`silver/clean_data.csv`,
   `gold/*.csv`). Gold mógłby zamiast tego zapisywać do S3 (nowa
   tabela/partycja w Glue/Athena) — wtedy wynik jest osiągalny z zewnątrz
   (np. przez przyszłą stronę), niezależnie od tego, gdzie fizycznie
   liczony.

Te dwie rzeczy można zmieniać osobno albo razem. Argument za którymkolwiek
(albo obiema) wynika wprost z Wątku 4: strona z wykresami „aktualizującymi
się codziennie" potrzebuje, żeby dane były zarówno **świeże bez Ciebie**
(punkt 1), jak i **osiągalne skądś indziej niż Twój dysk** (punkt 2).

Koszt: kolejna instalacja (`pandas` w `venv` na EC2, jeśli pkt 1), a
`t3.micro` już raz padł przez brak pamięci przy mniejszym obciążeniu niż
broker + 2 skrypty + pandas naraz — do przemyślenia razem z pamięcią/swapem.

~~**Decyzja odłożona na osobną sesję**~~ — **punkt 1 zrobiony 03.09.**
`pandas` i `pyathena` doinstalowane w `venv` na EC2, rola instancji
(`gpw_tracker_ec2_role` — nie `GPWTrackerEC2Role`, jak błędnie stało
w Planie-05) rozszerzona o `AmazonAthenaFullAccess`, oba skrypty
w `crontab` jako jedna linijka `silver.py && gold.py` o 16:10 UTC.
Obawa o pamięć okazała się nieuzasadniona: swap z 31.08 wciąż żyje
(2 GiB, zajęte 209 Mi), instalacja i oba biegi przeszły bez problemu.
Wynik na EC2 potwierdzony jako identyczny z lokalnym (2280 wierszy
w tej samej chwili). Szczegóły — dziennik 03.09.

**Punkt 2 (gdzie ląduje wynik) zostaje otwarty.** Dziś Silver i Gold
zapisują pliki na dysk EC2, gdzie nikt ich nie widzi z zewnątrz. To
pytanie ma sens dopiero razem z Wątkiem 4 (strona) — bo to strona
zdecyduje, skąd te dane mają być czytane.

---

## Wątek 4 — Etap 6: strona internetowa

Pomysł z 01.09, na razie **szkic, nie plan sesji**. Cel, własnymi słowami
Gracjana: strona (niekoniecznie pod publicznym adresem — wystarczy dostęp
przez prywatny link/plik) z ładnym overlayem najważniejszych informacji,
wykresami z Power BI aktualizującymi się codziennie, zakładkami dla
poszczególnych spółek, i słownikiem giełdowym (rozbudowa tego, co już
istnieje w `notatki/Slownik.md` — 445 linii na 01.09, więc nie od zera).

**Otwarte pytania, do rozstrzygnięcia, zanim zacznie się projektowanie:**

1. **Co znaczy „prywatna" strona, technicznie?** Power BI „Publish to
   web" robi stronę faktycznie **publiczną** dla każdego z linkiem — to
   nie to samo, co strona chroniona hasłem/logowaniem. Trzeba wybrać
   konkretny mechanizm, zanim zacznie się cokolwiek budować.
2. **Jaki stos technologiczny?** To zupełnie nowy obszar (HTML/CSS/JS,
   hosting) — dotąd nietknięty w tym projekcie, podobnie nowy jak AWS był
   19.08.
3. **Jak wykresy trafiają na stronę?** Zależy od odpowiedzi na pytanie 1 —
   osadzony Power BI, czy własne wykresy rysowane z danych w Athenie.
4. **Zależność od Wątku 3** — codzienna aktualizacja strony wymaga, żeby
   dane były świeże bez udziału Gracjana (patrz wyżej).

**Realistyczna skala:** to nie dodatek na koniec projektu — to osobny
etap, wielkości porównywalnej do całego Etapu 5 (tygodnie, nie dni), bo
obejmuje kompletnie nowy zestaw umiejętności. Kolejność sesji dopiszemy
dopiero, gdy padną odpowiedzi na pytania 1–3 — tak jak Etap 5 zaczynał się
od jednego zdania i rozrósł się w miarę pracy.

---

## Wątek 5 — Etap 5, Część E: Power BI → Athena

Ostatni kawałek Etapu 5 z 31.08, świadomie odłożony — dziś ponownie: „jeszcze
trochę". Zostaje jako otwarty punkt, bez konkretnej sesji. Warto go
rozważyć **razem** z Wątkiem 4 (strona) przy okazji — jeśli strona ma
pokazywać wykresy, konektor Power BI→Athena może się przydać w obu miejscach
naraz.

---

## Wątek 6 — Dalsza mapa (z `Plan-ogolny.md`, nieco starsza)

Zapisane dawno, wciąż aktualne, kolejność orientacyjna:

1. Więcej spółek (3→30) — tylko zmiana w pliku ustawień, nietknięte.
2. Codzienna automatyzacja — **zrobione 01.09** (Część F).
3. Testy sprawdzające dane — częściowo już jest (`test_plikow.py`).
4. Raporty giełdowe ESPI (web scraping) — nietknięte, trudne.
5. AI do rozpoznawania typu/kategorii raportu — **to jest dokładnie to**,
   o czym Gracjan wspomniał 01.09 („dzienny automatyczny import informacji
   o spółkach i dopasowywanie kategorii przez agentów AI") — ten sam
   pomysł, teraz doprecyzowany. Zanotowane, zdecydowanie nie teraz —
   naturalnie pasuje **po** Wątku 4 (strona), bo potrzebuje miejsca, gdzie
   te informacje ktoś zobaczy.

---

## Wątek 7 — Pułapka ze strefami czasu ✅ znaleziona i naprawiona 03.09

Producent trzymał w `companies/*.txt` pamięć „co już wysłałem" i porównywał
**pełny tekst daty z godziną**, a godzina pochodziła z
`datetime.fromtimestamp()`, czyli ze strefy maszyny: Windows `09:00`,
EC2 `07:00` dla tej samej chwili. Pliki są przy tym trzymane w gicie —
więc każda operacja gita podmieniająca ten plik na EC2 (`pull`, a 01.09
`stash` przy rozwiązywaniu konfliktu) sprawiała, że instancja nie
rozpoznawała żadnej daty i wysyłała całą trzyletnią historię do Kafki od
nowa. To jest prawdziwa przyczyna zalewu z 01.09, który kosztował całą
sesję 02.09 i utratę trzech dni danych.

**Rozwiązanie:** klucz porównawczy liczony z **samej daty** (przy czytaniu
pliku odcinana godzina, po stronie Yahoo `.date()`), a godzina doklejana
dopiero na wyjściu — przy zapisie pliku i wysyłce do Kafki. Dzięki temu
przejście nie wywołało zrzutu: stary wiersz `2026-08-26 09:00:00` i nowy
`2026-08-26 17:00:00` dają ten sam klucz.

**Przy okazji ujednolicona godzina w całych danych na `17:00:00`** — to
moment fixingu na zamknięcie GPW, czyli ustalenia kursu, który zapisujemy
(sprawdzone: notowania ciągłe 9:00–16:50, zamknięcie 17:00, dogrywka do
17:05). Wcześniej w danych stały trzy różne godziny naraz. Wymagało to
przepisania `bronze` (2286 wierszy, wgrane na nowo) i przebudowy `live`
(30 wierszy wysłanych ponownie, 16 starych plików skasowanych). Sam
zapis daty **musiał** zostać 19-znakowy, bo `pandas` przy mieszance
„z godziną" i „bez godziny" w jednej kolumnie rzuca `ValueError` — wersja
z samą datą położyłaby `silver.py`.

---

## Wątek 8 — Przenoszenie starszych danych z `live` do `bronze` (nowy, 03.09)

Pomysł Gracjana z końca sesji 03.09, **nierozpoczęty**. Dziś nic tego nie
robi: `bronze` zmienia się wyłącznie przy ręcznym wgraniu (dwa razy do tej
pory — 20.08 i 03.09), a `live` rośnie bez końca, o 3 wiersze i 3 nowe
pliki na każdą sesję giełdową. Warstwa „zamrożona" się starzeje, a
strumieniowa zbiera ok. 750 drobnych plików rocznie — klasyczny „small
files problem", bo Athena płaci stały narzut za każdy plik.

Proponowana częstotliwość (jego): co dwa tygodnie albo co miesiąc.

**Do rozstrzygnięcia w osobnej sesji:** czy uruchamia to czwarta linijka
`cron` na EC2, czy zostaje czynnością świadomie ręczną; skąd biorą się
dane do przepisania (Athena zna już jedno i drugie); co dokładnie znaczy
„starsze" i czy po przeniesieniu kasować wiersze z `live`, czy zostawić
nakładkę (dziś nieszkodliwą — `silver.py` i tak dedupuje po dniu i spółce,
a po 03.09 osiem dni siedzi w obu tabelach naraz); i czy przy okazji nie
zmienić formatu warstwy zamrożonej na taki, który Athena czyta szybciej.

Pasuje naturalnie do punktu 2 Wątku 3 — oba są o tym, żeby dane dało się
dosięgnąć spoza instancji EC2.

---

## Zrobione 01.09 i 03.09

**01.09** — Wątek 2 (spójność nazewnictwa), patrz wyżej i dziennik 01.09.

**03.09** — Wątek 3 punkt 1: Silver i Gold działają na EC2 przez `cron`,
potwierdzone tego samego dnia (wpis o 16:10 UTC odpalił się sam — dowodem
był wynik Golda w `companies/errors.txt`, bo tylko `cron` przekierowuje
tam wyjście). Odzyskane 9 wierszy utraconych przy sprzątaniu S3 z 02.09.
Znaleziony i naprawiony Wątek 7, przy okazji ujednolicona godzina w całych
danych na `17:00:00`. Zapisany nowy Wątek 8.

Następna sesja, do wyboru: Wątek 1 (Etap 4, Część D — README pod
pracodawcę, `Wnioski.md`), Wątek 8 (przenoszenie `live` → `bronze`)
albo punkt 2 Wątku 3 (gdzie mają lądować wyniki Silver/Gold, dziś
niewidoczne spoza EC2).

---

## Czego NIE robimy teraz

- ❌ Projektowanie całej strony naraz (overlay + zakładki + słownik +
  wykresy) — najpierw odpowiedzi na otwarte pytania z Wątku 4.
- ~~❌ Przenoszenie Silver/Gold gdziekolwiek dziś — osobna sesja.~~
  **Nieaktualne od 03.09** — wykonanie przeniesione na EC2 (punkt 1
  Wątku 3). Zapis wyniku zostaje na razie na dysku EC2.
- ❌ ESPI, AI-kategoryzacja — dalsza mapa, nie teraz.
- ❌ Rezygnacja z lokalnego Harmonogramu, dopóki nowe rozwiązanie (jeśli
  powstanie) nie jest sprawdzone.

---

## Powiązane notatki

- [[Plan-ogolny]] — punkty 1, 4, 5 z „Co dalej po miesiącu" to Wątek 6 tutaj
- [[Plan-04-pokazanie-wyniku]] — pełny opis Części D (Wątek 1)
- [[Plan-05-aws-migracja]] — cała architektura AWS, Część F zrobiona 01.09
- [[Slownik]] — tu trafi słownictwo giełdowe na stronę (Wątek 4)
