# Notatka 21.09 — nawiasy w Pythonie: `()`, `[]`, `{}` i skąd wiedzieć, który do czego

**Stan: notatka do nauki, nie projektowa.** Napisana na Twoją prośbę z 19.09:
jak w Pythonie działają nawiasy okrągłe, kwadratowe i klamrowe, w której
sytuacji którego używamy i od czego to zależy, także `funkcja(xyz(abc))`
a `funkcja(xyz[abc])`. Do przeczytania 22.09 przed sesją. Całość to ok. godziny, a na start wystarczy 25
minut (Sedno, Trzy pytania, Twoje pytanie wprost i Ćwiczenia). Każda część daje się czytać osobno, ale zacznij od dwóch pierwszych
(„Sedno" i „Trzy pytania") — reszta to ich rozwinięcie.

**Skąd wiem, że wyniki są prawdziwe.** Każdy wynik pokazany niżej uruchomiłem
21.09 na laptopie: Python 3.14.2, pandas 3.0.5. **Niczego nie uruchamiałem na
EC2** (tam jest Python 3.9). Miejsca, w których zachowanie może być tam inne,
mają osobne ostrzeżenie. Przykłady biorę z lodów, kawy i herbaty, a fragmenty
Twojego kodu pokazuję dopiero w części „Gdzie to widzisz w swoim kodzie".

## Sedno w pięciu zdaniach

1. Każdy nawias w Pythonie robi jedną z dwóch rzeczy: albo **działa na to, co
   stoi tuż przed nim**, albo, gdy nic przed nim nie stoi, **tworzy nową
   wartość**.
2. Tuż za nazwą lub wartością: `(` znaczy „**wywołaj** to" (uruchom funkcję,
   metodę), a `[` znaczy „**wybierz z tego element**" (indeks, klucz,
   wycinek, kolumna).
3. Sam, bez niczego przed sobą: `(` to grupa, krotka albo generator, `[` to
   lista, a `{` to słownik albo zbiór.
4. Zapis czyta się **od lewej do prawej**, a każdy kolejny nawias działa na
   wszystko, co zostało zbudowane po jego lewej stronie.
5. Zagnieżdżone `f(g(x))` liczy się **od środka**: najpierw `g(x)`, a jego
   wynik trafia do `f`.

## Tabela główna

| | tuż za nazwą lub wartością | sam, nic przed nim |
|---|---|---|
| `( )` okrągłe | **wywołaj** (funkcję, metodę) | grupa, krotka, generator |
| `[ ]` kwadratowe | **wybierz element** (indeks, klucz, wycinek, kolumna) | **lista** albo lista składana |
| `{ }` klamrowe | nie występuje jako operacja | **słownik** albo **zbiór** |

Jedyne miejsce, w którym `{ }` stoi „wewnątrz czegoś", to tekst z literą `f`
przed cudzysłowem (f-string): tam `{ }` znaczy „wstaw tu wartość wyrażenia".

## Trzy pytania, które rozstrzygają każdy nawias

Weź dowolny nawias i zadaj trzy pytania w tej kolejności.

1. **Co stoi bezpośrednio przed nim?** Nazwa, wartość, inny nawias zamykający
   (`)` albo `]`)? Czy może nic, operator (`+`, `=`, `==`), przecinek, dwukropek
   albo słowo kluczowe (`in`, `if`, `return`, `and`, `not`, `for`)?
2. **Jeśli stoi nazwa, wartość albo zamknięcie:** `(` to wywołanie, `[` to
   wybór elementu.
3. **Jeśli nie stoi nic z tej listy:** `(` to grupa, krotka lub generator,
   `[` to lista, `{` to słownik lub zbiór.

Słowo kluczowe nie jest nazwą, więc nawias po nim jest „samodzielny":
`2 in (1, 2, 3)` daje `True`, a nawias po `in` to krotka, nie wywołanie.

Jak to działa na siedmiu zapisach (dane: `napisy = ["lody", "kawa"]`,
`ceny = {"kawa": 12.5, "herbata": 9.0}`):

| Zapis | Pytanie 1: co przed nawiasem? | Rola | Wynik |
|---|---|---|---|
| `len("lody")` | nazwa `len` | wywołanie | `4` |
| `napisy[1]` | nazwa `napisy` | wybór elementu | `'kawa'` |
| `ceny["kawa"]` | nazwa `ceny` | wybór po kluczu | `12.5` |
| `[10, 20, 30]` | nic (początek) | nowa lista | `[10, 20, 30]` |
| `{"a": 1}` | nic (początek) | nowy słownik | `{'a': 1}` |
| `(2 + 3) * 4` | nic (początek) | grupa | `20` |
| `sorted(napisy)[0]` | `)` po wywołaniu | wybór z wyniku wywołania | `'kawa'` |

## Okrągłe `( )`

### Wywołanie funkcji

„Wywołać" funkcję znaczy ją uruchomić. Sama nazwa (`len`) jest tylko
etykietą funkcji, dopiero `len(...)` ją uruchamia. W środku stoją
**argumenty**, czyli to, co funkcja dostaje.

```python
len("lody")            # 4
max(3, 9, 5)           # 9   (kilka argumentów, po przecinku)
round(3.14159, 2)      # 3.14
```

Argumenty mogą być pozycyjne (kolejność ma znaczenie) albo nazwane
(`nazwa=wartość`). Dla `def f(a, b=2): return a + b`:

