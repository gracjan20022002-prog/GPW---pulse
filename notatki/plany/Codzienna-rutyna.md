# Codzienna rutyna — od włączenia komputera do pracy

Data utworzenia: 2026-07-21

Zakładam, że **nigdy tego nie robiłeś**. Nic nie pomijam.

---

## CZĘŚĆ A — Jednorazowo, tylko za pierwszym razem

Robisz to raz w życiu dla tego projektu. Potem już nigdy.

### A1. Otwórz VS Code i wskaż mu folder projektu

1. Kliknij ikonę **VS Code**
2. Na górze: **File** → **Open Folder...**
3. Znajdź folder: `Dokumenty` → `DE` → `gpw-pulse-v2`
4. Kliknij **Wybierz folder**
5. Jeśli zapyta „Do you trust the authors?" → kliknij **Yes, I trust the authors**

Po lewej stronie zobaczysz zawartość folderu. Na razie jest tam jeden plik: `CLAUDE.md`.

### A2. Otwórz terminal w VS Code

**Terminal** to czarne okienko, w którym wpisuje się polecenia zamiast klikać.

1. Na górze: **Terminal** → **New Terminal**
2. Na dole ekranu otworzy się czarny pasek

Po prawej stronie tego paska jest napis: `powershell`, `cmd` albo `bash`.
**Powiedz mi, co tam widzisz** — od tego zależą polecenia, które Ci podam.

Poniżej zakładam **PowerShell** (domyślny na Windowsie).

### A3. Zrób środowisko wirtualne

**Co to jest, po ludzku:**

Wyobraź sobie, że każdy projekt to osobna szuflada z narzędziami.
Projekt A potrzebuje młotka w wersji 1. Projekt B potrzebuje młotka w wersji 2.

Bez szuflad wrzucasz oba młotki do jednego pudła i one się kłócą.
Środowisko wirtualne to ta szuflada. **Osobny zestaw bibliotek tylko dla tego projektu.**

Wpisz w terminalu i naciśnij Enter:

```
python -m venv .venv
```

Nic się nie wyświetli. To normalne. Potrwa kilka sekund.
Po lewej pojawi się nowy folder `.venv`. **Nigdy go nie otwieraj i nie edytuj.**

### A4. Włącz środowisko

```
.\.venv\Scripts\Activate.ps1
```

**Jeśli wyskoczy czerwony błąd ze słowem `ExecutionPolicy`** — Windows blokuje skrypty.
Wpisz to raz, potwierdź literą `T` lub `Y`, i spróbuj ponownie:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Skąd wiesz, że zadziałało:** na początku linii w terminalu pojawi się `(.venv)`.
Tak:

```
(.venv) PS C:\Users\gracj\OneDrive\Dokumenty\DE\gpw-pulse-v2>
```

**To `(.venv)` jest najważniejszą rzeczą w całej tej instrukcji.**
Jeśli go nie widzisz — pracujesz poza szufladą i będą problemy.

### A5. Zainstaluj bibliotekę requests

```
pip install requests
```

Poleci dużo tekstu. Na końcu ma być `Successfully installed`.

### A6. Powiedz VS Code, żeby używał tego środowiska

1. Naciśnij `Ctrl` + `Shift` + `P`
2. Wpisz: `Python: Select Interpreter`
3. Naciśnij Enter
4. Z listy wybierz ten, który ma w nazwie `.venv` — zwykle jest pierwszy
   i ma dopisek **Recommended**

---

## CZĘŚĆ B — Codziennie, przed każdą sesją

**To robisz każdego dnia. Zajmuje 30 sekund.**

### Krok 1 — Otwórz VS Code

Kliknij ikonę. VS Code sam otworzy ostatni folder.
Sprawdź po lewej u góry, czy widzisz `GPW-PULSE-V2`.

### Krok 2 — Otwórz terminal

**Terminal** → **New Terminal** (albo skrót: `Ctrl` + `` ` `` — ten znak
jest pod klawiszem Escape).

### Krok 3 — Włącz środowisko

```
.\.venv\Scripts\Activate.ps1
```

**Sprawdź, czy widzisz `(.venv)`.** Jeśli nie — powtórz.

### Krok 4 — Sprawdź, czy nie masz niezapisanych zmian

```
git status
```

- `nothing to commit, working tree clean` → wszystko zapisane, w porządku
- lista plików na czerwono → masz zmiany z wczoraj, których nie wysłałeś

### Krok 5 — Włącz Claude

```
claude
```

Otworzy się rozmowa. **Zawsze zaczynaj od tego zdania:**

> Przeczytaj CLAUDE.md i dziennik z ostatniej sesji. Powiedz mi, na czym skończyliśmy
> i co robimy dzisiaj.

Dzięki temu Claude wie, gdzie jesteśmy, i nie zaczyna od zera.

---

## CZĘŚĆ C — Codziennie, na koniec sesji

**Nie kończ pracy bez tego.** Pięć minut, oszczędza godziny.

### Krok 1 — Zapisz pliki

`Ctrl` + `S` w każdej zakładce. Albo `Ctrl` + `K`, potem `S` — zapisuje wszystkie.

### Krok 2 — Wyślij pracę na GitHub

Trzy polecenia, po kolei:

```
git add .
```
*(zbierz wszystkie zmiany)*

```
git commit -m "opis tego, co dzisiaj zrobiłem"
```
*(zapisz je z opisem — pisz po ludzku, np. „pobieranie cen jednej spółki")*

```
git push
```
*(wyślij na GitHub)*

### Krok 3 — Poproś Claude o notatkę

> Zapisz w CLAUDE.md i w dzienniku, co dzisiaj zrobiliśmy i na czym skończyliśmy.

### Krok 4 — Zamknij Claude

Wpisz `/exit` albo naciśnij `Ctrl` + `D`.

---

## Ściągawka do wydrukowania

**START:**
```
1. VS Code
2. Terminal → New Terminal
3. .\.venv\Scripts\Activate.ps1     ← sprawdź (.venv)
4. git status
5. claude
```

**KONIEC:**
```
1. Ctrl+S
2. git add .
3. git commit -m "co zrobiłem"
4. git push
5. poproś Claude o notatkę
```

---

## Gdy coś nie działa

| Co widzisz | Co to znaczy | Co zrobić |
|---|---|---|
| Brak `(.venv)` | środowisko wyłączone | powtórz krok 3 |
| `python nie jest rozpoznawany` | Windows nie widzi Pythona | napisz do mnie, poprawimy ustawienia |
| `ExecutionPolicy` | Windows blokuje skrypty | polecenie z punktu A4 |
| `claude nie jest rozpoznawany` | Claude Code nie w tym terminalu | zamknij i otwórz terminal ponownie |
| `rejected` przy `git push` | ktoś zmienił coś na GitHubie | najpierw `git pull`, potem `git push` |
| `fatal: not a git repository` | jesteś w złym folderze | sprawdź ścieżkę w terminalu |

**Zasada:** jak nie wiesz, co się dzieje — skopiuj **cały** czerwony tekst
i wklej mi go. Nie streszczaj. Komunikaty błędów mówią dokładnie, co jest nie tak.

---

## Powiązane notatki

- [[Plan-01-bronze]] — co robić na kolejnych sesjach
- [[Slownik]] — trudne słowa
