# Notatka 24.09 — test prawdziwej drogi na EC2 (wpięcie do skryptu kontrolnego)

**Stan 26.09 wieczorem: wszystkie trzy etapy zamknięte — A (laptop) 25.09, B (EC2) i C
(pierwszy bieg z `cron`) 26.09. Wyniki pod Częścią 7. Zostaje obserwacja kilku dni, przede
wszystkim pierwszy dzień giełdowy 28.09.**

**Stan: zatwierdzona 25.09 w całości — wszystkie osiem decyzji w wariancie (a).** Instrukcja
do kodu: [[Notatka-2026-09-25-jak-wpiac-droge-do-kontroli]]. To dalszy ciąg siódmej naprawy z kolejki z przeglądu z 08.09
(„test prawdziwej drogi”). 23.09 powstały `kod/path.py` i `kod/test_path.py`. Działają, ale
tylko ręcznie z laptopa. Brakuje dwóch warunków definicji „zrobione”: (c) głośnej awarii
i (d) pracy na EC2. Ta notatka opisuje, jak to domknąć. Decyzje w Części 6 należą do Ciebie.
**Kodu jeszcze nie ma.** Numery linii i dokładne komendy dostaniesz w krokach, dopiero po
zatwierdzeniu (zasada 10). Przed pisaniem kodu dostaniesz też pełną notatkę-instrukcję
(zasada 3), jak 23.09.

---

## Część 1. Sedno w trzech zdaniach

1. Dziś skrypt kontrolny na EC2 (`control.py`, 18:30) czyta tylko **log** (`errors.txt`).
   Test drogi (`path.py`) czyta **dane** w Athenie, ale uruchamiasz go sam, z laptopa,
   i nikt nie dostaje maila, gdy coś wykryje.
2. Proponuję, żeby `control.py` o 18:30 robił obie rzeczy naraz: sprawdzał log (jak dziś)
   **i** pytał Athenę funkcją `sprawdz_daty`. Problemy z obu części trafiają do **jednej**
   listy, a ta do stróża w **jednym** zgłoszeniu.
3. Nie zmieniamy `crontab` ani ustawień stróża. Zmienia się kod dwóch plików, a na EC2
   wystarczy `git pull`. Awaria samej Atheny też ma być widoczna jako problem na liście,
   a nie wywracać skryptu.

---

## Część 2. Przykład na innych danych: wieczorna kontrola w lodziarni

Lodziarnia ma trzy smaki. Wieczorem kierownik robi kontrolę. Dotąd czytał tylko **raport
sprzedawcy** (kartkę „Raport z dnia…”), odpowiednik naszego logu `errors.txt`. Teraz ma
też zajrzeć do **zeszytu w szafce**, czyli odpowiednika tabeli w Athenie, i sprawdzić, czy
każdy smak ma dzisiejszy wpis. Wszystkie problemy zbiera na jedną kartkę i wysyła szefowi
jedną wiadomość. Szef to nasz stróż.

Są cztery kawałki kodu. Dwa pierwsze już znasz z projektu:

| Kawałek w przykładzie | Co robi |
|---|---|
| `sprawdz_raport(raport, dzis)` | sprawdza kartkę sprzedawcy, zwraca listę problemów (jak `sprawdz_blok`) |
| `sprawdz_zeszyt(df, smaki, dzis)` | Twoje pierwsze sprawdzenie z `sprawdz_daty`, słowo w słowo |
| `pobierz_zeszyt(szafka_otwarta)` | wyjmuje zeszyt z szafki; gdy szafka zamknięta, rzuca błąd (jak Athena, która nie odpowiada) |
| `kontrola(raport, dzis_tekst, szafka_otwarta)` | skleja obie listy i wypisuje jedną linię wyniku |

Najważniejszy fragment `kontrola`:

