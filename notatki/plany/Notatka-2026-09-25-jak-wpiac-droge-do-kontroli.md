# Notatka 25.09: jak wpiąć test drogi do skryptu kontrolnego (wszystko w jednym miejscu)

To instrukcja do etapu A z [[Notatka-2026-09-24-droga-na-ec2]]. Etap A to kod i sprawdzenia na
laptopie. Decyzje zatwierdzone 25.09, wszystkie w wariancie (a). Tutaj masz **wszystko**, czego
potrzebujesz: kroki, zasady, nowe pojęcia z wejściem i wyjściem, przypadki z wynikami i tabelę
błędów. Przy ocenie Twojego kodu odwołuję się tylko do tej notatki. Jeśli czegoś w niej zabraknie,
powiem to wprost i dopiszę.

Przykład to lodziarnia z trzema smakami, a nie spółki. **Każdy wynik z lodziarni pochodzi
z uruchomienia 25.09.** Kształt docelowego kodu sprawdziłem też na kopii folderu `kod/`
w katalogu roboczym Claude'a, poza projektem. `pytest` na obu plikach testów dał tam
`18 passed in 0.69s`. Twoich plików nie ruszałem.

---

## Część 1. Kroki (po jednej linii, szczegóły niżej)

1. `kod/path.py`: w `sprawdz_daty` dopisz czwarte sprawdzenie („spółka bez ani jednego wiersza”) tuż przed `return problemy`.
2. `kod/test_path.py`: dopisz siódmy test (sobota, pierwszej spółki brak w całej tabeli), a potem uruchom `pytest`. Ma być `7 passed`.
3. `kod/path.py`: między `sprawdz_daty` a `if __name__` dopisz funkcję `pobierz_dane()` i przenieś do niej połączenie i `SELECT`.
4. `kod/path.py`: w `__main__` zostaw jedno `df = pobierz_dane()` zamiast połączenia, a potem uruchom `python kod/path.py`. Ma być liczba wierszy i `Dane: OK`.
5. `kod/control.py`: pod `from datetime import date` dopisz `from path import sprawdz_daty, pobierz_dane`.
6. `kod/control.py`: pod `blad = sprawdz_blok(...)` zamień datę na obiekt `date` i dopisz wewnętrzny `try` z `pobierz_dane`.
7. Uruchom `pytest` na obu plikach testów. Ma być `18 passed`, poniżej sekundy.
8. Dwa ręczne biegi `control.py` na bloku z 18.09: najpierw z prawdziwymi kluczami, potem ze zmyślonymi (Część 7).
9. Commit i `git push`.

---

## Część 2. Zasady, wszystkie naraz

1. **Czwarte sprawdzenie idzie na koniec funkcji**, tuż przed `return`. Działa **zawsze**, także
   w weekend, czyli nie wchodzi pod `if dzis.weekday() < 5`.
2. **Lista „kogo oczekujemy” to `spolki`** (parametr funkcji), a „kogo mamy” to
   `df["spolka"].tolist()`. Tego samego `.tolist()` używasz już w linii 11.
3. **Treść problemu zaczyna się od nazwy spółki**, np. `f"{t}: brak w tabeli"`. Test sprawdza
   `ticker[0] in wynik[0]`.
4. **`pobierz_dane()` nie ma parametrów i kończy się `return df`.** Bez `return` funkcja oddaje
   `None` (Część 3, przypadek F).
5. **Połączenie z Atheną stoi wyłącznie w środku `pobierz_dane()`.** Poza funkcją zostają same
   importy (`connect`, `WYNIKI_ATHENY` itd.), a import niczego nie łączy. Gdyby połączenie stało
   poza funkcją i poza `__main__`, każdy `import path`, także ten w `pytest` i w `control.py`,
   łączyłby się z Atheną.
6. **Funkcja `pobierz_dane` stoi nad `if __name__ == "__main__":`**, obok `sprawdz_daty`.
   Python czyta plik z góry na dół, więc funkcja musi być zdefiniowana, zanim ktoś ją wywoła.
