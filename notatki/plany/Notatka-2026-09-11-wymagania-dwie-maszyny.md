# Notatka projektowa — spisy wymagań dla dwóch maszyn

**Data:** 11 września 2026
**Dotyczy:** `requirements.txt` oraz nowy spis dla EC2
**Skąd to się wzięło:** punkt 2.10 przeglądu z 8 września,
„`requirements.txt` nie odtworzy środowiska EC2"
**Status:** do zatwierdzenia przez Gracjana. Pliki tworzone po
zatwierdzeniu i po sprawdzeniu spisu na maszynie.

---

## 1. Co mamy dziś

Jeden plik, `requirements.txt`, 32 pozycje, każda przypięta znakiem `==`
do konkretnej wersji. Powstał 17 sierpnia, przepisany 7 września przez
`pip freeze`.

Sprawdzone 11 września: `Compare-Object` między tym plikiem a `pip freeze`
z lokalnego `venv` zwróciło **pustkę**. Plik zgadza się z laptopem
co do joty, wszystkie 32 pozycje.

Jako spis jednej maszyny jest bez zarzutu. Problem polega na tym, że
nigdzie nie jest napisane, **której**.

---

## 2. Dlaczego jeden plik nie wystarczy

Pomiar z 11 września, obie maszyny, same odczyty.

| Co | Laptop | EC2 |
|---|---|---|
| Python | 3.14.2 | 3.9.25 |
| Liczba pakietów | 32 | 19 |
| pandas | 3.0.5 | 2.3.3 |
| numpy | 2.5.1 | 2.0.2 |
| urllib3 | 2.7.0 | 1.26.20 |
| PyAthena | 3.35.4 | 3.20.0 |
| requests | 2.34.2 | 2.32.5 |
| boto3 i botocore | 1.43.75 | 1.42.97 |
| s3transfer | 0.19.2 | 0.16.1 |
| tenacity | 9.1.4 | 9.1.2 |
| charset-normalizer | 3.4.9 | **3.5.1** |
| idna | 3.18 | **3.19** |
| fsspec | 2026.7.0 | 2025.10.0 |

Pogrubione dwie pozycje są na EC2 **nowsze** niż na laptopie. To psuje
wygodną opowieść „EC2 jest po prostu stare". Maszyny nie rozjechały się
w jedną stronę, tylko każda żyje własnym życiem, bo nic nigdy nie
porównywało ich ze sobą.

Cztery pozycje są identyczne na obu: `certifi`, `jmespath`,
`kafka-python` i `six`, oraz `python-dateutil` i `tzdata`. Zgodność
`kafka-python` to dobra wiadomość, bo przez tę bibliotekę przechodzą
wszystkie dane projektu.

### Dlaczego to jest pułapka, nie tylko nieaktualność

Gdyby trzeba było odtworzyć EC2 od zera, naturalnym odruchem jest
`pip install -r requirements.txt`. Na Pythonie 3.9 większość tych wersji
się nie zainstaluje, bo pandas 3.0.5 i numpy 2.5.1 wymagają nowszego
Pythona. W najlepszym razie instalacja padnie od razu. W gorszym przejdzie
częściowo i zostawi środowisko, w którym potok nie ruszy, a przyczyny
będzie się szukało w kodzie.

Brak pliku mówi „nie wiemy". Ten plik mówi „wiemy" i myli się co do
połowy projektu.

---

## 3. Co proponuję

**Dwa pliki, po jednym na maszynę, nazwa niesie maszynę.**

- `requirements-lokalny.txt` — dzisiejsza zawartość `requirements.txt`,
  bez żadnej zmiany treści, tylko nowa nazwa. Zmiana przez `git mv`,
  żeby historia pliku została.
- `requirements-ec2.txt` — nowy, 19 pozycji, spis ze środowiska
  `~/GPW---pulse/venv`.

**Bez komentarzy wewnątrz plików.** Kusi, żeby dopisać na górze linię
`# spis z laptopa`. Nie robimy tego z konkretnego powodu: oba pliki mają
zostać czystym wynikiem `pip freeze`, żeby dało się je porównać z
rzeczywistością **jedną komendą, bez filtrowania**. Każda dopisana linia
psuje to sprawdzenie na zawsze. Wyjaśnienie należy do tej notatki i do
nazwy pliku, nie do środka.