```python
f(1)          # 3   (b dostaje wartość domyślną 2)
f(1, b=5)     # 6   (b podane jako nazwane)
```

Nawiasy w definicji `def f(a, b=2):` mają tę samą postać, ale robią coś
innego: **wymieniają parametry**, czyli nazwy, pod którymi funkcja będzie
widziała argumenty. Po `def nazwa` nic jeszcze nie jest wywoływane.

### Zagnieżdżone wywołanie: `funkcja(xyz(abc))`

Wywołania w wywołaniach liczą się **od środka**. Wynik wewnętrznego staje się
argumentem zewnętrznego.

```python
len(str(123))
# 1. str(123)  -> "123"     (liczba zamieniona na tekst)
# 2. len("123") -> 3
# wynik: 3

round(abs(-3.14159), 2)
# 1. abs(-3.14159)   -> 3.14159
# 2. round(3.14159, 2) -> 3.14
# wynik: 3.14
```

Czytaj to jak zdanie od środka: „długość tekstu z liczby 123", „zaokrąglij
wartość bezwzględną".

### Wywołanie metody: kropka i nawias

Metoda to funkcja przypięta do wartości przez kropkę. Nawias stoi zaraz za jej
nazwą, więc to nadal wywołanie.

```python
napisy = ["lody", "kawa"]
napisy[0].upper()        # 'LODY'
napisy[0].upper()[:2]    # 'LO'
```

Drugi zapis czytasz z lewej do prawej: `napisy[0]` (wybierz), `.upper()`
(wywołaj na tym, co wybrałeś), `[:2]` (weź wycinek z wyniku).

### Grupowanie i kolejność działań

Samodzielny `( )` wymusza kolejność, tak jak w matematyce.

```python
2 + 3 * 4            # 14   (mnożenie najpierw)
(2 + 3) * 4          # 20   (nawias najpierw)

not True and False   # False  (not dotyczy tylko True)
not (True and False) # True   (not dotyczy całego warunku w nawiasie)
```

Ta sama zasada działa w warunkach z `and` i `or`. Nawiasy nic nie kosztują, więc
gdy nie jesteś pewien priorytetu, dopisz je.

### Warunki w pandas: dlaczego każdy w osobnym nawiasie

Dla tabeli:

```
   kawa  herbata miasto
0     1        4      A
1     2        5      B
2     3        6      A
```

Warunki łączy się znakami `&` („i") oraz `|` („albo"), a **każdy warunek
musi mieć własny nawias**:

```python
df[(df["kawa"] > 1) & (df["herbata"] < 6)].index.tolist()   # [1]

df[df["kawa"] > 1 & df["herbata"] < 6]
# ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(),
#             a.item(), a.any() or a.all().
```

Powód: `&` wiąże w Pythonie **mocniej** niż `>` i `<`. Bez nawiasów Python
najpierw liczy `1 & df["herbata"]`, a potem próbuje porównać całą kolumnę,
i pandas nie wie, co zrobić z „prawdą" całej kolumny naraz. Ten sam wzorzec
masz w `gold.py` w linii 20, gdzie trzy warunki stoją w trzech nawiasach.
Zwykłe `and` i `or` nie działają na kolumnach — dlatego `&` i `|`.

### Krotka

Krotka (tuple) to lista, której nie da się zmienić po utworzeniu. **Krotkę robi
przecinek, nie nawias.**

```python
type((5))       # int      (nawias tylko grupuje, to nadal liczba 5)
type((5,))      # tuple    (przecinek robi krotkę)
type(())        # tuple    (pusta krotka)

x = 1, 2        # (1, 2)   (bez nawiasów, też krotka)
x = 5,          # (5,)     (jeden element, ale przecinek)
```

Krotka pojawia się częściej, niż się zdaje:

```python
a, b = (10, 20)          # rozpakowanie: a to 10, b to 20
def g():
    return (1, 2)
g()                      # (1, 2)
g()[1]                   # 2   (wywołaj, potem wybierz z wyniku)
2 in (1, 2, 3)           # True
```

Niezmienność w praktyce:

```python
t = (1, 2)
t[0] = 5
# TypeError: 'tuple' object does not support item assignment
```

Dla porównania listę i słownik da się zmieniać przez `[ ]` po lewej stronie
znaku `=`: `l[0] = 5` zmienia pierwszy element listy, a `d['b'] = 2` dopisuje
klucz do słownika (sprawdzone).

W `except (A, B, C):` nawias też tworzy krotkę: „złap którykolwiek z tych
wyjątków".

### Generator

Nawias z `for` w środku to **generator**: przepis na ciąg wartości, liczonych
dopiero wtedy, gdy ktoś o nie poprosi.

```python
type((x for x in range(3))).__name__      # 'generator'
list((x for x in range(3)))               # [0, 1, 2]
sum(x * x for x in range(4))              # 14   (0 + 1 + 4 + 9)
```

Gdy generator jest **jedynym** argumentem funkcji, jego nawias zlewa się
z nawiasem wywołania (`sum(x * x for x in range(4))`). Tak masz w
`kafka_consumer.py` w liniach 27 i 31.

### Zawijanie długiej linii

Wnętrze `( )`, `[ ]` i `{ }` może ciągnąć się przez wiele linii bez
żadnego znaku łączenia:

```python
suma = (1 +
        2 +
        3)
suma       # 6
```

