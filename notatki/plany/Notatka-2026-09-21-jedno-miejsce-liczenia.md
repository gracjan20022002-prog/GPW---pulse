# Notatka 21.09 — jedno miejsce liczenia: wyłączenie lokalnego Harmonogramu i dane poza gitem

**Stan: do zatwierdzenia przez Gracjana.** To szósta naprawa z kolejki
z przeglądu z 08.09 („wyłączenie lokalnego Harmonogramu, `silver/` i `gold/`
poza gitem"). Przeglądowy warunek — wynik Golda w S3 — spełniła naprawa
z 17.09. Dziś nic nie wykonujemy: notatka, potem Twoja decyzja, potem kroki.

## Sedno w trzech zdaniach

Dziś dwie maszyny co wieczór liczą ten sam wynik (EC2 o 18:00, laptop
z Harmonogramem Windows o 18:10), a wersja z laptopa trafia do gita, więc
w repozytorium leżą dwie różne wersje i EC2 musi jedną odrzucać przed każdym
`git pull`. Proponuję, żeby liczyło tylko EC2 (stamtąd wynik idzie do S3
i Atheny): wyłączyć zadanie w Harmonogramie Windows i wyjąć `silver/` i `gold/`
z gita — pliki zostają na dysku, ale git ich nie pilnuje. Największe ryzyko to
nie sam git, tylko dwie ciche pułapki: pierwszy `git pull` na EC2 skasuje
foldery, a wykresy i Power BI pokażą stare dane bez żadnego błędu.

## Przykład na innych danych: dwoje sąsiadów i wspólny zeszyt

Ola i Adam co wieczór liczą tabelę lokalnej ligi i przepisują ją do wspólnego
zeszytu (to jest git). Ola liczy o 18:00, Adam o 18:10 z innego źródła. Przed
każdym wpisem Ola wyrywa stronę Adama (to jest `git checkout`). Wynik z zeszytu
Ola przepisuje jeszcze na tablicę w klubie (to jest S3 i Athena) — Adam tego
nie robi.

| Wieczór | Ola (18:00) | Adam (18:10) | Zeszyt dziś | Zeszyt po zmianie | Tablica w klubie |
|---|---|---|---|---|---|
| wtorek, mecze skończone | Sokoły 3:1 Orły | Sokoły 3:1 Orły | dwie takie same strony | jedna strona Oli | 3:1 |
| środa, Adam liczy z wiadomości sprzed końca meczu | Sokoły 3:1 Orły | Sokoły 2:1 Orły | dwie **różne** strony, nie wiadomo która dobra | jedna strona Oli (3:1) | 3:1 |
| czwartek, Ola chora | nic | Sokoły 3:1 Orły | strona Adama w zeszycie | zeszyt bez nowej strony | **stara** (Adam jej nie ruszy) |

Trzeci wiersz to sedno „zapasu": Adam chroni zeszyt, a nie tablicę, którą
ktoś ogląda.

## Przykład → projekt

| Sąsiedzi | Projekt |
|---|---|
| Ola | EC2 (`cron`, `silver.py`, `gold.py`, wysyłka do S3) |
| Adam | laptop, Harmonogram Windows, `kod/pipeline.bat` |
| zeszyt | git: `silver/clean_data.csv`, `gold/dane_dzienne.csv`, `gold/ranking.csv` |
| tablica w klubie | S3 `gold/` i tabele w Athenie |
| wyrywanie strony Adama | `git checkout -- silver/ gold/` przed `git pull` na EC2 |
| „Adam przestaje liczyć" | wyłączenie zadania w Harmonogramie (*Disable*, nie usunięcie) |
| „zeszyt nie przechowuje tabel" | wpis w `.gitignore` i `git rm --cached` |
| „przegródka na stronę zostaje" | pusty plik `.gitkeep` w `silver/` i `gold/` |

**Nowe słowo: `.gitkeep`.** Git nie zapisuje pustych folderów, więc pusty plik
`.gitkeep` w środku jest tylko po to, żeby folder istniał. Na innych danych:
folder `zdjecia/` z `.gitkeep`, a w `.gitignore` dwie linie: `zdjecia/*`
(„wszystko w tym folderze") i `!zdjecia/.gitkeep` (`!` znaczy „poza tym
jednym"). Wrzucam `kot.jpg` do `zdjecia/` → `git status` nic nie pokazuje;
`git ls-files zdjecia` → `zdjecia/.gitkeep`.

## Stan dziś (sprawdzone 21.09, tylko odczyty lokalne)

- Git śledzi trzy pliki: `silver/clean_data.csv` (95937 B),
  `gold/dane_dzienne.csv` (157886 B), `gold/ranking.csv` (364 B).
  `.gitignore` ich nie wymienia.
- 14 commitów o tytule `Dane z … (lokalny Harmonogram)`. `kod/pipeline.bat` to
  dwie linie (Silver, Gold) i nie ma w nim `git`, więc te commity robisz ręcznie
  (nie sprawdziłem, czy nie ma drugiego zadania).
- Lokalny wynik **nie idzie do S3** (`GOLD_DO_S3` stoi tylko w `crontab` na EC2),
  więc Athena i przyszła strona widzą wyłącznie wersję z EC2.
- Ostatni zapis lokalnych plików: 20.09 o 20:22, nie o 18:10. Nie sprawdzałem,
  dlaczego (możliwe, że laptop był wtedy wyłączony).
- Te pliki czytają: `wykresy.py` (`gold/dane_dzienne.csv`), `ranking.py`
  (`gold/ranking.csv`), `test_plikow.py` (`silver/clean_data.csv`) i Power BI
  (według planu z Części B: `Get Data → Text/CSV`; który plik i skąd ścieżka —
  nie sprawdzałem).
- Precedens: 09.09 zagadka SNT — lokalny ręczny bieg zapisał parę plików
  z dwóch różnych chwil (przegląd z 08.09, sekcja o dwóch maszynach).

## Co proponuję — trzy ruchy, w tej kolejności

1. **Laptop:** zadanie w Harmonogramie Windows wyłączyć. `kod/pipeline.bat`
   zostaje w gicie.
2. **Laptop, git:** `silver/*` i `gold/*` do `.gitignore` z wyjątkiem
   `.gitkeep`; trzy pliki wyjąć z gita (`git rm --cached`, z dysku nie znikają);
   commit i push.
3. **EC2:** rytuał z zasady 14, potem `git pull` — ostatni raz z tym rytuałem.
   Pull skasuje trzy pliki z dysku EC2, ale foldery zostaną dzięki `.gitkeep`;
   o 18:10 Silver i Gold zapiszą pliki od nowa.

Poza tą notatką, osobna decyzja: przepięcie wykresów i Power BI na Athenę.

## Co może pójść źle

- **Pull kasuje foldery, a `silver.py` ich nie tworzy** (`to_csv` nie zakłada
  folderu) → o 18:10 `Traceback`, Gold nie rusza (`&&`), skrypt kontrolny pisze
  maila. Głośno, ale dzień bez nowego Golda. Zapobiega `.gitkeep`.
- Ta sama pułapka na nowej maszynie po `git clone` — też załatwia `.gitkeep`.
- Wykresy, `ranking.py` i Power BI pokażą **stare dane bez błędu** — pliki będą
  stały od ostatniego lokalnego biegu.
- `test_plikow.py` będzie zielony na zamrożonym pliku — kolejny test, który
  sprawdza rzecz obok potoku (znana wada).
- „Zapas" znika, ale był pozorny: lokalny wynik nie trafia do S3, więc chronił
  tylko lokalne pliki; gdy EC2 padnie, Athena stoi i tak.
- **Znika historia dzień po dniu.** 14 commitów `Dane z …` to dziś jedyne
  migawki wyniku (S3 trzyma tylko najnowszy plik — decyzja z 15.09: nadpisywać).
  Odtworzymy je z `bronze/` i `live/`, ale nie jeden do jednego (korekty cen
  Yahoo).
- `git rm --cached` nie czyści historii — dane zostają w starych commitach.
  Pliki są małe, więc zostawiamy.
- Ktoś odpali `gold.py` na laptopie z `GOLD_DO_S3=1` w środowisku i nadpisze
  plik z EC2 — obowiązuje decyzja z 15.09: przełącznik tylko na EC2.
- Pull w oknie 17:55–18:15 ruszałby foldery w trakcie biegu — robić poza nim.

## Decyzje — Twoje

1. **Foldery po pullu.** (a) `.gitkeep` w `silver/` i `gold/` — **rekomendacja**:
   zero zmian w kodzie, działa też na nowej maszynie. (b) `os.makedirs` w
   `silver.py` i `gold.py` — zmiana kodu i wdrożenie na EC2. (c) ręczne `mkdir`
   na EC2 — jednorazowe, nie chroni nowej maszyny.
2. **Harmonogram.** (a) wyłączyć (*Disable*) — **rekomendacja**, odwracalne
   jednym kliknięciem. (b) usunąć zadanie.
3. **`kod/pipeline.bat`.** (a) zostaje do przepięcia wykresów —
   **rekomendacja**. (b) usuwamy od razu.
4. **Historia gita.** (a) zostawić — **rekomendacja**. (b) przepisać
   (`git filter-repo`) — ryzykowne dla plików, które ważą razem ok. 250 KB.
5. **Termin.** (a) jedno posiedzenie jutro w ciągu dnia (22.09), pierwszy
   sprawdzian o 18:10 — **rekomendacja**. (b) dziś po 18:30, ale wieczór jest
   już zajęty odczytami. W obu wariantach EC2 poza oknem 17:55–18:15.

## Jak sprawdzimy

Przewidywania zapisane w wiadomości **przed** każdą komendą (kroki po
zatwierdzeniu).

- **Próba na klonie testowym**, zanim dotkniemy EC2: czy pull po
  `git rm --cached` kasuje pliki, a folder z `.gitkeep` zostaje. Na razie to
  wniosek z reguł gita, nie coś, co widziałem.
- Laptop po pushu: `git ls-files silver gold` → tylko dwa `.gitkeep`;
  `git status` czysty.
- EC2 po pullu: `ls -a silver gold` → w każdym tylko `.gitkeep`;
  `git status --short` bez linii.
- Bieg o 18:10: Silver i Gold bez `Traceback`, dwa razy `S3: wysłano`,
  `COUNT(*)` w Athenie zgodny z liczbą policzoną przed biegiem.
- Harmonogram: w zadaniach stan „Wyłączone"; kolejnego dnia data zapisu
  lokalnych plików się nie zmienia.

## Co to zepsuje za miesiąc

- Commity „Dane z …" znikają; czysty `git status` jest od tej pory sygnałem, że
  nic nie hałasuje.
- Rytuał `git checkout -- silver/ gold/` (zasada 14) przestaje być potrzebny —
  CLAUDE.md do poprawienia po wykonaniu.
- Analizy kompletności czytały lokalny `gold/dane_dzienne.csv`; po zmianie
  idą przez Athenę albo przez pobranie pliku z S3.
- Kompakcja 1.10 (`bronze`, laptop) bez związku.
- Wykresy i Power BI, jeśli ich nie przepniemy, pokażą coraz starsze dane.

## Czego nie sprawdziłem

- Co dokładnie robi zadanie w Harmonogramie (nazwa, wyzwalacz, akcje) — to
  pierwszy krok po zatwierdzeniu, do odczytu przez Ciebie.
- Który plik i skąd czyta Power BI.
- Czy S3 ma włączone wersjonowanie (wtedy migawki dzień po dniu by zostały).

## Powiązane notatki

- [[Przeglad-2026-09-08-co-nie-gra]] — sekcja o dwóch maszynach liczących to
  samo; kolejność napraw, punkt 6
- [[Notatka-2026-09-15-wynik-golda-do-s3]]
- [[Notatka-2026-09-18-sygnal-awarii]]
- [[Plan-04-pokazanie-wyniku]] — Power BI