```python
problemy = sprawdz_raport(raport, dzis_tekst)
try:
    zeszyt = pobierz_zeszyt(szafka_otwarta)
    print(f"Kontrola: zeszyt {len(zeszyt)} wierszy")
    problemy = problemy + sprawdz_zeszyt(zeszyt, SMAKI, date.fromisoformat(dzis_tekst))
except Exception as e:
    problemy.append(f"Zeszyt: błąd odczytu - {e}")
```

Wejście: raport `"Raport z 2026-09-24"`, w zeszycie trzy wpisy z 24.09. **Wyniki poniżej
pochodzą z uruchomienia przykładu 24.09**, nie z głowy:

| Przypadek | Wyjście |
|---|---|
| 1. czwartek 24.09, wszystko jest | `Kontrola: zeszyt 3 wierszy`<br>`Kontrola: OK` |
| 2. udawany piątek 25.09 | `Kontrola: zeszyt 3 wierszy`<br>`Kontrola: AWARIA - Brak raportu z 2026-09-25; wanilia brak wpisu z: 2026-09-25; czekolada brak wpisu z: 2026-09-25; pistacjowy brak wpisu z: 2026-09-25` |
| 3. udawana sobota 26.09 | `Kontrola: zeszyt 3 wierszy`<br>`Kontrola: AWARIA - Brak raportu z 2026-09-26` (w sobotę zeszyt nie musi mieć wpisu) |
| 4. czwartek 24.09, szafka zamknięta | `Kontrola: AWARIA - Zeszyt: błąd odczytu - szafka zamknięta` (brak linii o liczbie wierszy, bo zeszytu nie było) |

**Czego uczy przypadek 4.** Raport był dobry, zeszytu nie dało się otworzyć, a wynik
i tak wyszedł jako zwykła awaria z powodem. Gdyby wewnętrznego `try` nie było, błąd
poleciałby do zewnętrznego `except`, który w `control.py` już jest. Tam wypisuje się
`Kontrola: Błąd skryptu - …`, skrypt kończy z kodem 1 i **nie wysyła nic do stróża**.
Wynik sprawdzenia logu przepada, a mail przychodzi dopiero o 19:00, od stróża, który
nie dostał zgłoszenia. Taki mail mówi tylko „cisza”, bez powodu.

### Przykład → projekt

| Lodziarnia | Projekt |
|---|---|
| raport sprzedawcy | blok dzisiejszego biegu w `companies/errors.txt` |
| `sprawdz_raport` | `sprawdz_blok` w `control.py` (bez zmian) |
| zeszyt w szafce | tabela `gold_dane_dzienne` w Athenie |
| `pobierz_zeszyt` | nowa funkcja `pobierz_dane()` w `path.py` (połączenie + `SELECT`) |
| `sprawdz_zeszyt` | `sprawdz_daty` w `path.py` (bez zmian albo z czwartym sprawdzeniem, decyzja 6) |
| szafka zamknięta | Athena nie odpowiada, brak uprawnień, zły klucz |
| `kontrola` | część pod `if __name__ == "__main__":` w `control.py` |
| wiadomość do szefa | zgłoszenie do stróża (`get` przy OK, `post …/fail` przy awarii) |
| `dzis_tekst` | `KONTROLA_DATA` albo dzisiejsza data maszyny |

---

## Część 3. Nowe pojęcia (do słownika na koniec sesji)

**`try` w środku `try`.** Wewnętrzny łapie tylko błąd ze swojego kawałka (tu: Athena),
zamienia go na zwykły problem i program idzie dalej. Zewnętrzny zostaje na wszystko inne,
na przykład brak pliku `errors.txt`. Wejście i wyjście: przypadek 4 wyżej.

**Skąd `boto3` bierze klucze do AWS (łańcuch poświadczeń).** `pyathena` używa pod spodem
`boto3`. `boto3` szuka kluczy w ustalonej kolejności i bierze **pierwsze**, które znajdzie:
1. zmienne środowiskowe `AWS_ACCESS_KEY_ID` i `AWS_SECRET_ACCESS_KEY`;
2. plik `~/.aws/credentials` (tak działa laptop);
3. rola maszyny (tak działa EC2, rola `gpw_tracker_ec2_role`).