Dlatego wielolinijkowe wywołania, jak `connect(...)` w `silver.py`, są
zapisane po jednym argumencie w linii. Cena tej wygody: gdy zgubisz
nawias zamykający, Python zorientuje się dopiero na końcu i błąd bywa daleko
od miejsca pomyłki (patrz część o błędach).

### `lambda`

`lambda` to funkcja bez nazwy, zapisana w jednej linii. Nawias wokół niej
robi z niej wartość, którą można od razu wywołać.

```python
(lambda x: x + 1)(5)                       # 6
list(map(lambda x: x * 2, [1, 2, 3]))      # [2, 4, 6]
sorted(napisy, key=lambda s: s[-1])        # ['kawa', 'lody']
```

W pierwszym zapisie pierwszy nawias grupuje `lambda`, a drugi ją wywołuje z
argumentem 5. W trzecim `key=` mówi, **po czym** sortować: po ostatniej literze
(`'a'` idzie przed `'y'`).

### Rozpakowanie `*` i `**`

Gwiazdka przy argumencie „wysypuje" listę na osobne argumenty:

```python
max(*[3, 9, 5])            # 9   (jak max(3, 9, 5))
print(*[1, 2, 3])          # wypisze: 1 2 3
print(*["a", "b"], sep="-")   # wypisze: a-b
```

Dwie gwiazdki robią to samo ze słownikiem, także w `{ }`:

```python
{**{"a": 1}, **{"b": 2}}   # {'a': 1, 'b': 2}
```

## Kwadratowe `[ ]`

### Lista

```python
lista = [10, 20, 30]
```

Pusta lista to `[]`. Listę można też zbudować z czegoś innego:
`list("abc")` daje `['a', 'b', 'c']`.

### Indeks i indeks ujemny

`lista[n]` wybiera element o numerze `n`. **Liczy się od zera.**

```python
lista[0]      # 10
lista[-1]     # 30   (minus liczy od końca: -1 to ostatni)
lista[5]      # IndexError: list index out of range
```

Indeks działa też na tekście i krotce:

```python
"lody"[1]        # 'o'
(1, 2, 3)[0]     # 1
```

### Wycinek

Dwukropek w `[ ]` wybiera **zakres**. Początek jest wliczony, koniec nie.

```python
lista[1:3]     # [20, 30]   (od 1 do 3, bez 3)
lista[:2]      # [10, 20]   (od początku do 2, bez 2)
lista[1:]      # [20, 30]   (od 1 do końca)
lista[::-1]    # [30, 20, 10]   (odwrócona)
"lody"[1:3]    # 'od'
```

W `control.py` linia `linie[start:]` to „wszystkie linie od numeru `start` do
końca".

### Klucz słownika

Słownik tworzysz klamrami, ale **czytasz kwadratowymi**:

```python
ceny = {"kawa": 12.5, "herbata": 9.0}
ceny["kawa"]           # 12.5
ceny["kawa"] * 2       # 25.0
ceny["mleko"]          # KeyError: 'mleko'   (nie ma takiego klucza)
```

Gdy klucza może nie być, użyj metody `.get`, która ma **okrągłe** nawiasy:

```python
ceny.get("mleko", 0)   # 0      (drugi argument to wartość zapasowa)
ceny.get("kawa")       # 12.5
ceny.get("mleko")      # None   (bez drugiego argumentu)
```

To ta sama różnica, którą znasz z `os.environ.get("NAZWA", "domyślna")`.
`os.environ["NAZWA"]` rzuciłoby błąd, gdyby zmiennej nie było.

### Wiele nawiasów kwadratowych pod rząd

Czytaj od lewej do prawej. Każdy nawias działa na wynik poprzedniego.

```python
dane = {"kawa": {"cena": 12.5, "sztuki": [1, 2, 3]}}
dane["kawa"]["sztuki"][2]
# dane                  -> słownik
# dane["kawa"]          -> słownik {"cena": ..., "sztuki": ...}
# ...["sztuki"]         -> lista [1, 2, 3]
# ...[2]                -> 3
# wynik: 3

[[1, 2], [3, 4]][1][0]                # 3
{"k": (1, [2, 3])}["k"][1][0]          # 2
[(1, 'a'), (2, 'b')][1][0]             # 2
```

Do tego dochodzą wywołania w środku łańcucha, np. z `data_ingestion.py`:
`response.json()["chart"]["result"][0]`. To: wywołaj `.json()`, wybierz klucz
`"chart"`, wybierz klucz `"result"`, wybierz element numer 0. Cztery nawiasy,
cztery kroki, od lewej do prawej.

### Lista składana

Lista składana buduje nową listę z innej, w jednej linii:

```python
[x * 2 for x in [1, 2, 3, 4] if x > 1]     # [4, 6, 8]
[len(w) for w in napisy]                   # [4, 4]
[(x, y) for x in [1, 2] for y in "ab"]
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
```

Schemat: `[co_zrobić for element in skąd if warunek]`, a `if` na końcu jest
nieobowiązkowy. Gdy widzisz `[` z `for` w środku, to nie jest zwykła lista,
tylko przepis na listę.

### Pandas: `df["a"]`, `df[["a", "b"]]`, `df[warunek]`

Tabela z przykładu wyżej to `df`. **Zewnętrzny `[ ]` zawsze wybiera, a wnętrze
mówi, co wybrać.**

```python
df["kawa"]                       # jedna kolumna  -> Series: 1, 2, 3
df[["kawa"]]                     # jedna kolumna  -> DataFrame (tabela z 1 kolumną)
df[["kawa", "herbata"]].shape    # (3, 2)   dwie kolumny -> DataFrame
```

