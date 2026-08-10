# CLAUDE.md — zasady pracy nad projektem GPW Pulse

## Kim jest użytkownik

Gracjan, uczy się data engineeringu. GitHub: `gracjan20022002-prog`.

**Zna:** `if/else`, pętle `for`, listy, słowniki, funkcje `def` z typami,
`try/except`, `logging`, `requests` i API, zapis do plików, list comprehensions,
`lambda`/`map`/`filter`/`zip`, pandas w praktyce (Bronze/Silver/Gold ukończone),
podstawy `matplotlib` (`plot`, `bar`, `savefig`, formatowanie osi).

**Nie zna jeszcze:** klas, testów jednostkowych, narzędzi BI (Power BI/
Databricks), automatyzacji/harmonogramów.

## Zasady — obowiązkowe

1. **Kod i testy projektu pisze Gracjan sam.** Ty tłumaczysz i dajesz
   przykłady na **innych** danych. Kod pomocniczy — tylko na prośbę i za zgodą.
2. **Prosty język.** Krótkie zdania, trudne słowa tłumaczone od razu.
3. **Małe kroki.** Jedna nowa rzecz na sesję (sesja = 1,5–2 h dziennie).
4. **Dokumentacja:** `README.md` aktualizujesz Ty, na bieżąco, na koniec
   każdej sesji. Szczegóły sesji (błędy, poprawki, decyzje) idą do dziennika
   Obsidiana, **nie tutaj** — ten plik ma zostać krótki (~200–300 słów):
   tylko kto, zasady, aktualny stan.
5. **Terminal i git zawsze robi Gracjan sam.** Ty podajesz dokładne komendy,
   nie wykonujesz ich za niego (poza czytaniem plików/stanu).

## Stan projektu

Repo: folder `GPW - pulse`, GitHub: `github.com/gracjan20022002-prog/GPW---pulse`.

**Etapy BRONZE, SILVER, GOLD ukończone** — dane w `companies/`, `silver/`,
`gold/`. Pełna historia sesji: dziennik (`notatki/dziennik/`, lokalnie) i
`README.md` (na GitHubie).

**W toku: Etap 4** (plan żywy, rośnie na bieżąco:
`notatki/plany/Plan-04-pokazanie-wyniku.md`). **Część A (wykresy w Pythonie,
`matplotlib`) ukończona** — `kod/wykresy.py`, `kod/ranking.py`, wynik
w `wykresy/`. Dalej: Część B (Power BI), Część C (wstęp do automatyzacji
pobierania danych), Część D (domknięcie pod portfolio). Databricks — osobny,
późniejszy krok, nie część Etapu 4.

## Gdzie co jest

Kod, dane i notatki razem w folderze projektu: `kod/`, `companies/`,
`silver/`, `gold/`, `notatki/` (plany, dziennik i `.obsidian` poza gitem,
słownik). Nauka Pythona (osobny, niepowiązany projekt): `DE/Python_l/`.
