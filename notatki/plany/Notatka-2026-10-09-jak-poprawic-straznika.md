# Notatka 09.10: jak poprawić strażnika kompakcji (wszystko w jednym miejscu)

To instrukcja do `Notatka-2026-10-09-straznik-kompakcji.md` (zatwierdzona 09.10, wszystkie decyzje
(a)). Tu jest **wszystko**: kroki, zasady, nowe pojęcia z wejściem i wyjściem, przypadki
z wynikami, tabela błędów i przewidywania. Przy ocenie kodu odwołuję się tylko do tej notatki.
Jeśli czegoś zabraknie — powiem wprost i dopiszę.

Przykład to budki z lodami, nie spółki. **Każdy wynik z przykładu pochodzi z uruchomienia 09.10**
(Python 3.14.2, laptop, `botocore` 1.43.75, błędy udawane — bez łączenia z AWS). Numery linii po
zmianie sprawdzone na kopii pliku w brudnopisie Claude'a. Twojego pliku nie ruszałem.

**Jedna rzecz nowa względem notatki projektowej (do Twojej decyzji, Część 7):** próba generalna —
prawdziwy bieg kompakcji jeszcze w październiku. Nic by nie zmienił w danych (`stara 783 = nowa 783`,
`Usunięto 0 plików`), a sprawdziłby zwykłą drogę nowego kodu miesiąc przed listopadem.

---

## Część 1. Kroki (po jednej linii, szczegóły niżej)

**Porcja 1 — sprawdzenie kodów S3, przed kodem (laptop, `(.venv)`):**
1. Pobranie nieistniejącego pliku z naszego bucketu → ostatnia linia z `(404)`.
2. To samo ze zmyślonymi kluczami i istniejącym plikiem → ostatnia linia z `(403)`.

**Porcja 2 — zmiana w `kod/compaction.py` (VS Code):**
3. Blok pobrania kopii (linie 25–32) przenieść nad zapytanie do Atheny (linia 20).
4. `except ClientError:` → złapany wyjątek dostaje nazwę `e`.
5. Pod nim: zmienna `kod` z kodem odpowiedzi.
6. Warunek: `kod` równy napisowi `"404"` → `poprzedni[t] = 0`.
7. W przeciwnym razie: `raise`.
8. `python -m py_compile kod/compaction.py` → nic nie wypisuje.

**Porcja 3 — ścieżka błędu na prawdziwym skrypcie (zmyślone klucze):**
9. Odczyt `bronze/`, `live/` i `bronze\poprzedni` przed biegiem.
10. `python kod/compaction.py` ze zmyślonymi kluczami → `(403) … HeadObject`, nic więcej.
11. Ten sam odczyt po biegu → bez zmian.

**Porcja 4 — próba generalna (tylko jeśli wybierzesz, Część 7).**

**Porcja 5 — commit i `git push`** (razem z dokumentacją sesji). Na EC2 nic nie wdrażamy —
kompakcja działa tylko na laptopie.

---

## Część 2. Zasady, wszystkie naraz

1. **Zmieniasz tylko kolejność i blok `except`.** Strażnik (`assert`), zapis do `bronze` i kasowanie
   z `live/` zostają bez zmian.
2. **Blok pobrania stoi za `s3 = boto3.client("s3")`** (potrzebuje `s3`) i za dwoma `os.makedirs`
   (potrzebuje folderu `bronze/poprzedni`), a **przed** `df = pd.read_sql(…)`.
3. **Przenosisz cały blok: od `poprzedni = {}` do `poprzedni[t] = 0` włącznie (8 linii).**
   Linie z `df` i `dane` (dawne 20–24) zostają razem i w tej samej kolejności.
4. **Zostaje `except ClientError`, nie `except Exception`.** Błędy sieci i brak kluczy i tak
   zatrzymują skrypt (sprawdzone 09.10), a nie mają w środku kodu odpowiedzi (przypadek E).
5. **Kod porównujesz z napisem `"404"` w cudzysłowie**, nie z liczbą `404` (przypadek D).
6. **W gałęzi „inny kod” stoi samo `raise`** — nie `print`, nie `poprzedni[t] = 0`. Uwaga: linia 39
   po zmianie (`poprzedni.get(spolka, 0)`) daje 0 dla spółki, której nie ma w słowniku, więc `print`
   zamiast `raise` po cichu odtworzyłby starą wadę (przypadek C).
7. **`else:` ma to samo wcięcie co `if`** (8 spacji), nie to samo co `except` (4 spacje) — inaczej
   Python czyta je jako zupełnie inną konstrukcję (przypadek B).
