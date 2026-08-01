# GPW Pulse

Projekt nauki data engineeringu — pobieranie i przetwarzanie danych giełdowych
(GPW) dla wybranych spółek.

**Etap BRONZE (surowe dane):** ukończony. Program pobiera dzienne notowania
trzech spółek GPW (CBF, XTB, SNT) z Yahoo Finance za ostatnie 3 lata, zapisuje
je na dysk i sam sprawdza, czy zapisane dane są poprawne.

**Etap SILVER (czyszczenie danych, `pandas`):** w trakcie. Trzy osobne pliki
spółek są wczytywane, naprawiane (typy danych), sprawdzane pod kątem braków
i duplikatów, łączone w jedną tabelę, sortowane i zapisywane jako jeden
czysty plik: `silver/clean_data.csv`.

---

## Struktura folderu

| Folder | Co w nim jest |
|---|---|
| **kod/** | skrypty Pythona projektu (patrz tabela niżej) |
| **companies/** | pobrane dane spółek (pliki `.txt`, jeden na spółkę) + `errors.log` |
| **silver/** | wynik etapu Silver — jedna czysta tabela ze wszystkich spółek (`clean_data.csv`) |
| **notatki/** | notatki do nauki i projektu (patrz niżej) |
| **CLAUDE.md** | zasady pracy z asystentem nad tym projektem |

### Skrypty w `kod/`

| Plik | Co robi |
|---|---|
| `Data ingestion 2.py` | Główny skrypt — pobiera dane trzech spółek z Yahoo Finance (`requests`), zapisuje do `companies/{TICKER}.txt`, błędy loguje do `companies/errors.log` (`try/except` + `logging`) |
| `test_plikow.py` | Sprawdza pobrane pliki: czy istnieją, czy mają poprawny format wiersza, czy jest wystarczająco dużo danych, czy dane da się odczytać jako data i liczba |
| `Data ingestion.py` | Wczesna eksploracja odpowiedzi API Yahoo Finance (Sesja 3) — materiał referencyjny, nieużywany przez resztę programu |
| `silver 1.py` | Etap Silver — wczytuje trzy pliki spółek (`pandas`), naprawia typy (`to_datetime`, `to_numeric`), sprawdza braki i duplikaty, łączy w jedną tabelę (`pd.concat`), sortuje po spółce i dacie, zapisuje do `silver/clean_data.csv` |

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
3. [[Plan-01-bronze]] — sesja 1 czeka
4. [[Slownik]] — zaglądaj, gdy spotkasz nieznane słowo

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
- [[Codzienna-rutyna]]
- [[Stare-repo-co-to-bylo]]
- [[Slownik]]
- [[Zrodla]]