Reguła: **nazwa w `[ ]` daje Series, lista nazw w `[ ]` daje DataFrame**.
Podwójny nawias to nie jeden nawias, tylko dwa: zewnętrzny wybiera, wewnętrzny
tworzy listę nazw. Dlatego przecinek w jednym nawiasie nie działa:

```python
df["kawa", "herbata"]
# KeyError: ('kawa', 'herbata')
```

Przecinek w `[ ]` tworzy krotkę, więc pandas szuka jednej kolumny o nazwie
`('kawa', 'herbata')`. (Ta sama zasada: `{(1, 2): "punkt"}[1, 2]` daje
`'punkt'`.)

Filtrowanie wierszy to wybór z warunkiem w środku:

```python
df[df["kawa"] > 1].index.tolist()    # [1, 2]
# wnętrze: df["kawa"] > 1  -> True/False dla każdego wiersza (maska)
# zewnętrzny [ ]           -> zostaw wiersze, gdzie maska ma True
```

`.loc` i `.iloc` wyglądają jak metody, ale używają `[ ]`, bo to obiekty do
wyboru, nie funkcje. `.loc[wiersze, kolumny]` wybiera po nazwach i warunkach,
a `.iloc[numer, numer]` po pozycjach:

```python
df.loc[0, "kawa"]                                # 1
df.iloc[0, 0]                                    # 1
df.loc[df["kawa"] > 1, "herbata"].tolist()       # [5, 6]
```

Mieszanka, w której widać wszystkie role naraz:

```python
df.groupby("miasto")["kawa"].sum().to_dict()
# groupby("miasto")   wywołanie: pogrupuj po kolumnie
# ["kawa"]            wybór: weź kolumnę z grup
# .sum()              wywołanie: zsumuj
# .to_dict()          wywołanie: zamień na słownik
# wynik: {'A': 4, 'B': 2}

df.groupby("miasto")["kawa"].agg(["min", "max"]).reset_index().values.tolist()
# [['A', 1, 3], ['B', 2, 2]]     (lista nazw funkcji w wywołaniu agg)

df.rename(columns={"kawa": "K"}).columns.tolist()       # ['K', 'herbata', 'miasto']
df.drop(columns=["miasto"]).shape                       # (3, 2)
df.sort_values(["miasto", "kawa"]).index.tolist()       # [0, 2, 1]
```

W `rename` słownik `{"kawa": "K"}` znaczy „stara nazwa: nowa nazwa". W `drop`
i `sort_values` lista w nawiasie kwadratowym to **lista kolumn**. Kolejność w
`sort_values(["miasto", "kawa"])` ma znaczenie: najpierw miasto, w obrębie
miasta kawa.

Zbędny nawias, który widać w `gold.py:11`: `(df["kawa"].pct_change()) * 100`
daje ten sam wynik co `df["kawa"].pct_change() * 100`, bo wywołanie wykonuje
się przed mnożeniem. Nie szkodzi, ale nie jest potrzebny.

### Podpowiedzi typów

W `def f(x: list[int]) -> dict[str, int]:` `[ ]` opisują, co jest w środku
listy albo słownika. Żadna kontrola się nie wykonuje, to tylko opis dla
czytelnika i narzędzi. Uwaga na wersje: zapis `list[int]` działa od Pythona
3.9, ale `int | None` dopiero od 3.10 (z dokumentacji zmian Pythona; na EC2
nie sprawdzałem).

## Klamrowe `{ }`

### Słownik

Pary `klucz: wartość`, po przecinku.

```python
ceny = {"kawa": 12.5, "herbata": 9.0}
type({}).__name__            # 'dict'
type({"a": 1}).__name__      # 'dict'
```

`in` na słowniku sprawdza **klucze**, nie wartości:

```python
"kawa" in ceny     # True
12.5 in ceny       # False
```

Kluczem może być tylko wartość niezmienna (tekst, liczba, krotka), a listą
nie:

```python
{[1, 2]: 3}
# TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
# (w starszych Pythonach: "unhashable type: 'list'")

punkty = {(1, 2): "punkt"}
punkty[(1, 2)]     # 'punkt'   (krotka jako klucz)
```

### Zbiór i pułapka pustych `{}`

Zbiór (set) to kolekcja bez powtórzeń i bez kolejności. Zapisuje się go
klamrami, ale **bez kluczy**.

```python
type({1}).__name__       # 'set'
set([1, 1, 2])           # {1, 2}
type({}).__name__        # 'dict'    <- pusty {} to SŁOWNIK, nie zbiór
type(set()).__name__     # 'set'     <- pusty zbiór trzeba zrobić tak
```

To najczęstsza pomyłka z klamrami: pusty zbiór **nie** ma własnego zapisu.

### Słownik i zbiór składany

Tak samo jak lista składana, tylko w klamrach:

```python
{w: len(w) for w in napisy}                  # {'lody': 4, 'kawa': 4}
{len(w) for w in ["a", "bb", "cc"]}          # {1, 2}   (powtórki znikają)
```

Po dwukropku widać słownik, bez dwukropka zbiór.

### f-string

Tekst z literą `f` przed cudzysłowem. Wszystko w `{ }` to wyrażenie Pythona,
którego wynik trafia do tekstu.