7. **W `control.py` importujesz z `path` dwie funkcje**, a `ticker` masz już z `config`.
8. **Datę zamieniasz z napisu na `date` przed wewnętrznym `try`**:
   `dzis = date.fromisoformat(KONTROLA_DATA)`. `sprawdz_blok` dalej dostaje **napis**
   `KONTROLA_DATA` (bez zmian), a `sprawdz_daty` dostaje **datę** `dzis`. Dlaczego przed `try`:
   przypadki E i G w Części 3.
9. **Wewnętrzny `try` obejmuje trzy rzeczy:** `pobierz_dane()`, linię z liczbą wierszy i dopisanie
   problemów z `sprawdz_daty`. Jego `except` dopisuje do `blad` **jeden** problem zaczynający się
   od `Athena: błąd - `. Nie ma w nim ani `print`, ani `sys.exit`.
10. **Linia z liczbą wierszy zaczyna się od `Kontrola:`**, np. `Kontrola: dane 2340 wierszy`.
    Dzięki temu `wytnij_blok` odsieje ją przy drugim biegu tego samego dnia, tak jak dziś odsiewa
    `Kontrola: OK`.
11. **Listy skleja się przez `+`:** `blad = blad + sprawdz_daty(...)`. Tak samo jak `SMAKI * 2 + [...]`
    w testach.
12. **Reszty `control.py` nie ruszasz.** `if blad:`, `tekst`, `print(tekst)`, wysyłka do stróża
    i zewnętrzny `except` zostają słowo w słowo, bo wszystkie działają już na nowej, dłuższej
    liście `blad`.

---

## Część 3. Nowe pojęcia i przypadki (uruchomione 25.09)

Pliki przykładu:
- `lodziarnia.py` zawiera `sprawdz_zeszyt`, czyli Twój `sprawdz_daty` słowo w słowo plus czwarte
  sprawdzenie, oraz `pobierz_zeszyt`;
- `kontrola_lodziarni.py` to odpowiednik `control.py`.

W zeszycie jest 6 wierszy: każdy smak ma 24.09 i 25.09. Raport sprzedawcy to
`Raport z 2026-09-25`. Kalendarz: 24.09 czwartek, 25.09 piątek, 26.09 sobota, 28.09 poniedziałek.

### Czwarte sprawdzenie

```python
    obecne = df["spolka"].tolist()
    for t in spolki:
        if t not in obecne:
            problemy.append(f"{t}: brak w tabeli")
    return problemy
```

`t not in obecne` znaczy „tego smaku nie ma na liście”. Wejście i wyjście w teście poniżej:
zeszyt bez wanilii, sobota.

```python
def test_brak_smaku_w_sobote():
    zeszyt = pd.DataFrame({
        "spolka": SMAKI[1:] * 2,
        "data": ["2026-09-24 17:00:00"] * (len(SMAKI) - 1) + ["2026-09-25 17:00:00"] * (len(SMAKI) - 1)})
    wynik = sprawdz_zeszyt(zeszyt, SMAKI, date(2026, 9, 26))
    assert len(wynik) == 1
    assert SMAKI[0] in wynik[0]
```
Tabela i wynik (z `-s`):
```
       spolka                 data       dzien
0   czekolada  2026-09-24 17:00:00  2026-09-24
1  pistacjowy  2026-09-24 17:00:00  2026-09-24
2   czekolada  2026-09-25 17:00:00  2026-09-25
3  pistacjowy  2026-09-25 17:00:00  2026-09-25
['wanilia: brak w tabeli']
PASSED
```
Przejście przez cztery sprawdzenia:
- sprawdzenie 1: jest sobota, więc nie działa;
- sprawdzenie 2: nic po 26.09;
- sprawdzenie 3: dwa smaki po 2 dni, więc `nunique` = 1 i brak problemu, bo wanilii nie ma w `groupby`;
- sprawdzenie 4: wanilii brak, więc **1 problem**.

