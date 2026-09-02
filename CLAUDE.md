# CLAUDE.md — zasady pracy nad projektem GPW Pulse

## Kim jest użytkownik

Gracjan, uczy się data engineeringu. GitHub: `gracjan20022002-prog`.

**Zna:** `if/else`, pętle `for`, listy, słowniki, funkcje `def` z typami,
`try/except`, `logging`, `requests` i API, zapis do plików, list comprehensions,
`lambda`/`map`/`filter`/`zip`, pandas w praktyce (Bronze/Silver/Gold ukończone),
podstawy `matplotlib` (`plot`, `bar`, `savefig`, formatowanie osi), podstawy
Power BI, Harmonogram zadań Windows, podstawy `pytest` (`assert`,
`@pytest.mark.parametrize`).

**Nie zna jeszcze:** klas. AWS/Kafka/Linux — pierwszy raz 19.08, z dużym
prowadzeniem krok po kroku (SSH, EC2, KRaft, Security Groups, PowerShell).

## Zasady — obowiązkowe

1. **Kod i testy projektu pisze Gracjan sam.** Ty tłumaczysz i dajesz
   przykłady na **innych** danych. Kod pomocniczy — tylko na prośbę i za zgodą.
2. **Prosty język.** Krótkie zdania, trudne słowa tłumaczone od razu.
3. **Małe kroki.** Jedna nowa rzecz na sesję (sesja = 1,5–2 h dziennie).
4. **Dokumentacja:** `README.md` **i** dziennik (`notatki/dziennik/`)
   aktualizujesz Ty, na bieżąco, na koniec każdej sesji — Gracjan już
   tego nie robi sam. Szczegóły sesji (błędy, poprawki, decyzje) idą do
   dziennika, **nie tutaj** — ten plik ma zostać krótki (~200–300 słów):
   tylko kto, zasady, aktualny stan.
5. **Terminal i git zawsze robi Gracjan sam.** Ty podajesz dokładne komendy,
   nie wykonujesz ich za niego (poza czytaniem plików/stanu).

## Stan projektu

Repo: folder `GPW - pulse`, GitHub: `github.com/gracjan20022002-prog/GPW---pulse`.

**BRONZE, SILVER, GOLD ukończone.** **Etap 4** — Części A, B, C ukończone,
zostaje **Część D** (domknięcie pod portfolio).

**Etap 5 — migracja do AWS** (`Plan-05-aws-migracja.md`) — EC2
(Kafka+`systemd`, 24/7) → S3 → Glue → Athena → Silver/Gold, w pełni
ukończona i zautomatyzowana. Zbieranie na EC2 (`cron`) i lokalny
Harmonogram — oba **po zamknięciu GPW**, nie o otwarciu (18:00/18:02
i 18:10 polskiego, od 02.09). 02.09: naprawiony błąd duplikatów
w Silver/Gold (posprzątane w S3, nowy test). Zostaje Część E: Power BI
→ Athena (odłożone).

**`Plan-06-domkniecie-i-strona.md`** — domknięcie Części D, strona
internetowa. **Następna sesja:** przeniesienie wykonania Silver/Gold
na EC2.

## Gdzie co jest

Kod, dane i notatki razem w folderze projektu: `kod/`, `companies/`,
`silver/`, `gold/`, `notatki/` (plany, dziennik i `.obsidian` poza gitem,
słownik). Nauka Pythona (osobny, niepowiązany projekt): `DE/Python_l/`.