```python
imie = "Ola"
f"Cześć {imie}"                    # 'Cześć Ola'
f"{len(napisy)} elementy"          # '2 elementy'   (wywołanie w środku)
f"{2 + 3}"                         # '5'            (dowolne wyrażenie)
f"{3.14159:.2f}"                   # '3.14'         (po dwukropku: format, 2 miejsca po przecinku)
f"{{tekst}}"                       # '{tekst}'      (podwójna klamra to zwykła klamra)
```

Uwaga na cudzysłowy. Gdy tekst jest w `"..."`, wyrażenie w środku musi
używać apostrofów:

```python
f"{ceny['kawa']}"      # '12.5'   działa w każdej wersji Pythona
f"{ceny["kawa"]}"      # '12.5'   działa na 3.14 — ale to zmiana z Pythona 3.12
```

**EC2 ma Pythona 3.9, na którym drugi zapis jest błędem składni** (nie
uruchamiałem tego na EC2; wiem z dokumentacji zmian Pythona 3.12). Dlatego w
kodzie na EC2 masz apostrofy w środku: `silver.py:20` i `data_ingestion.py:9`.
Zostań przy tym zwyczaju, dopóki EC2 jest na 3.9.

### `.format()` — starszy zapis

```python
"Cena: {}".format(9.5)              # 'Cena: 9.5'
"{0}-{1}-{0}".format("a", "b")      # 'a-b-a'   (numer wskazuje argument)
```

Robi to samo co f-string, tylko wartości podaje się osobno, w okrągłych
nawiasach za `.format`.

## `xyz(abc)` a `xyz[abc]` — Twoje pytanie wprost

Od czego zależy wybór? **Od tego, czym jest `xyz`.**

| `xyz` jest | Używasz | Bo |
|---|---|---|
| funkcją, metodą, klasą (coś, co się **uruchamia**) | `xyz(abc)` | to wywołanie, `abc` to argument |
| listą, słownikiem, tekstem, krotką, tabelą (coś, z czego się **wybiera**) | `xyz[abc]` | to wybór, `abc` to numer, klucz albo kolumna |

Cztery zapisy z tymi samymi elementami, cztery różne znaczenia
(`napisy = ["lody", "kawa"]`):

| Zapis | Jak czytać | Wynik |
|---|---|---|
| `len(str(123))` | `str` i `len` to funkcje; wywołaj `str`, wynik daj do `len` | `3` |
| `len(napisy[1])` | `napisy` to lista; wybierz element 1, jego daj do `len` | `4` |
| `sorted(napisy)[0]` | wywołaj `sorted` na liście, z wyniku wybierz element 0 | `'kawa'` |
| `sorted(napisy[0])` | wybierz element 0 z listy (to `'lody'`), jego daj do `sorted` | `['d', 'l', 'o', 'y']` |

Ostatnie dwa są zbudowane z tych samych znaków, w innej kolejności. Pierwszy
sortuje **listę** i bierze pierwszy wyraz, drugi sortuje **litery jednego
wyrazu**. Kolejność nawiasów jest kolejnością działań.

Jak sprawdzić, czym jest `xyz`, gdy nie wiesz? Sam Python powie ci, gdy
się pomylisz:

```python
lista(0)     # TypeError: 'list' object is not callable
len[lista]   # TypeError: 'builtin_function_or_method' object is not subscriptable
```

Słowo **callable** znaczy „da się wywołać nawiasem okrągłym", a **subscriptable**
„da się wybrać z tego nawiasem kwadratowym". Pierwszy komunikat mówi: „lista
nie jest funkcją, nie wołaj jej". Drugi: „`len` jest funkcją, nie wybieraj z niej".

## Nawiasy w miejscach, gdzie pytasz o coś innego niż Python

W Twojej pracy te same znaki pojawiają się w innych językach i znaczą coś
innego. Kiedy przeglądasz komendę, zapytaj: **w jakim języku jest ten wiersz?**

| Gdzie | Nawiasy | Co znaczą | Przykład z Twojej pracy |
|---|---|---|---|
| tekst w cudzysłowie | dowolne | zwykłe znaki, Python ich nie czyta | `"[abc]"` |
| SQL (Athena) | `( )` | wywołanie funkcji, grupa, lista po `IN` | `COUNT(DISTINCT data)` |
| PowerShell | `{ }` | **blok kodu** do wykonania na każdym elemencie | `Where-Object { $_.Name -match "x" }` |
| PowerShell | `( )` | wyrażenie do policzenia najpierw | `(Get-Content owoce.txt).Count` |
| bash | `$( )` | wynik komendy wstawiony w to miejsce | — |
| bash | `<( )` | wynik komendy udający plik | `diff <(crontab -l) plik` |
| bash | `${#zmienna}` | długość wartości zmiennej | `echo ${#STROZ_URL}` |
| regex / `grep -E` | `( )`, `[ ]`, `{ }` | grupa, zbiór znaków, liczba powtórzeń | `[0-9]` to „jedna cyfra" |
| Obsidian | `[[nazwa]]` | link do notatki | `[[Slownik]]` |
| Markdown | `[tekst](adres)` | link | — |

Przykład z `grep -E`, gdzie `\|` (kreska pionowa) znaczy „albo":

```bash
grep -n -E "Traceback|Error|ERROR|nietknięte" companies/errors.txt
```

## Gdzie to widzisz w swoim kodzie

Fragmenty z Twoich plików, żeby nawiasy przestały być abstrakcją. Numery
linii z 21.09.