### Dlaczego nie jedna z pozostałych dróg

**Jeden plik z bibliotekami, których potok naprawdę używa, bez wersji.**
Odpada, bo obie maszyny potrzebują **innych wersji tej samej
biblioteki**. Pandas to 3.0.5 tu i 2.3.3 tam. Plik bez wersji zamiatałby
tę różnicę pod dywan, a to jest właśnie ta różnica, która potrafi zmienić
zachowanie kodu.

**Zostawienie jednego pliku z dopiskiem, czyj to spis.** Odpada, bo
zostawia EC2 bez żadnego spisu. Maszyna, która liczy dane co wieczór,
byłaby jedyną nieudokumentowaną.

### Dlaczego zmiana nazwy, a nie zostawienie `requirements.txt`

Nazwa `requirements.txt` jest konwencją i właśnie dlatego jest groźna.
Ktoś na EC2 wpisze `pip install -r requirements.txt` odruchowo, bo tak
się robi wszędzie. Po zmianie nazwy ta komenda zgłosi brak pliku.
To jest awaria głośna i nieszkodliwa, która zmusza do wyboru, zamiast
cicho zainstalować zły zestaw.

Koszt: jedna linia w `README.md` (104) do poprawienia. Wzmianki w starych
notatkach i dziennikach zostają, bo opisują stan z tamtego dnia.

---

## 4. Spis dla EC2 — 19 pozycji

```
boto3==1.42.97
botocore==1.42.97
certifi==2026.7.22
charset-normalizer==3.5.1
fsspec==2025.10.0
idna==3.19
jmespath==1.1.0
kafka-python==3.0.11
numpy==2.0.2
pandas==2.3.3
PyAthena==3.20.0
python-dateutil==2.9.0.post0
pytz==2026.3.post1
requests==2.32.5
s3transfer==0.16.1
six==1.17.0
tenacity==9.1.2
tzdata==2026.3
urllib3==1.26.20
```

### Skąd ta lista i dlaczego jej jeszcze nie ufamy

Nie została odczytana wprost z EC2. Została **wyprowadzona** z wyniku
`diff` uruchomionego tam 11 września. Linie oznaczone `>` to pozycje
z EC2, linie bez znaku to pozycje wspólne dla obu maszyn.

Wyprowadzenie ma jedno niezależne potwierdzenie: ostatni nagłówek `diff`
brzmiał `32c19`, czyli trzydziesta druga linia spisu lokalnego odpowiada
**dziewiętnastej** linii spisu z EC2. Lista powyżej ma dokładnie
dziewiętnaście pozycji. Rachunek zgadza się też od drugiej strony:
32 pozycje lokalne minus 14 brakujących plus 1 dodatkowa daje 19.

To jest mocna poszlaka, nie dowód. **Zanim ten spis trafi do pliku,
trzeba go porównać z prawdziwym `pip freeze` na EC2** — komenda w części
7.

> **Sprawdzone 11 września.** `pip freeze` na EC2 zwrócił dziewiętnaście
> linii, identycznych ze spisem powyżej co do znaku i co do kolejności.
> Wyprowadzenie z `diff` było poprawne. Spis powyżej jest odtąd
> odczytem, nie rekonstrukcją, i na jego podstawie powstał plik
> `requirements-ec2.txt`.

---

## 5. Czego na EC2 nie ma i czy to problem

Czternastu pozycji z laptopa na EC2 nie ma. Przeczytałem tę listę pod
kątem tego, co je ze sobą łączy, i wynik jest lepszy, niż się
spodziewałem.

**Wszystkie czternaście należą do trzech rodzin, i każda z tych rodzin
nie ma na EC2 nic do roboty.**

**Rodzina wykresów.** `matplotlib`, a za nim `contourpy`, `cycler`,
`fonttools`, `kiwisolver`, `pillow`, `pyparsing`. Wykresy powstają
z laptopa, `wykresy.py` nigdy nie był uruchamiany na EC2.

