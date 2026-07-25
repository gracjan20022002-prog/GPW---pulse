# Stare repo `gpw-pulse` — co to za pliki i po co były

Data utworzenia: 2026-07-21

To repozytorium **zostaje jako podgląd**. Nie pracujemy w nim.
Ta notatka tłumaczy, co tam jest — żebyś wiedział, na co patrzysz,
i żeby te nazwy przestały być straszne.

**Ważne:** to jest opis „jak wygląda duży, dojrzały projekt".
Ty **nie musisz** mieć tego wszystkiego. Większość z tych plików w Twoim
nowym projekcie pojawi się dopiero za kilka tygodni albo wcale.

---

## Wyjaśnienie nazw, których nie znałeś

Zanim przejdziemy do plików — cztery słowa, które się powtarzają.

**`src`** — skrót od *source*, czyli „źródło". Folder, w którym leży
właściwy kod programu. Umowa, którą stosuje cały świat.
Po polsku byłoby `kod`.

**`config`** — skrót od *configuration*, czyli „ustawienia".
Miejsce na rzeczy, które chcesz zmieniać bez grzebania w kodzie.
Na przykład listę spółek.

**`ingestion`** — po angielsku „połykanie", „przyjmowanie".
W świecie danych: **pobieranie danych ze źródła**.
Po polsku powiedzielibyśmy `pobieranie`.

**`transform`** — „przekształcanie". Wszystko, co dzieje się z danymi
po pobraniu: czyszczenie, liczenie, układanie.
Po polsku `przetwarzanie`.

---

## Plik po pliku

### `README.md`

Wizytówka projektu. **Pierwsza rzecz, którą widzi każdy** na GitHubie.
Opisuje, co projekt robi i jak go uruchomić.

**Czy potrzebny Ci teraz?** Tak, ale krótki. Trzy zdania wystarczą na start.

---

### `CLAUDE.md`

Instrukcja dla mnie i dla innych narzędzi AI. Zasady współpracy, Twój poziom,
stan projektu. Dzięki temu nie zaczynamy każdej rozmowy od zera.

**Czy potrzebny?** Tak, już go masz w nowym projekcie.

---

### `.gitignore`

Lista rzeczy, których **nie wysyłamy na GitHub**.

Po co? Bo nie wszystko powinno tam trafić:
- hasła i klucze — nigdy
- pobrane dane — czasem gigabajty, a GitHub to nie dysk na dane
- folder `.venv` — każdy robi swój własny

**Czy potrzebny?** Tak, od pierwszego dnia. Bez niego łatwo przypadkiem
wysłać hasło do internetu.

---

### `.env.example`

`.env` to plik z hasłami i kluczami do serwisów. **Nigdy nie trafia na GitHub.**

Ale ktoś, kto pobierze Twój projekt, musi wiedzieć, jakich haseł potrzebuje.
Dlatego obok robi się `.env.example` — ten sam plik, ale z pustymi
albo fałszywymi wartościami. Sam wzór, bez treści.

**Czy potrzebny?** Dopiero gdy zaczniesz używać czegoś z hasłem.
stooq.pl nie wymaga hasła, więc na razie **nie**.

---

### `pyproject.toml`

Dowód osobisty projektu. Nazwa, wersja, lista bibliotek, których używa.

**Czy potrzebny?** Nie teraz. Na start wystarczy prostszy plik `requirements.txt` —
zwykła lista bibliotek, jedna w każdej linii. Zrobimy go w etapie 1.

---

### `config/companies.yaml`

Lista spółek. YAML to format do zapisywania ustawień — czytelniejszy
dla człowieka niż inne formaty.

**Idea jest dobra:** dodanie spółki to dopisanie linijki w pliku ustawień,
a nie zmiana w kodzie.

**Czy potrzebny?** Nie na start. W etapie 1 lista trzech spółek może być
zwykłą listą na górze pliku z kodem. Do osobnego pliku przeniesiemy ją,
gdy spółek będzie dwadzieścia.

---

### `config/settings.yaml`

Wszystkie pokrętła projektu: gdzie zapisywać dane, od kiedy pobierać historię,
jaki model AI, ile wynosi limit prób.

**Czy potrzebny?** Nie teraz. To rozwiązanie problemu, którego jeszcze nie masz.