| Miejsce | Fragment (skrócony) | Co robią nawiasy, po kolei |
|---|---|---|
| `gold.py:7` | `pd.read_csv(os.path.join(BASE_DIR, "silver", "clean_data.csv"))` | dwa wywołania, jedno w drugim: najpierw `os.path.join` skleja ścieżkę, jej wynik idzie do `read_csv` |
| `gold.py:11` | `(gold.groupby("spolka")["cena"].pct_change())*100` | wywołanie, wybór kolumny, wywołanie; zewnętrzny nawias jest zbędny, bo wywołanie i tak idzie przed `*` |
| `gold.py:12` | `.agg(["first", "last"]).reset_index()` | lista nazw funkcji w środku wywołania `agg`; potem kolejne wywołanie |
| `gold.py:17` | `.groupby(["spolka", "miesiac"])["zmiana_proc"].agg(["std", "count"])` | **lista** w `groupby` = grupuj po dwóch kolumnach naraz; `[ "zmiana_proc" ]` = wybierz kolumnę z grup |
| `gold.py:18` | `.rename(columns={"min": "pierwszy_miesiac", ...})` | słownik w argumencie nazwanym: stara nazwa, nowa nazwa |
| `gold.py:20` | `zmiana_msc[(A) & (B) & (C)]` | trzy warunki, każdy w osobnym nawiasie, spięte przez `&`, całość w `[ ]` jako filtr wierszy |
| `gold.py:21` | `f"... {len(zmiana_msc)} ... {len(pelne)}"` | `{ }` w f-string, a w środku wywołanie |
| `gold.py:29` | `for nazwa in ["dane_dzienne", "ranking"]:` | lista dwóch nazw, pętla weźmie je po kolei |
| `silver.py:6` | `connect(s3_staging_dir=..., region_name=..., schema_name=...)` | wywołanie rozpisane na wiele linii; argumenty nazwane |
| `silver.py:15` | `sort_values(["spolka", "data"])` | lista kolumn: najpierw po pierwszej, w obrębie pierwszej po drugiej |
| `silver.py:20` | `assert set(dane["spolka"].unique()) == set(ticker), f"...{dane['spolka'].unique()}"` | wywołania i wybory w jednym wyrażeniu; w f-string **apostrofy** w środku (bezpieczne na Pythonie 3.9) |
| `data_ingestion.py:19` | `lambda x: dumps(x).encode('utf-8')` | `lambda` z dwoma wywołaniami w łańcuchu: `dumps(x)`, potem `.encode(...)` na wyniku |
| `data_ingestion.py:27` | `dane = {}` | pusty **słownik** |
| `data_ingestion.py:34` | `data_str, cena_str = linia.split(", ")` | wywołanie zwraca listę dwóch tekstów, przecinek po lewej je rozpakowuje |
| `data_ingestion.py:35` | `data_str.split(" ")[0]` | wywołanie, potem wybór pierwszego elementu z wyniku |
| `data_ingestion.py:45` | `params = {"range": "3y", "interval": "1d"}` | słownik: nazwy parametrów zapytania i ich wartości |
| `data_ingestion.py:49` | `response.json()["chart"]["result"][0]` | wywołanie, dwa klucze, jeden numer, od lewej do prawej |
| `data_ingestion.py:53` | `for t, c in con:` | każdy element `con` to para, rozpakowana do `t` i `c` |
| `data_ingestion.py:66` | `producer.send('gpw_tracker', value={...}).get(timeout=10)` | słownik jako argument nazwany, w nim f-string i wybór `dane[data]`; potem `.get(...)` **na wyniku** `send(...)` |
| `data_ingestion.py:79` | `except (requests.exceptions.RequestException, TypeError, KeyError):` | nawias tworzy krotkę wyjątków: „złap którykolwiek" |
| `kafka_consumer.py:27` | `"\n".join(dumps(w) for w in wiadomosci)` | generator jako jedyny argument, jego nawias zlewa się z wywołaniem `join` |
| `kafka_consumer.py:31` | `sum(len(w) for w in odebrane.values())` | generator w `sum`; w środku wywołanie `.values()` |
| `control.py:11` | `[linia.split(":")[0] for linia in blok.splitlines() if "stan: zapisane" in linia]` | lista składana; w niej wywołanie, potem wybór `[0]` |
| `control.py:35` | `os.environ.get("KONTROLA_LOG", os.path.join(...))` | drugi argument to wartość zapasowa, sam jest wywołaniem |
| `control.py:49` | `data=(tekst + "\n\n" + blok).encode("utf-8")` | **nawias grupuje sklejanie**, żeby `.encode` zadziałało na całości; bez niego `.encode` dotyczyłoby tylko `blok` |

Ostatni wiersz to dobry przykład, po co grupowanie: `tekst + "\n\n" + blok.encode(...)`
próbowałoby zakodować sam `blok` i skleić bajty z tekstem, co kończy się błędem.

## Błędy nawiasowe: co mówi komunikat

Komunikaty z Pythona 3.14.2 (dokładnie skopiowane). Pierwsza kolumna to to,
co napisałeś.