8. **Wcięcia:** `for` — 0 spacji, `try`/`except` — 4, `kod = …`/`if`/`else` — 8,
   `poprzedni[t] = 0`/`raise` — 12.
9. **`compaction.py` z prawdziwymi kluczami uruchamiasz tylko w porcji 4** (jeśli ją wybierzesz)
   i w listopadzie — nigdy jako „sprawdzę, czy działa”. Ten skrypt zapisuje do S3 i kasuje pliki.
   Nigdy między 17:55 a 18:35.
10. **Składnię sprawdzasz `python -m py_compile`**, nie uruchomieniem.
11. **Zmyślone klucze zawsze usuwasz po teście** i sprawdzasz `Get-ChildItem Env:AWS*` → nic.

---

## Część 3. Nowe pojęcia i przypadki (uruchomione 09.10)

Kod przykładu (`lody.py`). `stan_wczoraj(budka)` udaje pobranie pliku ze stanem z chmury:

```python
from botocore.exceptions import ClientError


def stan_wczoraj(budka):
    if budka == "Kraków":
        return 120
    if budka == "Gdańsk":
        raise ClientError({"Error": {"Code": "404", "Message": "Not Found"}}, "HeadObject")
    raise ClientError({"Error": {"Code": "403", "Message": "Forbidden"}}, "HeadObject")


stany = {}
for budka in ["Kraków", "Gdańsk", "Poznań"]:
    try:
        stany[budka] = stan_wczoraj(budka)
    except ClientError as e:
        kod = e.response["Error"]["Code"]
        if kod == "404":
            stany[budka] = 0
        else:
            raise
print(stany)
```

Funkcja `stan_wczoraj` jest tylko po to, żeby udać chmurę — w projekcie jej miejsce zajmuje
prawdziwe `s3.download_file(...)`. Linijki `raise ClientError({...}, "HeadObject")` w niej
**nie przepisujesz** — tak tylko udaję odpowiedź S3.

### `ClientError` — S3 odpowiedziało „nie”

Wyjątek z biblioteki `botocore` (na niej stoi `boto3`). Znaczy: połączenie było, S3 odpowiedziało,
ale odmówiło. W środku jest kod odpowiedzi. Treść wyjątku ma zawsze ten sam kształt:
`An error occurred (KOD) when calling the OPERACJA operation: OPIS` — **w nawiasie stoi właśnie kod**.
`download_file` najpierw pyta S3 o plik operacją `HeadObject`, dlatego tę nazwę zobaczysz w błędzie.

| Co się stało | Kod | Opis |
|---|---|---|
| pliku nie ma | `404` | `Not Found` |
| brak dostępu, zły klucz | `403` | `Forbidden` |

Błędy sieci (`EndpointConnectionError` i podobne) i brak kluczy (`NoCredentialsError`) to **inny
rodzaj** wyjątku — `except ClientError` ich nie łapie (sprawdzone 09.10: `issubclass` → `False`).

### `except ClientError as e` — złapany wyjątek ma nazwę

Znasz z `control.py`, linia 48 (`except Exception as e`). Pod nazwą `e` jest cały złapany wyjątek.

### `e.response["Error"]["Code"]` — kod jako napis

`e.response` to zwykły słownik ze słownikiem w środku: `{"Error": {"Code": "404", "Message": "Not
Found"}, …}`. Dwa nawiasy kwadratowe po kolei — jak `dane["a"]["b"]`.
*Gdańsk: `e.response["Error"]["Code"]` → `'404'` (napis, z apostrofami); `e.response["Error"]["Message"]`
→ `'Not Found'`.*

### `raise` bez niczego — puść błąd dalej

Wewnątrz `except` samo słowo `raise` wyrzuca **ten sam** wyjątek jeszcze raz. Program zatrzymuje się
tak, jakby `try` nie było, a `Traceback` pokazuje miejsce, w którym błąd powstał.

### Przypadki (wszystkie uruchomione)