**Rodzina testów.** `pytest`, a za nim `iniconfig`, `pluggy`, `Pygments`
oraz `colorama`, który służy do kolorowania konsoli Windows i na
Linuksie nie miałby czego robić.

**Zapis Parquetu.** `pyarrow`. To jest decyzja z 4 września, opisana
w dzienniku z tamtego dnia i w Planie 06. `silver.py` na EC2 nie otwiera
plików z S3, tylko wysyła SQL, a Parquet czyta Atena po swojej stronie.
`pyarrow` jest potrzebny wyłącznie temu, kto **zapisuje**, czyli
kompakcji, a ta chodzi z laptopa.

`packaging` należy jednocześnie do rodziny testów i wykresów.

**Wniosek: na EC2 nie brakuje niczego przypadkiem.** Cztery narzędzia
świadomie tam nie chodzą i cały ubytek to one wraz z tym, co ze sobą
ciągną.

Zastrzeżenie co do sposobu, w jaki to ustaliłem: przypisanie pakietów do
rodzin zrobiłem z wiedzy o tym, czego te biblioteki zwykle wymagają, a nie
z odczytu na Twojej maszynie. Sprawdzenie jest w części 7 i zajmuje jedną
komendę.

> **Sprawdzone 11 września.** `pip show` potwierdził oba przypisania.
> `matplotlib` wymaga `contourpy`, `cycler`, `fonttools`, `kiwisolver`,
> `packaging`, `pillow` i `pyparsing`, czyli siedmiu z brakujących.
> `pytest` wymaga `colorama`, `iniconfig`, `packaging`, `pluggy`
> i `Pygments`, czyli czterech nowych obok wspólnego `packaging`.
> `pyarrow` nie wymaga niczego. Siedem plus cztery plus trzy same
> narzędzia daje **dokładnie czternaście**, czyli tyle, ile brakuje.
> Żaden pakiet nie zostaje bez wyjaśnienia.

### Jedna pozycja jest tylko na EC2

`pytz`. To zależność pandas w wersji drugiej. Pandas trzeci przeszedł na
mechanizm stref wbudowany w Pythona i `pytz` przestał być potrzebny.
Obecność tej paczki na EC2 i jej brak na laptopie są więc bezpośrednim
skutkiem różnicy wersji pandas, nie osobnym rozjazdem.

---

## 6. Co może pójść źle

**Oba pliki zestarzeją się przy pierwszej instalacji, jakiej ktoś
dokona.** Nic ich nie pilnuje. Dziś sprawdziliśmy je ręcznie po raz
pierwszy od 7 września, czyli po czterech dniach, i lokalny się zgadzał.
Przy dłuższej przerwie nie ma takiej gwarancji. Jedyne, co możemy
zrobić teraz, to zapisać obie komendy porównujące w tej notatce, żeby
sprawdzenie zajmowało pół minuty, a nie godzinę.

**Ktoś użyje spisu z laptopa na EC2.** To jest ta pułapka, przed którą
chroni zmiana nazwy. Po niej komenda z `requirements.txt` zgłosi brak
pliku zamiast zainstalować zły zestaw.

**Spis z EC2 przestanie się instalować sam z siebie.** Część tych wersji
to ostatnie, które wspierają Pythona 3.9. `boto3` porzucił tę wersję
Pythona 29 kwietnia 2026, czyli cztery i pół miesiąca temu. Im dalej,
tym mniej z tego spisu będzie dostępne. Spis jest więc zapisem stanu,
a nie gwarancją, że da się go odtworzyć za rok. To argument za Pythonem
3.10 na EC2, ale to osobny kawałek.

**Ktoś potraktuje spis jako listę zależności projektu.** Nie jest nią.
`pip freeze` wypisuje wszystko, co siedzi w środowisku, razem
z zależnościami zależności. Projekt importuje wprost tylko osiem
bibliotek spoza standardowego Pythona: `requests`, `kafka`, `pandas`,
`pyathena`, `boto3`, `botocore`, `matplotlib` i `pytest`, plus `pyarrow`
używany przez pandas bez jawnego importu.