| Napisałeś | Komunikat | Co znaczy | Naprawa |
|---|---|---|---|
| `lista(0)` | `TypeError: 'list' object is not callable` | okrągły nawias na liście | `lista[0]` |
| `ceny("kawa")` | `TypeError: 'dict' object is not callable` | okrągły nawias na słowniku | `ceny["kawa"]` |
| `len[lista]` | `TypeError: 'builtin_function_or_method' object is not subscriptable` | kwadratowy nawias na funkcji | `len(lista)` |
| `ceny["mleko"]` | `KeyError: 'mleko'` | brak takiego klucza | `ceny.get("mleko", 0)` |
| `lista[5]` | `IndexError: list index out of range` | za duży numer | sprawdź `len(lista)` |
| `ceny{"kawa"}` | `SyntaxError: invalid syntax` | klamry nie służą do odczytu | `ceny["kawa"]` |
| `df["kawa", "herbata"]` | `KeyError: ('kawa', 'herbata')` | przecinek w `[ ]` robi krotkę | `df[["kawa", "herbata"]]` |
| `df[df["kawa"] > 1 & df["herbata"] < 6]` | `ValueError: The truth value of a Series is ambiguous...` | `&` bez nawiasów wokół warunków | `df[(...) & (...)]` |
| `print(1 + 2` | `SyntaxError: '(' was never closed` | brak `)` | dopisz `)` |
| `x = (1 + 2]` | `SyntaxError: closing parenthesis ']' does not match opening parenthesis '('` | zły rodzaj zamknięcia | zamień `]` na `)` |
| `print(1))` | `SyntaxError: unmatched ')'` | jeden `)` za dużo | usuń nadmiarowy |
| `[1, 2` | `SyntaxError: '[' was never closed` | brak `]` | dopisz `]` |
| `{1: 2` | `SyntaxError: '{' was never closed` | brak `}` | dopisz `}` |
| `{[1, 2]: 3}` | `TypeError: cannot use 'list' as a dict key (unhashable type: 'list')` | lista nie może być kluczem | użyj krotki `(1, 2)` |
| `t[0] = 5` (`t` to krotka) | `TypeError: 'tuple' object does not support item assignment` | krotki nie da się zmienić | zrób nową krotkę albo użyj listy |

**Uwaga o EC2.** Komunikaty o niezamkniętym nawiasie w takiej postaci
(`'(' was never closed`) mają Pythony od 3.10. Python 3.9 z EC2 pisze w takich
razach ogólniej (z dokumentacji zmian: `unexpected EOF while parsing`) i często
wskazuje koniec pliku, a nie miejsce zgubionego nawiasu. Nie uruchamiałem tego
na EC2.

**Jak szukać zgubionego nawiasu.**
1. Komunikat z 3.10+ wskazuje miejsce **otwarcia**, którego nikt nie zamknął.
   Zacznij tam.
2. Edytor podświetla parę nawiasów, gdy ustawisz kursor przy jednym z nich.
3. Wpisując nowy nawias, od razu dopisuj zamykający i dopiero potem środek.
4. W wyrażeniu na wiele linii rozpisuj po jednym argumencie w linii. Zgubioną
   linię widać wtedy od razu.

## Pułapki

1. **Pusty `{}` to słownik, nie zbiór.** Pusty zbiór to `set()`.
2. **`(5)` to liczba 5, nie krotka.** Krotkę robi przecinek: `(5,)` albo `5,`.
3. **Słownik tworzysz klamrami, czytasz kwadratowymi.** `ceny["kawa"]`, nie
   `ceny{"kawa"}` i nie `ceny("kawa")`.
4. **Przecinek w `[ ]` robi krotkę.** `df["a", "b"]` szuka kolumny o nazwie-krotce.
   Dwie kolumny to `df[["a", "b"]]`.
5. **`&` bez nawiasów wokół warunków** — patrz część o pandas.
6. **`in` znaczy co innego na różnych typach.** `"kaw" in "kawa"` daje `True`
   (fragment tekstu), ale `"kaw" in ["lody", "kawa"]` daje `False` (całe
   elementy listy), a na słowniku `in` sprawdza klucze.
7. **Metoda zmienia obiekt w miejscu.** Po `d = {"a": [1, 2]}` i
   `d["a"].append(3)` słownik ma `{'a': [1, 2, 3]}`: `["a"]` wybrało listę, a
   `.append(3)` dopisało do niej.
8. **Puste kontenery są „fałszem".** `bool([])` daje `False`, a `bool([0])`
   daje `True`. Dlatego `if lista:` znaczy „jeśli lista nie jest pusta".
9. **Cudzysłowy w f-string** — na Pythonie 3.9 (EC2) używaj apostrofów w środku.
10. **Za dużo nawiasów nie szkodzi, za mało tak.** Gdy nie jesteś pewien
    kolejności działań, dopisz nawias.

## Ściąga

| Widzę | To jest |
|---|---|
| `nazwa(...)` | wywołanie funkcji, argumenty w środku |
| `.nazwa(...)` | wywołanie metody na tym, co po lewej |
| `nazwa[...]` | wybór elementu z tego, co po lewej |
| `nazwa[[...]]` | wybór listy kolumn z tabeli (pandas) |
| `nazwa[a:b]` | wycinek: od `a` do `b` bez `b` |
| `nazwa[-1]` | ostatni element |
| `(...)` sam, z przecinkiem | krotka |
| `(...)` sam, bez przecinka | grupa, wymusza kolejność |
| `(... for ... in ...)` | generator |
| `[...]` sam | lista |
| `[... for ... in ...]` | lista składana |
| `{...}` z dwukropkami | słownik |
| `{...}` bez dwukropków | zbiór |
| `{}` pusty | pusty słownik |
| `f"...{x}..."` | f-string, `{ }` wstawia wartość |
| `def nazwa(...)` | nawias z parametrami |
| `lambda x: ...` | funkcja bez nazwy |
| `(lambda ...)(5)` | lambda wywołana od razu |
| `f(*lista)` | lista rozpakowana na osobne argumenty |
| `{**a, **b}` | dwa słowniki sklejone w jeden |