| # | Wariant | Wynik |
|---|---|---|
| A | dziś: `except ClientError:` → `stany[budka] = 0` | `Kraków 120`, `Gdańsk 0`, `Poznań 0` — Poznań kłamie |
| F | **po zmianie** (kod wyżej) | Kraków 120, Gdańsk 0, potem `Traceback`, ostatnia linia: `botocore.exceptions.ClientError: An error occurred (403) when calling the HeadObject operation: Forbidden`; `print(stany)` się nie wykonuje |
| B | `else:` z wcięciem 4 (równo z `except`) zamiast 8 | `py_compile` nie widzi błędu; bieg: `RuntimeError: No active exception to reraise` już przy **Krakowie**. Python czyta to jako `try … except … else` — `else` po `try` działa wtedy, gdy błędu **nie było**, a wtedy nie ma czego „puścić dalej” |
| C | `print("Błąd:", kod)` zamiast `raise`, a potem `stany.get(budka, 0)` | `Błąd: 403`, potem `Kraków 120`, `Gdańsk 0`, `Poznań 0` — skrypt idzie dalej, stara wada wraca po cichu |
| D | `if kod == 404:` (liczba) | już **Gdańsk** kończy się `Traceback` z `(404) … Not Found` — napis `"404"` nigdy nie równa się liczbie `404`, więc każdy brak pliku zatrzymuje |
| E | `except Exception as e` i błąd sieci | `AttributeError: 'EndpointConnectionError' object has no attribute 'response'` — błąd sieci nie ma kodu odpowiedzi |
| G | brak wcięcia pod `if` | `python -m py_compile` → `Sorry: IndentationError: expected an indented block after 'if' statement on line 18 (a.py, line 19)` |

### `python -m py_compile plik.py` — sprawdzenie składni bez uruchomienia

Python czyta plik i zamienia go na kod do wykonania, ale **niczego nie uruchamia**. Przy dobrej
składni nic nie wypisuje (kod wyjścia 0). Przy złej — jedna linia `Sorry: …Error: … (plik, line N)`.
Łapie błędy wcięć i literówki w składni; **nie łapie** złej kolejności linii ani przypadków B–E.
Przy okazji tworzy plik w `kod/__pycache__/` — jest w `.gitignore`, git go nie zobaczy.
*`lody.py` z przypadku G → `Sorry: IndentationError: …`; poprawny `lody.py` → nic.*

---

## Część 4. Przykład → projekt

| Przykład | Projekt (`kod/compaction.py`, numery **po** zmianie) |
|---|---|
| `stany = {}` | `poprzedni = {}`, linia 20 |
| `for budka in [...]` | `for t in ticker:`, linia 21 |
| `stany[budka] = stan_wczoraj(budka)` | `s3.download_file(...)` i `poprzedni[t] = len(...)`, linie 24–25 |
| `except ClientError as e:` | linia 26, 4 spacje |
| `kod = …` | linia 27, 8 spacji |
| `if kod == "404":` | linia 28, 8 spacji |
| `stany[budka] = 0` | `poprzedni[t] = 0`, linia 29, 12 spacji |
| `else:` | linia 30, 8 spacji |
| `raise` | linia 31, 12 spacji |
| — | `df = pd.read_sql(…)` przenosi się z 20 na 32; `nowe = …` z 33 na 37; `assert` z 37 na 41 |

Plik po zmianie: **58 linii** (dziś 54). `git diff --stat` (policzone na kopii): `1 file changed,
11 insertions(+), 7 deletions(-)` — przeniesienie pięciu linii `df`/`dane` git liczy jako 5 usuniętych
i 5 dodanych.

---

## Część 5. Porcje krok po kroku

### Porcja 1 — jakie kody daje S3 (laptop)

Przewidywania: krok 3 → `(404)` i `Not Found`, bo z laptopa działa `aws s3 ls`, czyli masz prawo
listować bucket (bez niego S3 na brak pliku odpowiada `403`); krok 7 → `(403)` i `Forbidden`.
Plik `proba.parquet` nie powstanie w żadnym z kroków.

1. **PRZEŁĄCZENIE** [lokalny PowerShell, nowe okno, venv nieistotne] — wiersz kończy się na `GPW - pulse>`.
   `cd "C:\Users\gracj\OneDrive\Dokumenty\DE\GPW - pulse"`
2. **PRZEŁĄCZENIE** [lokalny PowerShell, włączenie venv] — wiersz zaczyna się od `(.venv)`.
   `.venv\Scripts\Activate.ps1`
3. [lokalny PowerShell, (.venv) włączone] — `Traceback`, ostatnia linia z `(404)` i `Not Found`.
   `python -c "import boto3; boto3.client('s3').download_file('gpw-tracker-bucket', 'bronze/spolka=NIEMA.WA/NIEMA.WA.parquet', 'proba.parquet')"`
4. [lokalny PowerShell, (.venv) włączone] — `False`.
   `Test-Path proba.parquet`