**Bez czwartego sprawdzenia ten sam test dałby `[]`**, czyli „OK”. To jest właśnie luka z decyzji 6.

**Uwaga na dzień roboczy:** gdyby spółki brakowało w całej tabeli we wtorek, odezwą się
sprawdzenia 1 **i** 4, czyli 2 problemy. To nie jest błąd, tylko dwa opisy jednej dziury. Sześć
Twoich dotychczasowych testów tego nie dotyka, bo w każdym wszystkie spółki mają choć jeden
wiersz. Dalej przechodzą.

### Funkcja bez parametrów, która oddaje tabelę

```python
def pobierz_zeszyt():
    zeszyt = pd.read_csv("zeszyt.csv")
    return zeszyt
```
Puste nawiasy `()` znaczą, że funkcja niczego nie potrzebuje z zewnątrz. Wywołanie też ma puste
nawiasy: `pobierz_zeszyt()`. Wejście to plik z 6 wierszami, wyjście to tabela, a
`len(pobierz_zeszyt())` daje `6`.

W `lodziarnia.py` część `__main__` wygląda tak:
```python
if __name__ == "__main__":
    df = pobierz_zeszyt()
    print(len(df))
    wynik = sprawdz_zeszyt(df, SMAKI, date.fromisoformat(os.environ.get("LODY_DATA", str(date.today()))))
```
W projekcie w miejscu `pd.read_csv(...)` stoją Twoje linie `con = connect(...)`
i `pd.read_sql(...)`. Przenosisz je **w całości** do środka funkcji, z wcięciem o 4 spacje.

### `try` w środku `try`

Najważniejszy fragment `kontrola_lodziarni.py`:
```python
        blad = sprawdz_raport(raport, LODY_DATA)
        dzis = date.fromisoformat(LODY_DATA)
        try:
            zeszyt = pobierz_zeszyt()
            print(f"Kontrola: zeszyt {len(zeszyt)} wierszy")
            blad = blad + sprawdz_zeszyt(zeszyt, SMAKI, dzis)
        except Exception as e:
            blad.append(f"Zeszyt: błąd - {e}")
        if blad:
            ...
```
Wewnętrzny `try` łapie tylko błąd ze swojego kawałka, zamienia go na zwykły problem i program idzie
dalej, do `if blad:` i do wysyłki. Zewnętrzny `try` (ten, który już masz w `control.py`) zostaje
na całą resztę, np. brak pliku z logiem.

### Osiem przypadków, każdy z wyjściem

| # | Przypadek | Wyjście |
|---|---|---|
| A | piątek 25.09, wszystko jest | `Kontrola: zeszyt 6 wierszy`<br>`Kontrola: OK`<br>`Kontrola: brak adresu szefa` |
| B | udawany poniedziałek 28.09 | `Kontrola: zeszyt 6 wierszy`<br>`Kontrola: AWARIA - Brak raportu z 2026-09-28; wanilia brak wpisu z: 2026-09-28; czekolada brak wpisu z: 2026-09-28; pistacjowy brak wpisu z: 2026-09-28`<br>`Kontrola: brak adresu szefa` |
| C | udawany czwartek 24.09 (dzień wstecz) | `Kontrola: zeszyt 6 wierszy`<br>`Kontrola: AWARIA - Brak raportu z 2026-09-24; wanilia: wpis z przyszłości: 2026-09-25, dziś jest: 2026-09-24; czekolada: …; pistacjowy: …`<br>`Kontrola: brak adresu szefa` |
| D | piątek, pliku zeszytu nie ma (odpowiednik „Athena nie odpowiada”) | `Kontrola: AWARIA - Zeszyt: błąd - [Errno 2] No such file or directory: 'zeszyt.csv'`<br>`Kontrola: brak adresu szefa` |
| E | zła data `25.09.2026` | `Kontrola: Błąd skryptu - Invalid isoformat string: '25.09.2026'`, kod wyjścia 1 |
| F | `pobierz_zeszyt` bez `return` | `Kontrola: AWARIA - Zeszyt: błąd - object of type 'NoneType' has no len()` |
| G | do `sprawdz_zeszyt` podany napis `LODY_DATA` zamiast `dzis` | `Kontrola: zeszyt 6 wierszy`<br>`Kontrola: AWARIA - Zeszyt: błąd - 'str' object has no attribute 'weekday'` |
| H | sobota 26.09, zeszyt pusty (sam nagłówek) | `Kontrola: zeszyt 0 wierszy`<br>`Kontrola: AWARIA - Brak raportu z 2026-09-26; wanilia: brak w tabeli; czekolada: brak w tabeli; pistacjowy: brak w tabeli` |