## Jak sprawdzać samemu

Najszybciej w konsoli Pythona: wpisujesz wyrażenie, Enter, widzisz wynik.

1. `[lokalny PowerShell, (.venv) włączone]` W folderze projektu, gdy w wierszu
   jest `(.venv)`, wpisz `python`. Zobaczysz `>>>`.
2. Wpisz wyrażenie, na przykład `len("lody")`, i naciśnij Enter. Zobaczysz
   wynik w następnej linii (dla `len("lody")` będzie to `4`).
3. Żeby wyjść, wpisz `exit()` i Enter. Wróci wiersz z `PS`.

Gdy nie wiesz, czym jest coś, wpisz `type(coś)`. Dla `type(len)` zobaczysz
`<class 'builtin_function_or_method'>`, czyli funkcję: da się ją wywołać `( )`,
ale nie da się z niej wybierać `[ ]`.

## Ćwiczenia

Dane do wszystkich: `napisy = ["lody", "kawa"]`,
`ceny = {"kawa": 12.5, "herbata": 9.0}`,
`dane = {"kawa": {"cena": 12.5, "sztuki": [1, 2, 3]}}`, tabela `df` z części
o pandas. Najpierw odpowiedz sam, potem sprawdź poniżej.

1. `len(napisy[1])`
2. `sorted(napisy[0])` i `sorted(napisy)[0]` — czym się różnią?
3. `type((7))` i `type((7,))`
4. `ceny["kawa"] * 2`
5. `[x * 2 for x in [1, 2, 3, 4] if x > 1]`
6. `{w: len(w) for w in napisy}`
7. `f"{ceny['kawa']}"`
8. `not (True and False)` i `not True and False`
9. `dane["kawa"]["sztuki"][2]`
10. `df[["kawa", "herbata"]].shape`
11. Napraw: `df[df["kawa"] > 1 & df["herbata"] < 6]`
12. Który nawias jest zły w `lista(0)` i jak go poprawić?
13. `max(*[3, 9, 5])`
14. `sorted(ceny.items(), key=lambda kv: kv[1])` — co zwraca i po czym sortuje?
15. Przeczytaj po kolei, krok po kroku: `response.json()["chart"]["result"][0]`
16. `len({})` i `type({})`

### Odpowiedzi

1. **`4`.** `napisy[1]` to `'kawa'`, jej długość to 4.
2. **`['d', 'l', 'o', 'y']`** i **`'kawa'`**. Pierwszy sortuje litery wyrazu
   `'lody'`, drugi sortuje listę wyrazów i bierze pierwszy.
3. **`int`** i **`tuple`**. Przecinek robi krotkę.
4. **`25.0`.**
5. **`[4, 6, 8]`.** Element 1 odpada (warunek `x > 1`), reszta jest podwojona.
6. **`{'lody': 4, 'kawa': 4}`.**
7. **`'12.5'`.**
8. **`True`** i **`False`**. Nawias zmienia to, czego dotyczy `not`.
9. **`3`.** Czytasz: `dane`, klucz `"kawa"`, klucz `"sztuki"`, numer 2.
10. **`(3, 2)`:** trzy wiersze, dwie kolumny.
11. **`df[(df["kawa"] > 1) & (df["herbata"] < 6)]`.** Każdy warunek w osobnym
    nawiasie. Wynik: wiersz o indeksie 1.
12. Zły jest okrągły nawias: lista nie jest funkcją. Poprawnie `lista[0]`.
13. **`9`.** Gwiazdka rozpakowuje listę na `max(3, 9, 5)`.
14. Zwraca **listę par** posortowaną rosnąco po wartości:
    `[('herbata', 9.0), ('kawa', 12.5)]`. `ceny.items()` daje pary
    (klucz, wartość), a `kv[1]` to wartość z pary.
15. Od lewej do prawej: wywołaj `.json()` na `response`; z wyniku wybierz klucz
    `"chart"`; z tego wybierz klucz `"result"`; z tego wybierz element 0.
16. **`0`** i **`<class 'dict'>`** (w skrócie: `'dict'`). Pusty `{}` to słownik.

## Co sprawdzone, a czego nie

- **Sprawdzone 21.09** na Pythonie 3.14.2 z pandas 3.0.5: każdy wynik i każdy
  komunikat błędu w tej notatce.
- **Niesprawdzone na EC2 (Python 3.9):** f-string z tym samym rodzajem
  cudzysłowu w środku (zmiana Pythona 3.12), brzmienie komunikatów o
  niezamkniętym nawiasie (zmiana 3.10), `int | None` w podpowiedziach typów
  (od 3.10). Wszystkie trzy to wiedza z dokumentacji zmian Pythona, nie z
  uruchomienia.
- **Pominięte:** klasy (`class A(Base):`, jeszcze ich nie znasz),
  dekoratory z argumentami (`@pytest.mark.parametrize(...)` to wywołanie w
  dekoratorze), wyrażenia regularne (osobny język).

## Powiązane notatki

- [[Slownik]] — hasło „Nawiasy: trzy rodzaje i trzy pytania", krotka,
  wycinek listy, maska z kilkoma warunkami
- [[Plan-02-silver]] — starszy opis różnicy między `df["a"]` i `df[["a"]]`
- [[Przeglad-2026-09-08-co-nie-gra]]