Z tego wynika sposób na **wymuszenie awarii Atheny bez zmiany kodu**. Wystarczy przed
komendą ustawić te dwie zmienne na zmyślone wartości. `boto3` weźmie je jako pierwsze,
a AWS je odrzuci. Rola i plik zostają nietknięte, a zmienne znikają po zamknięciu okna
albo po `Remove-Item Env:` (na laptopie) czy `unset` (na EC2).

| Wejście | Wyjście (przewidywanie, **nie uruchamiałem**, bo nie dotykam AWS) |
|---|---|
| zmyślone `AWS_ACCESS_KEY_ID` i `AWS_SECRET_ACCESS_KEY` + bieg `path.py` | błąd z nazwą w rodzaju `UnrecognizedClientException` („token jest nieprawidłowy”), opakowany przez `pandas` w `Execution failed on sql …` |
| to samo + bieg nowego `control.py` | `Kontrola: AWARIA - Athena: błąd - Execution failed on sql …` jako jeden problem na liście |

Dokładny tekst błędu zobaczymy przy pierwszym biegu na laptopie. Przewidujemy **jeden**
problem i słowo `Athena` na początku, a nie cały tekst.

**Dlaczego nie osobna linia w `crontab` wysyłająca do tego samego stróża.** Stróż pamięta
tylko **ostatnie** zgłoszenie. Tak było 19.09: po `Failure` przyszło `OK` i stan przeszedł
`down → up`. Gdyby log dał awarię o 18:30, a test danych o 18:35 powiedział „OK”, drugie
zgłoszenie **wymazałoby** pierwsze. Stąd jedna lista i jedno zgłoszenie.

---

## Część 4. Co dokładnie się zmienia

**Pliki zmienia Gracjan.** Zmiany dotyczą tylko dwóch plików:

1. **`kod/path.py`**
   - Nowa funkcja `pobierz_dane()` zawiera cztery linie połączenia i `SELECT spolka, data
     FROM gold_dane_dzienne`, a zwraca tabelę. Część `__main__` w `path.py` woła tę funkcję
     zamiast własnego połączenia, więc ręczny bieg z laptopa działa jak dotąd.
   - Jeśli wybierzesz decyzję 6a: czwarte sprawdzenie w `sprawdz_daty` i jeden nowy test.
2. **`kod/control.py`**
   - `from path import sprawdz_daty, pobierz_dane`.
   - Pod `__main__`, zaraz po `sprawdz_blok`: wewnętrzny `try` pobiera dane, wypisuje linię
     `Kontrola: dane N wierszy`, dokłada problemy z `sprawdz_daty` do listy `blad`,
     a błąd Atheny zamienia na problem `Athena: błąd - …`.
   - Data dla `sprawdz_daty` to `date.fromisoformat(KONTROLA_DATA)`, czyli ta sama, co dla
     logu, tylko zamieniona z napisu na datę (pułapka typu: Część 5).
   - Reszta bez zmian: jedna linia `Kontrola: OK` albo `Kontrola: AWARIA - …`, `get` albo
     `post …/fail`, kod wyjścia 1 przy złej odpowiedzi stróża.

**Czego nie zmieniamy:** `crontab` (linia `30 18 … control.py >> …errors.txt 2>&1` zostaje),
ustawień stróża (`30 18`, `Europe/Warsaw`, 30 min zapasu), `sprawdz_blok`, `wytnij_blok`,
`test_control.py`, Silvera, Golda, Producenta, Konsumenta.

**Co się zmieni w logu** (przewidywanie, potwierdzi pierwszy ręczny bieg na EC2). Do linii
`Kontrola: OK` o 18:30 dojdą **3 linie**:
- 2 linie ostrzeżenia `pandas` o SQLAlchemy przy `pd.read_sql`, te same co w Silverze;
- 1 linia `Kontrola: dane N wierszy`.