Czego uczą przypadki:
- **D.** Raport był dobry, zeszyt się nie otworzył, a wynik i tak wyszedł jako zwykła awaria z powodem.
  Brakuje linii `zeszyt N wierszy`, bo program nie dotarł do `print`. Tak ma wyglądać bieg ze
  zmyślonymi kluczami AWS (Część 7).
- **E i G razem pokazują, dlaczego data zamienia się przed wewnętrznym `try` (zasada 8).** Zła data
  przed `try` daje uczciwy `Błąd skryptu`. Błąd typu w środku `try` przebiera się za „błąd zeszytu”,
  a w projekcie wyglądałby jak `Athena: błąd - …`, choć Athena działała. Wtedy szukałbyś usterki
  w złym miejscu.
- **F.** Brak `return` też przebiera się za awarię zeszytu. W projekcie wyszłoby
  `Athena: błąd - object of type 'NoneType' has no len()`. Zapamiętaj ten tekst: to Twój błąd w kodzie,
  a nie Athena.
- **H.** To luka z decyzji 6, już zamknięta. Bez czwartego sprawdzenia pusta sobota dałaby
  `Kontrola: OK`.

### Skąd `boto3` bierze klucze (do testu z awarią Atheny)

Pod spodem `pyathena` używa `boto3`. `boto3` szuka kluczy w ustalonej kolejności i bierze
**pierwsze**, które znajdzie:
1. zmienne środowiskowe `AWS_ACCESS_KEY_ID` i `AWS_SECRET_ACCESS_KEY`;
2. plik `~/.aws/credentials` (tak działa laptop);
3. rola maszyny (tak działa EC2).

Jeśli ustawisz zmyślone wartości w zmiennych, `boto3` weźmie je jako pierwsze, a AWS je odrzuci.
Kod się nie zmienia, plik z kluczami też. Zmienne znikają po `Remove-Item Env:…` albo po
zamknięciu okna. **Tego przypadku nie uruchamiałem**, bo nie dotykam AWS. Przewidywanie
w Części 7.

### Kolejność linii w logu (dla etapu B, na EC2)

Na EC2 `cron` kieruje wszystko do pliku. Ostrzeżenia idą przez `stderr`, który pisze od razu.
`print` idzie przez `stdout`, który przy pisaniu do pliku czeka w buforze do końca programu.
Widzieliśmy to 19.09. Dlatego w logu dwie linie `UserWarning` o SQLAlchemy staną **nad**
wszystkimi liniami `Kontrola:`, a `Kontrola: OK` zostanie ostatnia. Na laptopie, w oknie
PowerShella, linie mogą wyjść w innej kolejności, bo tam `print` nie czeka. To nie jest błąd.

---

## Część 4. Przykład → projekt