5. [lokalny PowerShell, (.venv) włączone] — nic nie wypisuje.
   `$env:AWS_ACCESS_KEY_ID = "AKIAZMYSLONY00000000"`
6. [lokalny PowerShell, (.venv) włączone] — nic nie wypisuje.
   `$env:AWS_SECRET_ACCESS_KEY = "zmyslony"`
7. [lokalny PowerShell, (.venv) włączone] — `Traceback`, ostatnia linia z `(403)` i `Forbidden`.
   `python -c "import boto3; boto3.client('s3').download_file('gpw-tracker-bucket', 'bronze/spolka=CBF.WA/CBF.WA.parquet', 'proba.parquet')"`
8. [lokalny PowerShell, (.venv) włączone] — nic.
   `Remove-Item Env:AWS_ACCESS_KEY_ID`
9. [lokalny PowerShell, (.venv) włączone] — nic.
   `Remove-Item Env:AWS_SECRET_ACCESS_KEY`
10. [lokalny PowerShell, (.venv) włączone] — nic (żadnej zmiennej `AWS…`).
    `Get-ChildItem Env:AWS*`
11. [lokalny PowerShell, (.venv) włączone] — `False`.
    `Test-Path proba.parquet`

**Wynik porcji 1 (09.10):** krok 3 → `An error occurred (404) when calling the HeadObject operation:
Not Found`; krok 7 → `(403) … Forbidden`; `Test-Path` 2 × `False`; `Get-ChildItem Env:AWS*` pusto.
Zgodne z przewidywaniem. Warunek `kod == "404"` patrzy więc na właściwy kod, a nowa spółka nie
będzie blokowana.

### Porcja 2 — zmiana w pliku

1. **PRZEŁĄCZENIE** [lokalny PowerShell, okno z porcji 1, (.venv) włączone] — wiersz `(.venv) PS …\GPW - pulse>`.
   `cd "C:\Users\gracj\OneDrive\Dokumenty\DE\GPW - pulse"`
2. VS Code, `kod/compaction.py`: 54 linie; linia 20 `df = pd.read_sql(…`, linia 25 `poprzedni = {}`,
   linia 32 `        poprzedni[t] = 0`, linia 33 `nowe = …`.
3. Kliknij na samym początku linii 25, przytrzymaj Shift i kliknij na samym początku linii 33
   (przed `nowe`). Zaznaczone 8 pełnych linii.
4. Ctrl+X. Teraz linia 25 to `nowe = dane.groupby("spolka").size()`, plik ma 46 linii.
5. Kliknij na samym początku linii 20 (`df = pd.read_sql(…`) i Ctrl+V. Teraz linia 20 to
   `poprzedni = {}`, linia 27 `        poprzedni[t] = 0`, linia 28 `df = pd.read_sql(…`; 54 linie.
6. Linia 26 (`    except ClientError:`): nadaj złapanemu wyjątkowi nazwę `e`, jak w przykładzie.
   Dwukropek zostaje na końcu.
7. Kursor na końcu linii 26, Enter — VS Code sam wstawi 8 spacji. Wpisz zmienną `kod` z kodem
   odpowiedzi z `e` (jak `kod = …` w przykładzie).
8. Kursor na końcu linii 27, Enter (8 spacji). Wpisz warunek: `kod` równy napisowi `"404"`,
   dwukropek na końcu.
9. Linia 29 (`        poprzedni[t] = 0`, 8 spacji): kursor na samym początku linii, Tab —
   ma mieć 12 spacji (w pasku na dole VS Code ma być `Spaces: 4`).
10. Kursor na końcu linii 29, Enter (VS Code wstawi 12 spacji), raz Backspace (zostaje 8), wpisz
    `else:`.
11. Kursor na końcu linii 30, Enter (12 spacji), wpisz samo `raise`.
12. Ctrl+S. Ma być: 58 linii; linie 20–31 kształtem jak przykład z lodami (Część 4); linia 32
    `df = pd.read_sql(…`; linia 37 `nowe = …`; linia 41 `assert …`.
13. [lokalny PowerShell, (.venv) włączone] — nic nie wypisuje.
    `python -m py_compile kod/compaction.py`
14. Napisz mi „gotowe” i wklej wynik kroku 13. Diff przeczytam sam.

### Porcja 3 — ścieżka błędu na prawdziwym skrypcie