---

### `src/ingestion/` — pobieranie

Pięć plików: `espi.py`, `prices.py`, `fundamentals.py`, `calendar.py`, `cli.py`.
Każdy pobiera co innego.

**`prices.py`** to jedyny, który Cię teraz dotyczy — pobieranie cen akcji.
To jest dokładnie zadanie z [[Plan-01-bronze]].

`cli.py` to sposób uruchamiania programu z terminala poleceniem
zamiast klikania. Przydatne, ale później.

---

### `src/transform/` — przetwarzanie

`bronze.py`, `silver.py`, `gold.py`, `quality.py`.

Te trzy pierwsze to **trzy etapy obróbki danych**, opisane w [[Plan-ogolny]]:
surowe → czyste → policzone.

`quality.py` sprawdza, czy dane mają sens — czy nie ma duplikatów,
czy cena nie jest ujemna. Ważna rzecz, ale w etapie 2 albo 3.

---

### `src/ai/` — sztuczna inteligencja

`classifier.py` (rozpoznawanie typu raportu), `rag.py` (wyszukiwanie po znaczeniu),
`agent.py` (odpowiadanie na pytania), `prompts.py` (polecenia dla modelu).

**Czy potrzebne?** To miesiąc trzeci albo czwarty. Zupełnie nie teraz.

---

### `src/utils/` — narzędzia pomocnicze

`config.py` (czytanie ustawień), `logging.py` (zapisywanie, co się dzieje),
`io.py` (zapis i odczyt plików), `dates.py` (obsługa dat).

*utils* to skrót od *utilities* — „narzędzia". Drobiazgi używane w wielu miejscach,
zebrane w jednym pliku, żeby nie przepisywać ich w kółko.

**Czy potrzebne?** Nie na start. Takie pliki powstają **naturalnie**, gdy zauważysz,
że piszesz to samo trzeci raz. Robienie ich z góry to odwrotna kolejność.

---

### `sql/gold_schema.sql`

Projekt tabel w bazie danych. Opis, jakie tabele powstaną i jakie będą miały kolumny.

**Czy potrzebny?** Dopiero przy bazie danych. My na start używamy plików CSV.
Ale zajrzyj tam w etapie 3 — zobaczysz, jak się planuje tabele.
Twój kurs SQL bardzo się tu przyda.

---

### `tests/`

Programy sprawdzające inne programy.

**To był mój błąd.** Napisałem je za Ciebie, gotowe, żebyś tylko uzupełniał kod
pod nie. Powiedziałeś, że tak nie chcesz — i masz rację.
Test do własnego kodu piszesz sam, **po** napisaniu kodu.

W nowym projekcie tego nie będzie.

---

### `.github/workflows/ci.yml`

Robot na serwerze GitHuba. Po każdym wysłaniu kodu sam sprawdza,
czy wszystko się uruchamia.

**Czy potrzebny?** Miesiąc drugi. Fajna rzecz do portfolio,
ale najpierw musi być co sprawdzać.

---

### `docs/`

Dokumentacja: `gpw_pulse_brief_v2.md` (opis pomysłu),
`etap2_setup.md` (instrukcja uruchomienia), `research_design.md` (stary,
z czasów gdy projekt był powiązany z pracą magisterską).

**Czy potrzebne?** Tę rolę przejmuje teraz Twój sejf w Obsidianie.

---

### `notebooks/`

Miejsce na notatniki Jupyter — pliki, gdzie kod pisze się małymi kawałkami
i od razu widzi wynik pod spodem. Dobre do zabawy z danymi.

**Czy potrzebne?** Poznasz je w etapie 2, przy pandas. Będą bardzo pomocne.

---

## Jedno zdanie podsumowania

To repozytorium pokazuje, **do czego dojdziemy za kilka miesięcy**.

Nie jest wzorem do przepisania. Powstało za wcześnie i dlatego było
dla Ciebie niezrozumiałe — nie dlatego, że czegoś nie umiesz.

W nowym projekcie **każdy plik pojawi się dopiero wtedy, gdy będziesz umiał
powiedzieć, po co on jest.**

---

## Powiązane notatki

- [[Plan-ogolny]]
- [[Plan-01-bronze]]
- [[Slownik]]