Ostrzeżenia `boto3` o Pythonie 3.9 **nie będzie**. Sprawdziłem 24.09 w kodzie `boto3`:
wypisuje je tylko `boto3.client(...)` (Konsument, Gold), a `pyathena` tworzy sesję inną
drogą. Zgadza się to z blokiem z 18.09: Silver też pyta Athenę przez `pyathena` i tego
ostrzeżenia nie ma.

Blok urośnie z 29 do **32** linii w dzień giełdowy, a w weekend/święto z 27 do **30**.
Ostrzeżenia idą na stderr od razu, a `print` do pliku czeka w buforze do końca programu
(to widzieliśmy 19.09). Dlatego ostrzeżenia będą **nad** liniami `Kontrola:`, a
`Kontrola: OK` dalej ostatnia. Obie linie `Kontrola:` zaczynają się od `Kontrola:`, więc
`wytnij_blok` odsieje je przy drugim biegu tego samego dnia. Ostrzeżenia nie zawierają słów
`Traceback`, `Error`, `ERROR` ani `nietknięte` (sprawdzone na prawdziwym bloku z 18.09),
więc krok 8 codziennej kontroli dalej ma dać „nic”.

**Co sygnał złapie nowego:**
- **brak świecy w dzień giełdowy.** Dotąd taki dzień wyglądał jak sobota (`nowych dni: 0`,
  `Odebrano 0`) i przechodził. Teraz `sprawdz_daty` powie `… brak wpisu z: <dziś>`;
- wpis z przyszłości w tabeli;
- rozjazd liczby dni między spółkami (np. Athena oddała pół tabeli, jak 04.09);
- (z decyzją 6a) spółkę, której w tabeli nie ma wcale, także w weekend.

**Czego dalej nie złapie:** złej ceny przy dobrej dacie, korekt Yahoo wstecz, ceny
z trwającej sesji, ubytku dni **u wszystkich spółek po równo** (np. po nieudanej kompakcji,
gdy wszystkim zniknie ten sam miesiąc).

---

## Część 5. Co może pójść źle

| Ryzyko | Co się stanie | Jak się bronimy |
|---|---|---|
| Athena nie odpowiada, brak uprawnień, zły klucz | wyjątek w środku skryptu | wewnętrzny `try` → problem `Athena: błąd - …` → `post /fail` o 18:30, z powodem (decyzja 3) |
| Athena wisi i nie kończy zapytania | skrypt nie wysyła nic | stróż po 19:00 pisze mail „cisza”, bez powodu; głośno, ale później |
| Rola EC2 nie ma prawa czytać `gold/` przez Athenę | `AccessDenied` przy pierwszym biegu | rola ma `AmazonS3FullAccess` i `AmazonAthenaFullAccess` (spisane 15.09), więc powinno działać; **sprawdzi to pierwszy ręczny bieg na EC2, przed 18:30** |
| Święto w dzień roboczy | fałszywy alarm: mail `DOWN`, a dzień później `UP` | świadomie przyjęte 22.09 (decyzja 2 tamtej notatki); najbliższe: 11.11 (śr), 24–25.12 (czw–pt), 31.12 (czw), 1.01 (pt), **z pamięci, nie z kalendarza GPW** |
| Data przekazana jako napis zamiast daty | `AttributeError: 'str' object has no attribute 'weekday'` (sprawdzone 24.09) | `date.fromisoformat(KONTROLA_DATA)`; wewnętrzny `try` i tak zamieni to na problem, ale z mylącym powodem, więc wyłapać na laptopie |
| Pusta tabela albo brak całej spółki **w weekend** | `sprawdz_daty` zwraca `[]`, czyli „OK” (**sprawdzone 24.09** na Twojej funkcji: pusta tabela w sobotę → `[]`, brak pierwszej spółki w sobotę → `[]`) | decyzja 6 |
| `git pull` na EC2 w chwili biegu o 18:30 | bieg na pół starym, pół nowym pliku | `pull` tylko przed 17:55 albo po 18:35 polskiego |
| Skrypt odpala się dwa razy tego samego dnia | drugie zapytanie do Atheny i drugie zgłoszenie | nieszkodliwe: odsiew `Kontrola:` działa jak dziś, koszt zapytania to ułamek grosza |
| Bieg przed 18:10 (ręczny test) | dziś jeszcze nie ma wpisów → „brak” | w testach przed 18:00 udajemy **wczoraj** (`KONTROLA_DATA`), wtedy log i dane są kompletne (Część 7) |
| Czwarta spółka w `config.ticker` | Yahoo da jej inną liczbę dni (`range=3y`, wada z 13.09), więc sprawdzenie 3 alarmuje **codziennie** | do pamięci: dodanie spółki wymaga decyzji, jak liczyć jej dni |
| Test zależy od `path.py` | literówka w `path.py` wywraca też kontrolę logu | `test_control.py` importuje `control`, a ten `path`, więc błąd składni wyjdzie w `pytest` na laptopie, przed commitem |