Przewidywania: krok 7 kończy się `Traceback`, w nim linia `File "…\kod\compaction.py", line 24, in
<module>`, ostatnia linia `botocore.exceptions.ClientError: An error occurred (403) when calling the
HeadObject operation: Forbidden`. **Nie ma** linii `stara ilosc`, `Usunięto`, `Failed to execute
query` — do Atheny skrypt nie dochodzi. Kroki 11–13 dają to samo co 2–4.

Liczby na kroki 2–4 podam przed porcją (zależą od godziny: po biegu o 18:00 w `live/` przybywają
3 pliki). Stan znany: `bronze\poprzedni` — 3 pliki z 03.10.2026 10:56 (CBF 9079 B, SNT 10029 B,
XTB 10889 B).

1. **PRZEŁĄCZENIE** [lokalny PowerShell, (.venv) włączone] — wiersz `(.venv) PS …\GPW - pulse>`.
2. `aws s3 ls s3://gpw-tracker-bucket/bronze/ --recursive` — 3 pliki; zapisz daty i rozmiary.
3. `aws s3 ls s3://gpw-tracker-bucket/live/ --recursive --summarize` — zapisz `Total Objects`.
4. `Get-ChildItem bronze\poprzedni` — 3 pliki z 03.10.2026 10:56.
5. `$env:AWS_ACCESS_KEY_ID = "AKIAZMYSLONY00000000"`
6. `$env:AWS_SECRET_ACCESS_KEY = "zmyslony"`
7. `python kod/compaction.py` — patrz przewidywania.
8. `Remove-Item Env:AWS_ACCESS_KEY_ID`
9. `Remove-Item Env:AWS_SECRET_ACCESS_KEY`
10. `Get-ChildItem Env:AWS*` — nic.
11–13. Kroki 2–4 jeszcze raz — bez zmian.

(Przy podawaniu porcji 3 każda komenda dostanie osobne okienko i etykietę.)

**Wynik porcji 2 (09.10, ok. 12:15):** `git diff --stat` → `1 file changed, 11 insertions(+), 7
deletions(-)`, plik 58 linii, skrót gita `789612a` taki sam jak kopii wzorcowej w brudnopisie Claude'a
(plik identyczny co do znaku). `python -m py_compile` → nic.

**Wynik porcji 3 (09.10, ok. 12:20) — wszystko zgodne z przewidywaniem:**
- przed i po biegu identycznie: `bronze/` 3 pliki z `2026-10-03 10:56:04–05` (CBF 9285 B, SNT
  10253 B, XTB 11147 B — przewidziane: większe od lokalnych kopii, poniżej 12 000 B); `live/`
  `Total Objects: 18`, `Total Size: 1531`; `bronze\poprzedni` 3 pliki z 3.10.2026 10:56 (9079 /
  10029 / 10889 B);
- bieg ze zmyślonymi kluczami: `Traceback`, pierwsza ramka `kod\compaction.py", line 24, in <module>`
  (`s3.download_file(…)`), ostatnia linia `botocore.exceptions.ClientError: An error occurred (403)
  when calling the HeadObject operation: Forbidden`; żadnej linii `stara ilosc`, `Usunięto`,
  `Failed to execute query`;
- `Get-ChildItem Env:AWS*` po teście — pusto.

Stan warunków „zrobione”: (a) ścieżka błędu na prawdziwym skrypcie ✅; (b) przewidziane przed
biegiem, potwierdzone ✅; (c) głośno — `Traceback` na ekranie, nic nie zapisane ✅; (d) zwykła droga
nowego kodu jeszcze nie uruchomiona — porcja 4 albo listopad; (e) README przy dużej dokumentacji.

---

## Część 6. Błędy, które możesz zobaczyć, i co znaczą

