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

Repo robocze: folder lokalny `GPW - pulse`, połączony z repozytorium na GitHubie:
`https://github.com/gracjan20022002-prog/GPW---pulse`.
Stare repo `gpw-pulse` zostaje tylko jako podgląd.
**Etap: przygotowanie środowiska. Sesja 1 i Sesja 2 (BRONZE) ukończone.**

**Zrobione (2026-07-22):**
- `.venv` utworzone lokalnie, `requests` zainstalowany.
- Sesja 1: sprawdzone stooq.pl, ręcznie pobrane pliki CSV dla trzech spółek —
  **XTB, Cyber_Folks, Synektik** (zamiast PKN/PKO/CDR z planu — dozwolona
  zmiana, plan mówił „możesz wybrać inne"). Pliki w `companies/`
  (`xtb_d.csv`, `cbf_d.csv`, `snt_d.csv`).
  Link do danych: `https://stooq.pl/q/d/?f=20230722&t=20260722&s=xtb&c=0`
  (to strona z tabelą/eksportem, nie bezpośredni plik — trzeba kliknąć „pobierz").
  Kolumny w pliku: Data, Otwarcie, Najwyzszy, Najnizszy, Zamkniecie, Wolumen.
  748 wierszy (747 danych + nagłówek), zakres dat 24.07.2023–22.07.2026 (~3 lata).
- Sesja 2: `.gitignore` (wyklucza `.venv/`), `git init`, pierwszy commit,
  repozytorium `GPW---pulse` założone na GitHubie i połączone (`git remote add origin`,
  `git push -u origin main`) — **udało się, dane są na GitHubie.**

**Do zrobienia (Sesja 3):**
- Napisać program, który pobiera dane **jednej** spółki przez `requests`
  i wypisuje je na ekran (jeszcze bez zapisu do pliku).

**Ważna zasada pracy (potwierdzona 2026-07-22):** Gracjan robi **wszystko sam** —
nie tylko kod Pythona, ale też komendy gita i terminala. Ja tłumaczę i podaję
dokładne polecenia do wpisania, nie wykonuję ich za niego (poza czytaniem
plików/stanu, żeby wiedzieć, co się dzieje).

## Gdzie co jest

Plany, słownik, dziennik: `DE/Obsidian-DE/`. Nauka Pythona: `DE/Python_l/`.