---

## Część 6. Decyzje — Twoje

Każda w jednej linii, rekomendacja pierwsza.

1. **Gdzie wpiąć:** (a) do `control.py`, jedna lista i jedno zgłoszenie — **rekomendacja**;
   (b) osobna linia `cron` + **drugie zadanie u stróża** z drugim adresem (dwa maile, drugi
   sekret w `crontab`); (c) osobna linia, ten sam stróż — **odradzam**, bo drugie zgłoszenie
   wymazuje pierwsze (Część 3).
2. **Problem z danymi = awaria u stróża?** (a) tak, `post /fail` jak przy logu —
   **rekomendacja**, inaczej punkt (c) definicji dalej niespełniony; (b) tylko linia w logu,
   bez maila (cicho, czyli bez zmiany względem dziś).
3. **Błąd Atheny:** (a) wewnętrzny `try` → problem na liście, zgłoszony od razu —
   **rekomendacja**; (b) zostawić zewnętrzny `except` → mail o 19:00, bez powodu, a wynik
   logu przepada.
4. **Połączenie z Atheną:** (a) funkcja `pobierz_dane()` w `path.py`, używana przez
   `path.py` i `control.py` — **rekomendacja**, bo zapytanie jest w jednym miejscu i przy
   zmianie kolumn poprawia się jedno miejsce; (b) kopia czterech linii w `control.py`.
5. **Data dla danych:** (a) ta sama `KONTROLA_DATA` co dla logu — **rekomendacja**, jedno
   pokrętło, testy przewidywalne (Część 7); (b) osobna `DROGA_DATA` także w `control.py`.
   `DROGA_DATA` w ręcznym biegu `path.py` zostaje w obu wariantach.
6. **Luka „w weekend pusta tabela to OK”:** (a) czwarte sprawdzenie w `sprawdz_daty`:
   spółki z `ticker` bez ani jednego wiersza, sprawdzane zawsze; do tego jeden nowy test
   (7 zamiast 6) — **rekomendacja**, bo to kilka linii, a automat ma nie przepuszczać
   pustki; (b) zostawić, bo poniedziałek to złapie.
7. **Linia z liczbą wierszy:** (a) osobna linia `Kontrola: dane N wierszy` —
   **rekomendacja**, bo daje codziennej kontroli liczbę bez konsoli Atheny; (b) bez niej,
   wtedy blok ma 31/29 linii.
8. **Ostrzeżenie `pandas`:** (a) zostawić — **rekomendacja**, znane i nieszkodliwe
   (to samo co w Silverze); (b) wyciszyć w kodzie (`warnings`, nowe pojęcie, więcej do
   nauki niż zysku).

---

## Część 7. Jak sprawdzimy — kolejność pracy (bez komend, te przyjdą w krokach)

Przewidywania piszę w wiadomości **przed** każdą komendą. Liczba wierszy w Athenie to
3 × liczba dni. 23.09 było to 2334. Jeśli bieg z 24.09 się udał, powinno być **2337**
(nie sprawdziłem, dzisiejszej kontroli nie było).