| Co widzisz | Co to znaczy |
|---|---|
| `py_compile` → `Sorry: IndentationError: expected an indented block after 'if' statement …` | pod `if` brak wcięcia 12 spacji (przypadek G) |
| `py_compile` → `Sorry: IndentationError: unindent does not match any outer indentation level (…, line N)` | linia N ma wcięcie, którego nie ma żadna linia wyżej, np. `else:` z 6 spacjami albo `kod = …` z 9 (oba uruchomione 09.10). Uwaga: **głębsze** wcięcie pod `if`/`else` (np. 10 spacji zamiast 12) `py_compile` przepuszcza — działa, ale odstaje od reszty pliku; zobaczę to w diffie |
| porcja 3: `RuntimeError: No active exception to reraise` | `else:` z wcięciem 4 zamiast 8 (przypadek B) — `py_compile` tego nie łapie |
| porcja 3: `NameError: name 's3' is not defined` | blok wklejony nad `s3 = boto3.client("s3")` (zasada 2) |
| porcja 3: `NameError: name 'dane' is not defined` | `nowe = …` znalazło się nad liniami `dane = …` — przeniesiono za dużo albo za mało |
| porcja 3: `Failed to execute query.` i błąd Atheny (`UnrecognizedClientException`) zamiast `(403) … HeadObject` | pobranie dalej stoi **za** zapytaniem do Atheny (kolejność bez zmian) albo `except` dalej zamienia każdy błąd na 0 |
| porcja 3: `AttributeError: … has no attribute 'response'` | `except Exception` zamiast `except ClientError` (przypadek E) |
| porcja 1, krok 3: `(403)` zamiast `(404)` | konto nie ma prawa listowania bucketu — zatrzymaj się i wklej wynik: wtedy „nie ma pliku” wygląda jak „brak dostępu” i nowa spółka byłaby blokowana |
| porcja 1, krok 7: **brak** `Traceback`, a krok 11 → `True` | zmyślone klucze nie zadziałały (zmienne nieustawione), więc prawdziwy plik CBF pobrał się jako `proba.parquet`. Nic się nie zepsuło (to tylko pobranie); usuń go `Remove-Item proba.parquet` i wklej mi wynik `Get-ChildItem Env:AWS*` |
| `ModuleNotFoundError: No module named 'boto3'` | `(.venv)` nie jest włączone |
| porcja 3: wypisało `stara ilosc` albo `Usunięto` | **skrypt połączył się z prawdziwym S3** — zmyślone klucze nieustawione. Zatrzymaj się i wklej wynik, nic więcej nie uruchamiaj |

---

## Część 7. Do decyzji: próba generalna w październiku (porcja 4)

**Co:** zwykły bieg `python kod/compaction.py` z prawdziwymi kluczami, na laptopie, po porcji 3,
nie między 17:55 a 18:35.

**Dlaczego nic nie zmieni w danych:** granica to 1.10. `bronze` ma dane do 30.09 (783 dni na
spółkę), a w `live/` są tylko pliki z października (wrześniowe skasowała kompakcja 03.10).
Przewidywania: 3 × `stara ilosc: 783, nowa_ilosc: 783` (CBF, XTB, SNT), `Usunięto 0 plików`; pliki
w `bronze/` nadpisane tą samą treścią (nowa godzina, rozmiar najpewniej ten sam — nie sprawdzone);
`live/` bez zmian; w `bronze\poprzedni` kopia z dziś zamiast z 03.10. Wieczorny Silver i Gold:
`(M, 3)` jak w tabeli przewidywań — to dowód, że `bronze` po próbie czyta się tak samo.

**Koszt:** prawdziwy zapis do S3 poza zwykłym terminem; kopia sprzed kompakcji 03.10 (761 wierszy
na spółkę) zostanie nadpisana — od 03.10 niepotrzebna (Athena potwierdziła 785 × 3 przed i po).

- **(a) zrobić** — listopad nie będzie pierwszym biegiem nowego kodu; spełnia warunek (d) już teraz;
- (b) nie robić — zwykła droga sprawdzona dopiero na początku listopada.

Rekomendacja: (a). **Decyzja Gracjana 09.10: (a).**

**Wynik porcji 4 (09.10, `Get-Date` 12:27:22) — wszystko zgodne z przewidywaniem:**
- `Get-ChildItem Env:AWS*` przed biegiem — pusto;
- `python kod/compaction.py`: ostrzeżenie `UserWarning` (SQLAlchemy) z `compaction.py:32` (2 linie),
  3 × `stara ilosc: 783, nowa_ilosc: 783` (CBF, XTB, SNT), ostrzeżenie z `compaction.py:49` (2 linie),
  `Usunięto 0 plików`; bez `Traceback`;
- `bronze/` w S3: 3 pliki z `2026-10-09 12:27:31`, rozmiary **te same** co przed (9285 / 10253 /
  11147 B) — przewidziane jako „najpewniej”;
- `live/`: `Total Objects: 18`, `Total Size: 1531` — bez zmian;
- `bronze\poprzedni`: 9.10.2026 12:27, 9285 / 10253 / 11147 B — kopia stanu S3 sprzed próby.

Warunek (d) spełniony na laptopie, jedynym miejscu, gdzie kompakcja działa. Zostaje: wieczorem
`(2370, 3)` w Silverze i Goldzie (dowód, że `bronze` po próbie czyta się tak samo) i (e) — README.