| Lodziarnia | Projekt |
|---|---|
| `sprawdz_zeszyt` | `sprawdz_daty` w `kod/path.py` |
| `SMAKI`, `SMAKI[0]`, `SMAKI[1:]` | `ticker`, `ticker[0]`, `ticker[1:]` (z `config`) |
| `test_brak_smaku_w_sobote` | siódmy test w `kod/test_path.py` (nazwa Twoja, zaczyna się od `test_`) |
| `pobierz_zeszyt()` z `pd.read_csv` | `pobierz_dane()` z `connect(...)` i `pd.read_sql("SELECT spolka, data FROM gold_dane_dzienne", con)` |
| `from lodziarnia import sprawdz_zeszyt, pobierz_zeszyt` | `from path import sprawdz_daty, pobierz_dane` |
| `sprawdz_raport(raport, LODY_DATA)` | `sprawdz_blok(blok, ticker, KONTROLA_DATA)` (bez zmian) |
| `LODY_DATA` | `KONTROLA_DATA` |
| `dzis = date.fromisoformat(LODY_DATA)` | `dzis = date.fromisoformat(KONTROLA_DATA)` |
| `Kontrola: zeszyt N wierszy` | `Kontrola: dane N wierszy` |
| `Zeszyt: błąd - {e}` | `Athena: błąd - {e}` |
| `Kontrola: brak adresu szefa` | `Kontrola: brak adresu stróża` (już jest w `control.py`) |

Nazwy zmiennych (`dzis`, `dane`, `zeszyt`) wybierasz sam. Stałe są tylko słowa `Kontrola:`
i `Athena: błąd` na początku linii, bo od nich zależą odsiew i przewidywania.

---

## Część 5. Błędy, które możesz zobaczyć, i co znaczą

| Co widzisz | Przyczyna | Zasada |
|---|---|---|
| `ImportError: cannot import name 'pobierz_dane' from 'path'` | literówka w nazwie albo funkcja jeszcze niedopisana | 7 |
| `NameError: name 'pobierz_dane' is not defined` w `path.py` | funkcja stoi **pod** `__main__` albo wywołanie ma inną nazwę niż definicja | 6 |
| `Athena: błąd - object of type 'NoneType' has no len()` | brak `return df` w `pobierz_dane` (przypadek F) | 4 |
| `Athena: błąd - 'str' object has no attribute 'weekday'` | do `sprawdz_daty` poszedł napis zamiast `dzis` (przypadek G) | 8 |
| `Kontrola: Błąd skryptu - Invalid isoformat string` | zły format `KONTROLA_DATA`, poprawny to `RRRR-MM-DD` (przypadek E) | 8 |
| `pytest` trwa kilka sekund albo pokazuje ostrzeżenie SQLAlchemy | połączenie stoi poza `pobierz_dane()` | 5 |
| `IndentationError` | linie przeniesione do `pobierz_dane` bez wcięcia o 4 spacje | Część 3 |
| `TypeError: can only concatenate list (not "str") to list` | `blad + "tekst"` zamiast `blad.append("tekst")` | 9, 11 |
| `assert 0 == 1` w siódmym teście | czwarte sprawdzenie jest pod `if dzis.weekday() < 5` albo nie ma go wcale | 1 |
| `assert 0 == 1` w siódmym teście, choć wcięcie dobre | warunek `if t not in spolki` (lista porównana sama ze sobą) albo `if t not in df["spolka"]` bez `.tolist()`, a `in` na kolumnie pandas sprawdza **numery wierszy**: `'czekolada' in df['spolka']` → `False`, `0 in df['spolka']` → `True` (sprawdzone 25.09; dopisane po pytaniu Gracjana) | 2 |
| `assert 2 == 1` w siódmym teście | dane testu mają w sobotę inną liczbę dni u spółek albo datę z przyszłości | Część 3 |
| dwie linie `UserWarning … SQLAlchemy` | ostrzeżenie, nie błąd; znane z Silvera | — |

---

## Część 6. Uruchomienie testów i `path.py`

**1. [lokalny PowerShell, venv nieistotne]** Przejdź do folderu projektu.
```powershell
cd "C:\Users\gracj\OneDrive\Dokumenty\DE\GPW - pulse"
```
Ma być: wiersz kończy się na `GPW - pulse>`.

**2. [lokalny PowerShell]** Włącz środowisko.
```powershell
.\.venv\Scripts\Activate.ps1
```
Ma być: `(.venv)` na początku wiersza.