**Etap A — laptop (Twój kod, ok. 1–1,5 godz.)**
1. Pełna notatka-instrukcja do kodu (zasada 3), dopiero potem pisanie.
2. `path.py` z `pobierz_dane()`, ręczny bieg → `N` wierszy i `Dane: OK` (jak 23.09).
3. (6a) czwarte sprawdzenie + test → `7 passed` w `test_path.py`.
4. `control.py` → `pytest` na obu plikach: `11 passed` i `6` albo `7 passed`.
5. Ręczne biegi `control.py` na laptopie, bez `STROZ_URL`, na prawdziwym bloku z 18.09
   (`KONTROLA_LOG` wskazuje `kod/dane_testowe/blok_2026-09-18.txt`):
   - `KONTROLA_DATA=2026-09-18` → log czysty, a dane mają trzy wpisy „z przyszłości”
     (dni po 18.09) → `AWARIA` z **3** problemami + `brak adresu stróża`;
   - to samo ze zmyślonymi kluczami AWS → **1** problem `Athena: błąd - …`, bez linii
     `dane N wierszy`.
6. Commit i `git push`.

**Etap B — EC2 (ok. 45 min), poza oknem 17:55–18:35**
1. `git pull` (z `6af7b48` przejdzie przez trzy commity dokumentacji i `path.py` do nowego).
   `git status --short` pusty.
2. Ręczne biegi w oknie SSH. `STROZ_URL` jest tylko w `crontab`, więc w oknie SSH go nie ma
   i nic nie poleci do stróża:
   - **E1, OK:** przed 18:00 z `KONTROLA_DATA` = wczoraj, po 18:35 bez zmiennej → linie
     ostrzeżeń, `Kontrola: dane N wierszy`, `Kontrola: OK`, `Kontrola: brak adresu stróża`.
     **To zarazem sprawdza uprawnienia roli do `gold/`.** Tu liczymy linie ostrzeżeń
     (przewidywanie: 2, od `pandas`).
   - **E2, alarm danych:** `KONTROLA_DATA` = następny dzień roboczy → **4** problemy
     (1 z logu „Brak pomiaru producenta” + 3 × „brak wpisu”).
   - **E3, awaria Atheny:** zmyślone klucze AWS → **1** problem `Athena: błąd - …`
     (log czysty, gdy data jak w E1).
   - **E4, stróż (proponuję, do Twojej decyzji):** E2 z `STROZ_URL` wpisanym w oknie →
     u stróża `Failure`, mail `DOWN` z czterema problemami. Potem E1 z `STROZ_URL` →
     `OK`, mail `UP`. To jedyny dowód „głośno” dla problemu z danymi przed prawdziwym
     biegiem. Adres przepisujesz z `crontab`, nie pokazujesz na zrzucie.
3. Bez zmiany `crontab`.

**Etap C — pierwszy bieg z `cron` o 18:30 (codzienna kontrola, ok. 10 min)**
- blok **32** linie w dzień giełdowy (30 w weekend);
- przedostatnia linia `Kontrola: dane N wierszy`, N = poprzednie + 3;
- ostatnia `Kontrola: OK`;
- stróż: kolejne `OK`, `GET` z `13.63.105.190`;
- `git status --short` pusty.

Potem kilka dni obserwacji, bo jeden bieg to za mało na „działa”. Pierwszy weekend sprawdzi
gałąź „sobota”.

**Wycofanie, gdyby coś poszło źle:** cofnąć commit na laptopie (`git revert`, nowy commit),
`push`, `pull` na EC2. `crontab` i stróż są nietknięte, więc nic więcej nie trzeba.

### Wyniki etapu B (26.09, sobota)

Wszystkie przewidywania zapisane w rozmowie **przed** komendami. Ręczne biegi bez `>>`, więc
nic nie trafiło do `errors.txt` (807 linii przed i po).