**Dojdzie trzecia maszyna.** Wtedy schemat „jeden plik na maszynę"
przestanie się skalować i trzeba będzie wrócić do tej decyzji. Przy
dwóch jest najprostszy z możliwych.

---

## 7. Jak to sprawdzimy

### Sprawdzenie spisu z EC2 przed utworzeniem pliku

**[EC2, przez SSH]**

```bash
~/GPW---pulse/venv/bin/pip freeze
```

Wynik ma mieć dziewiętnaście linii i zgadzać się co do znaku ze spisem
z części 4. Każda różnica znaczy, że wyprowadzenie z `diff` było błędne
i plik trzeba oprzeć na tym wyniku, nie na mojej rekonstrukcji.

### Sprawdzenie przypisania pakietów do rodzin

**[lokalny PowerShell, (.venv) włączone]**

```bash
pip show matplotlib pytest pyarrow | Select-String "^(Name|Requires):"
```

Przy `matplotlib` mają się pojawić `contourpy`, `cycler`, `fonttools`,
`kiwisolver`, `packaging`, `pillow`, `pyparsing`. Przy `pytest`
`iniconfig`, `packaging`, `pluggy` i `Pygments`, a na Windowsie także
`colorama`. Jeśli któryś z czternastu brakujących pakietów nie należy do
żadnej z tych list, znaczy to, że jest tam z innego powodu i trzeba go
wyjaśnić osobno.

### Sprawdzenie po zmianie nazw, na przyszłość

Te dwie komendy zostają w notatce jako rutyna do powtórzenia, ilekroć
ktoś coś doinstaluje.

**[lokalny PowerShell, (.venv) włączone]**

```bash
Compare-Object (Get-Content requirements-lokalny.txt) (pip freeze)
```

**[EC2, przez SSH]**

```bash
cd ~/GPW---pulse && diff <(sort requirements-ec2.txt) <(venv/bin/pip freeze | sort)
```

W obu wypadkach **pusty wynik to sukces**.

---

## 8. Czego to nie naprawia

Piszę osobno, żeby nie uznać tej zmiany za większą, niż jest.

- **Nie zbliża środowisk do siebie.** Po tej zmianie dalej mamy Pythona
  3.14 i 3.9, pandas 3 i 2, `urllib3` w dwóch wersjach głównych. Zmiana
  tylko to opisuje.
- **Nie pilnuje sama siebie.** Nic nie sprawdza zgodności automatycznie.
  Zostają dwie komendy do ręcznego uruchomienia.
- **Nie naprawia Pythona 3.9 na EC2.** To osobna decyzja, odłożona
  w przeglądzie, i najpoważniejsza z całej tej rodziny spraw, bo jako
  jedyna pogarsza się sama z siebie z upływem czasu.
- **Nie dotyka kodu.** Żaden skrypt nie czyta tych plików.

---

## 9. Rzecz obok, ustalona przy okazji

`compaction.py` dostanie na górze komentarz mówiący, że wolno go
uruchamiać wyłącznie z laptopa i dlaczego. Dziś ta informacja żyje
w dzienniku z 4 września, w Planie 06 i w przeglądzie, czyli wszędzie
poza plikiem, który ktoś otworzy 1 października. Komentarz ma powiedzieć
trzy rzeczy: że skrypt należy do laptopa, że powodem jest brak `pyarrow`
na EC2, i że brak ten jest świadomy, bo `pyarrow` jest potrzebny tylko
przy zapisie Parquetu.

---

## Powiązane notatki

- [[Przeglad-2026-09-08-co-nie-gra]] — punkt 2.10, źródło tej pozycji;
  punkt 2.8, kompakcja i `pyarrow`
- [[Plan-06-domkniecie-i-strona]] — decyzja o `pyarrow` z 4 września
- [[Notatka-2026-09-11-podsumowanie-w-producencie]] — druga notatka
  z tego samego dnia
- [[Slownik]] — `pip freeze`, przypięcie wersji, zależność przechodnia