**3. [lokalny PowerShell, (.venv) włączone]** Po krokach 1–2 z Części 1.
```powershell
pytest kod/test_path.py -v
```
Ma być: `7 passed`.

**4. [lokalny PowerShell, (.venv) włączone]** Po krokach 3–4 z Części 1.
```powershell
python kod/path.py
```
Ma być: dwie linie `UserWarning`, potem liczba wierszy, potem `Dane: OK`. Liczba wierszy to
3 × liczba dni: **2340** od 25.09 wieczorem do niedzieli 27.09, a **2343** w poniedziałek 28.09 po 18:10.
Przed 18:10 w dzień giełdowy wyjdzie `Dane: Problem - … brak wpisu z: <dziś>`. To nie jest usterka,
tylko za wcześnie.

**5. [lokalny PowerShell, (.venv) włączone]** Po krokach 5–6 z Części 1.
```powershell
pytest kod/test_path.py kod/test_control.py -v
```
Ma być: `18 passed`, poniżej sekundy (na kopii 0.69 s).

---

## Część 7. Ręczne biegi `control.py` na laptopie

Oba biegi czytają prawdziwy blok z 18.09, a nie dzisiejszy log. `STROZ_URL` na laptopie nie
istnieje, więc nic nie poleci do stróża. Przed biegami sprawdź, czy okno nie ma starych zmiennych.

**1. [lokalny PowerShell, (.venv) włączone]** Pokaż zmienne, które mogą zostać z poprzednich sesji.
```powershell
Get-ChildItem Env: | Where-Object Name -Match "KONTROLA|STROZ|DROGA|AWS"
```
Ma być: nic. W środowisku, z którego korzystam, 25.09 żadnej z tych zmiennych nie było. Jeśli
coś się wypisze, najpierw wklej mi to i niczego nie usuwaj: zmienna `AWS_…` może służyć czemuś
innemu.

**2. [lokalny PowerShell, (.venv) włączone]** Wskaż plik z blokiem z 18.09.
```powershell
$env:KONTROLA_LOG = "kod\dane_testowe\blok_2026-09-18.txt"
```
Ma być: brak wyniku.

**3. [lokalny PowerShell, (.venv) włączone]** Udawany dzień: 18.09.
```powershell
$env:KONTROLA_DATA = "2026-09-18"
```
Ma być: brak wyniku.

**4. [lokalny PowerShell, (.venv) włączone]** Bieg 1, prawdziwe klucze.
```powershell
python kod/control.py
```
Przewidywanie:
- dwie linie `UserWarning` z `kod\path.py`;
- `Kontrola: dane 2340 wierszy` (albo 2343 od 28.09 po 18:10);
- `Kontrola: AWARIA - ` i **3** problemy `…: wpis z przyszłości: 2026-09-25, dziś jest: 2026-09-18`,
  po jednym na spółkę, w dowolnej kolejności (od 28.09 z datą `2026-09-28`);
- `Kontrola: brak adresu stróża`.

Log z 18.09 jest czysty, więc problemów z logu nie będzie. `Różna liczba dni` i `brak w tabeli`
też nie wyjdą, bo każda spółka ma po tyle samo dni.

**5. [lokalny PowerShell, (.venv) włączone]** Zmyślony klucz.
```powershell
$env:AWS_ACCESS_KEY_ID = "AKIAFALSZYWYKLUCZ00"
```
Ma być: brak wyniku.

**6. [lokalny PowerShell, (.venv) włączone]** Zmyślony sekret.
```powershell
$env:AWS_SECRET_ACCESS_KEY = "falszywysekret"
```
Ma być: brak wyniku.

**7. [lokalny PowerShell, (.venv) włączone]** Bieg 2, zmyślone klucze.
```powershell
python kod/control.py
```
Przewidywanie (**nieuruchomione**, bo nie dotykam AWS):
- dwie linie `UserWarning`, bo ostrzeżenie pada przed wysłaniem zapytania;
- **brak** linii `Kontrola: dane … wierszy`;
- `Kontrola: AWARIA - Athena: błąd - ` i dalej tekst błędu, najpewniej zaczynający się od
  `Execution failed on sql`, z nazwą w rodzaju `UnrecognizedClientException` („token jest
  nieprawidłowy”). Dokładnego tekstu nie znam. Liczy się **jeden** problem i słowo `Athena` na początku;