| Krok | Przewidziane | Wyszło |
|---|---|---|
| `date` przed `pull` | sobota, UTC, przed 15:55 | `Sat Sep 26 13:55:17 UTC 2026` |
| `git status --short` przed / po | pusty / pusty | zgodne |
| `git pull` | `6af7b48..fc6e262`, `Fast-forward`, `13 files changed, 3258 insertions(+), 178 deletions(-)` | zgodne co do liczby |
| E1, `KONTROLA_DATA=2026-09-25` | 2 linie ostrzeżenia `pandas`, `Kontrola: Dane 2340 wierszy`, `Kontrola: OK`, `Kontrola: brak adresu stróża` | zgodne co do słowa |
| E2, `KONTROLA_DATA=2026-09-28` | `AWARIA` z 4 problemami (1 z logu + 3 × `brak wpisu z: 2026-09-28`, kolejność CBF, XTB, SNT) | zgodne co do słowa |
| E3, zmyślone klucze AWS | `Failed to execute query.` + `Traceback`, potem **3 linie** wyniku: `Athena: Błąd - Execution failed on sql: …`, `An error occurred (UnrecognizedClientException) …`, `unable to rollback`; bez linii `Dane` | zgodne, wariant 3-liniowy |
| E4, adres z `crontab -l` przez `$( )` | `${#STROZ_URL}` = 56 | 56 |
| E4a (dane E2 + stróż) | 4 linie, bez `brak adresu`, bez `bramka … odpowiedziała` | zgodne; u stróża **#8 `Failure`**, `POST`, 16:04, **2450 B**, `up → down` |
| E4b (dane E1 + stróż) | `Kontrola: OK` | zgodne; **#9 `OK`**, `GET`, 16:04, `down → up` |
| po `unset` | `${#STROZ_URL}` = 0, `wc -l` 807 | zgodne |

- **Rozmiar treści #8:** 2450 = 154 (linia `AWARIA`, policzona) + 2 (pusta linia) + 2294 (blok
  z 25.09 bez linii `Kontrola:`). Tyle samo bajtów miał blok z 18.09 przy teście 19.09, bo oba
  bloki mają ten sam kształt.
- **Część 9 domknięta w trzech punktach:** rola EC2 czyta `gold_dane_dzienne` przez Athenę (E1);
  ostrzeżenia w `control.py` na EC2 to 2 linie od `pandas`, bez `boto3` (E1); dokładny tekst
  błędu przy zmyślonych kluczach (E3). **Otwarte:** czas biegów i to, czy `pyathena` ponawia
  zapytanie przed poddaniem się — nie mierzone.
- **Nieprzewidziane w tej notatce, przewidziane w rozmowie przed E3:** pandas 2.3.3 na EC2
  opakowuje błąd zapytania we własny komunikat ze znakami nowej linii, więc przy awarii Atheny
  wynik ma 3 linie, a nie 1 jak na laptopie (pandas 3.0.5). `Traceback` od `pyathena` na
  Pythonie 3.9: 25 linii razem z `Failed to execute query.`. W dniu prawdziwej awarii Atheny
  do bloku dojdzie więc ok. 30 linii zamiast 4. Nic to nie psuje w kontroli logu.
- **Maile `DOWN` i `UP` z 16:04:** oba przyszły na Interię o 16:19, 15 minut po zmianie stanu
  (hipoteza z 19.09 potwierdzona). Warunek (c) „awaria jest głośna” spełniony dla problemu
  z danymi.
- **Etap C, 26.09 wieczorem (`date` na EC2 17:00:43 UTC):** pierwszy bieg z `cron` o 18:30
  zgodny co do linii. Start w linii 808 (`16:00:02` UTC), `wc -l` 837, blok 30 linii zakończony
  2 liniami ostrzeżenia z `kod/path.py:32`, `Kontrola: Dane 2340 wierszy` i `Kontrola: OK`.
  Zero `Traceback|Error|ERROR|nietknięte`, pliki 780 × 3, zakładka `2369 2369 0`, S3 156615 B
  i 338 B, `git status --short` pusty. Stróż według Gracjana OK (zrzutu nie było). Gałąź
  „brakuje dzisiejszej świecy” (pon–pt) pierwszy raz 28.09.

