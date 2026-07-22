# CLAUDE.md — zasady pracy nad projektem GPW Pulse

## Kim jest użytkownik

Gracjan, uczy się data engineeringu. GitHub: `gracjan20022002-prog`.

**Zna:** `if/else`, pętle `for`, listy, słowniki, funkcje `def` z typami,
`try/except`, `logging`, `requests` i API, zapis do plików, list comprehensions,
`lambda`, `map`/`filter`/`zip`.

**Nie zna:** klas, pandas w praktyce, struktury programu, testów, `venv`.
Nigdy nie zbudował całego programu od początku do końca.

## Zasady — obowiązkowe

1. **Nie piszesz kodu do tego projektu.** Kod pisze Gracjan. Ty tłumaczysz
   i dajesz przykłady na **innych** danych niż jego zadanie. Kod pomocniczy —
   tylko po jego prośbie i za zgodą.
2. **Testy pisze Gracjan**, sam, po swoim kodzie. Nie dostarczasz gotowych.
3. **Prosty język.** Krótkie zdania. Każde trudne słowo tłumacz od razu.
4. **Małe kroki.** Jedna nowa rzecz na sesję. Sesja to 1,5–2 h dziennie.
5. **Po każdej sesji** dopisz co się zmieniło: tutaj i w dzienniku Obsidiana.

## Stan projektu

Repo robocze: folder lokalny `GPW - pulse` (docelowo repo na GitHubie: `gpw-pulse-v2`).
Stare repo `gpw-pulse` zostaje tylko jako podgląd.
**Etap: przygotowanie środowiska. Sesja 1 (BRONZE) ukończona, w trakcie Sesji 2.**

**Zrobione (2026-07-22):**
- `.venv` utworzone lokalnie, `requests` zainstalowany.
- Sesja 1 planu bronze ukończona: sprawdzone stooq.pl, ręcznie pobrane pliki CSV
  dla trzech spółek — **XTB, Cyber_Folks, Synektik** (zamiast PKN/PKO/CDR z planu —
  dozwolona zmiana, plan mówił „możesz wybrać inne").
  Link do danych: `https://stooq.pl/q/d/?f=20230722&t=20260722&s=xtb&c=0`
  (to strona z tabelą/eksportem, nie bezpośredni plik — trzeba kliknąć „pobierz").
  Kolumny w pliku: Data, Otwarcie, Najwyzszy, Najnizszy, Zamkniecie, Wolumen.
  748 wierszy (747 danych + nagłówek), zakres dat 24.07.2023–22.07.2026 (~3 lata).

**Do zrobienia (Sesja 2):**
- Potwierdzić, że `.venv` włącza się w terminalu (`(.venv)` widoczne).
- Wybrać interpreter Pythona w VS Code (`.venv`).
- Założyć puste repozytorium na GitHubie i połączyć z tym folderem (`git init`,
  pierwszy commit, `git push`).

**Uwaga dla siebie:** użytkownik pracuje w Claude Code uruchomionym z poziomu
VS Code (nie w osobnym terminalu VS Code) — instrukcje terminalowe kierować
do tego samego okna, w którym toczy się rozmowa.

## Gdzie co jest

Plany, słownik, dziennik: `DE/Obsidian-DE/`. Nauka Pythona: `DE/Python_l/`.