- `Kontrola: brak adresu stróża`.

Czasu biegu nie znam. Jeśli `pyathena` ponawia zapytanie, może to potrwać kilkanaście sekund.

**8. [lokalny PowerShell, (.venv) włączone]** Usuń wszystkie cztery zmienne.
```powershell
Remove-Item Env:AWS_ACCESS_KEY_ID, Env:AWS_SECRET_ACCESS_KEY, Env:KONTROLA_LOG, Env:KONTROLA_DATA
```
Ma być: brak wyniku.

**9. [lokalny PowerShell, (.venv) włączone]** Sprawdź, czy zmienne zniknęły.
```powershell
Get-ChildItem Env: | Where-Object Name -Match "KONTROLA|STROZ|DROGA|AWS"
```
Ma być: nic. **Nie pomijaj tego kroku.** Zmyślone klucze w oknie psują każdy kolejny bieg
z AWS, także `python kod/path.py`.

---

### Wyniki 25.09 (ok. 20:55 polskiego)

Kod napisał Gracjan. Słowa w jego wersji: `Kontrola: Dane N wierszy` i `Athena: Błąd - …`.
- `pytest kod/test_path.py -v`: `7 passed`; `python kod/path.py`: `2340`, `Dane: OK`;
  `pytest` na obu plikach: `18 passed in 0.61s`, bez `warnings summary`.
- **Bieg 1:** zgodny co do słowa. Kolejne linie: ostrzeżenie `UserWarning` (jedno, zajmuje
  dwie linie), `Kontrola: Dane 2340 wierszy`, `Kontrola: AWARIA -` z 3 × `wpis z przyszłości: 2026-09-25,
  dziś jest: 2026-09-18` (w kolejności CBF.WA, SNT.WA, XTB.WA), `Kontrola: brak adresu stróża`.
- **Bieg 2 (zmyślone klucze):** zgodne jest to, że wyszedł jeden problem
  `Athena: Błąd - An error occurred (UnrecognizedClientException) when calling the
  StartQueryExecution operation: The security token included in the request is invalid.`,
  nie było linii `Kontrola: Dane`, a skrypt się nie wywrócił. **Dwie rzeczy Claude
  przewidział źle:** tekst nie zaczyna się od `Execution failed on sql`; poza tym **nad**
  wynikiem pojawiły się linia `Failed to execute query.` i pełny `Traceback` (ok. 40 linii
  na Pythonie 3.14). To robi sama `pyathena`: przy błędzie woła `_logger.exception(...)`
  (`pyathena/common.py`). Nasz program nie ustawia `logging`, więc Python wypisuje to na stderr.
  Na EC2 stderr z `cron` trafia do `errors.txt`, więc w dniu awarii Atheny blok w logu będzie
  miał słowo `Traceback`. **Decyzja Gracjana 25.09: (a) zostawić.** Nie ma nowego kodu, a log
zachowuje pełny opis błędu. Świadomie przyjęty koszt: ręczny bieg `control.py` tego samego dnia,
po powrocie Atheny, dalej powie `AWARIA`, bo w dzisiejszym bloku jest `Traceback`. Stróż wróci
na `Up` dopiero przy następnym biegu o 18:30. Odrzucony wariant (b): wyciszenie loggera
`pyathena` w `control.py`.
- Zmienne usunięte, kontrolny odczyt pusty.

## Część 8. Commit (na koniec etapu A)

Komendy dostaniesz w krokach po biegach z Części 7, z przewidywaną liczbą zmian. Na EC2 nic nie
robimy, dopóki etap A nie jest zamknięty. `git pull` na EC2 tylko poza oknem 17:55–18:35
czasu polskiego.