---

## Część 8. Co to zepsuje za miesiąc

- **Codzienna kontrola** (CLAUDE.md, kroki 6–7): liczby 29/27 zmieniają się na 32/30. Do
  poprawienia w dniu wdrożenia.
- **Python 3.10 na EC2** (osobna, późniejsza sprawa): zniknie ostrzeżenie `boto3` u Konsumenta
  i w Goldzie, więc blok skurczy się o 4 linie (w weekend o 2, bo wtedy Konsument nie tworzy
  klienta S3). Nie robić obu zmian w jednym tygodniu, żeby było wiadomo, skąd zmiana
  liczby linii.
- **1.10 kompakcja:** zmienia `bronze`, a następny bieg Silvera i Golda przelicza wszystko.
  Gdyby kompakcja zgubiła dni u wszystkich spółek po równo, test tego **nie** złapie
  (Część 4).
- **25.10 zmiana czasu:** `date.today()` na EC2 liczy w UTC. O 18:30 polskiego jest 17:30
  UTC (zimą), czyli ta sama data. Bez wpływu.
- **Święta:** 11.11 pierwszy prawdziwy fałszywy alarm, mail `DOWN`, a 12.11 `UP`.
- **Zmiana kolumn w `gold_dane_dzienne`:** poprawka w jednym miejscu, w `pobierz_dane()`
  (z decyzją 4a).
- **Koszt Atheny:** jedno zapytanie dziennie po ok. 160 kB, poniżej minimalnej jednostki
  rozliczenia. Pomijalne.

---

## Część 9. Czego nie sprawdziłem

- Czy rola EC2 faktycznie czyta `gold_dane_dzienne` przez Athenę. Z EC2 pytaliśmy dotąd tylko
  `bronze` i `live` (Silver). Polityki wyglądają na wystarczające; potwierdzi to bieg E1.
- Liczbę ostrzeżeń w nowym `control.py` na EC2 w prawdziwym biegu. Przewidywanie 2 wynika
  z kodu `boto3` na laptopie i z bloku Silvera z 18.09. Laptop ma inną wersję `boto3`
  (1.43.75) niż EC2 (1.42.97), więc mocniejszym dowodem jest blok z 18.09: tam Silver
  pyta Athenę przez `pyathena` na EC2 i ostrzeżenia `boto3` nie ma.
- Dokładny tekst błędu przy zmyślonych kluczach i to, czy `pyathena` przed poddaniem się
  nie ponawia zapytania (czas biegu E3).
- Czas zapytania z EC2 (Silver robi podobne w kilka sekund, nie mierzone).
- Bieg `cron` z 24.09 (Athena 2337?). Dzisiejszej kontroli nie było.
- Listę świąt GPW na resztę 2026 roku (w Części 5 z pamięci).

## Szacunek

Etap A ok. 1–1,5 godz., etap B ok. 45 min, etap C 10 min dzień później. Najpewniej dwie
sesje: A w jednej, B i C w następnej. **Nie w tym samym czasie co zmiana Pythona na EC2.**

## Powiązane notatki

- [[Notatka-2026-09-22-test-prawdziwej-drogi]] — decyzje 1–4 z 22.09 (tabela `gold`,
  heurystyka pon–pt, start ręcznie, trzy sprawdzenia); ta notatka realizuje „(b) później”
  z decyzji 3.
- [[Notatka-2026-09-23-jak-napisac-testy-drogi]] — wzór pełnej instrukcji przed kodem.
- [[Notatka-2026-09-18-sygnal-awarii]] — skrypt kontrolny, stróż, odsiew `Kontrola:`,
  pułapka UTF-8.
- [[Przeglad-2026-09-08-co-nie-gra]] — kolejność napraw, punkt 7.
