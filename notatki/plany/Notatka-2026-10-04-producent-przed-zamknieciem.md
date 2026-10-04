# Notatka 04.10.2026 — Producent nie bierze dzisiejszej świecy przed zamknięciem

Status: **zatwierdzona przez Gracjana 04.10 — wszystkie pięć decyzji w wariancie (a)**
(próg 17:55, osobny plik `kod/sesja.py` z testami `kod/test_sesja.py` — nazwa z przykładu,
dopisek przy pominięciu, sprawdzenie na EC2 ręcznym biegiem i biegiem `cron`, wdrożenie od
wtorku 06.10). Instrukcja przed kodem:
[[Notatka-2026-10-04-jak-napisac-warunek-sesji]]. Naprawa z decyzji 04.10 („naprawić przed
stroną”), czerwona wada z przeglądu 08.09, punkt 2.1.

## Sedno w trzech zdaniach

1. W trakcie sesji Yahoo podaje „dzisiejszą świecę” z bieżącą ceną, a Producent zapisuje ją
   jako kurs zamknięcia z godziną `17:00:00` (08.09 o 16:43: CBF `194.5` zamiast prawdziwego
   zamknięcia).
2. Taka cena trafia do Kafki i S3 **na zawsze**, bo pamięć Producenta zapisuje ten dzień jako
   wysłany i następny bieg go już nie wyśle. Dziś pilnuje tego tylko godzina w `crontab`,
   a każdy ręczny bieg testowy w dzień roboczy przed zamknięciem trafiłby na tę minę.
3. Proponuję prosty warunek: **dopóki w Warszawie nie ma 17:55, Producent pomija dzisiejszą
   datę.** Nie wysyła jej i nie zapisuje w pamięci, więc bieg o 18:00 weźmie ją jako nowy
   dzień, już z prawdziwą ceną.

## Przykład na innych danych: utarg sklepu w zeszycie

Sklep zamyka kasę o 17:00, raport z kasy jest pewny dopiero po 17:15. Kierownik wpisuje do
zeszytu „utarg dnia” i nigdy nie poprawia dnia, który już raz wpisał.

| Kiedy kierownik spisuje | Stan kasy | Zeszyt bez warunku | Zeszyt z warunkiem „dziś dopiero od 17:55” |
|---|---|---|---|
| wtorek 16:30 | 1200 zł, sklep otwarty | wtorek: 1200 zł — na zawsze, a prawdziwy utarg to 1850 zł | wtorek pominięty, w zeszycie go nie ma |
| wtorek 18:00 | 1850 zł, kasa zamknięta | nic, bo wtorek „już był” | wtorek: 1850 zł |
| sobota 10:00 | sklep zamknięty, dnia brak | nic | nic |

| Przykład | Projekt |
|---|---|
| zeszyt, który nie poprawia wpisanych dni | pamięć Producenta `companies/*.txt` + wiadomości w Kafce i pliki w S3 |
| spisanie o 16:30 | ręczny bieg `data_ingestion.py` w dzień roboczy przed zamknięciem |
| spisanie o 18:00 | bieg `cron` o 18:00 |
| warunek „dziś dopiero od 17:55” | nowy warunek w Producencie, liczony w czasie polskim |

## Co wiemy o godzinach (fakty z dziennika)

| Kiedy | Co Yahoo oddało dla dzisiejszego dnia |
|---|---|
| 08.09, 16:43 (sesja trwa) | świecę z bieżącą ceną (CBF `194.5`) — to jest ta wada |
| 11.09, 17:45 | brak świecy albo pusta cena (kod pomija `None`) — bezpieczne |
| codziennie 18:00 (`cron`) | świecę z ceną zamknięcia; 17, 18 i 21.09 zgodne z archiwum GPW |

Sesja kończy się ok. 17:00. Między 17:00 a 18:00 nie wiemy dokładnie, kiedy cena staje się
ostateczna. Pominięcie dnia nic nie kosztuje, bo bieg o 18:00 go weźmie, więc próg może stać
późno.

## Co może pójść źle

- **Strefa czasowa:** EC2 liczy w UTC, laptop w czasie polskim. Warunek musi liczyć godzinę
  jawnie w strefie `Europe/Warsaw`, inaczej na EC2 przesunie się o 2 godziny (zimą o 1).
- **Zmiana czasu 25.10:** przy jawnej strefie warunek sam się dostosuje. Pierwszy dzień
  giełdowy po zmianie (pon. 26.10) trzeba sprawdzić.
- **Próg za blisko `cron`:** `cron` startuje o 18:00:02, próg 17:55 daje 5 minut zapasu. Próg
  równy 18:00 nie dawałby żadnego.
- **Próg za wcześnie** (np. 17:05): Yahoo mogłoby jeszcze nie mieć ostatecznej ceny.
- **Test, który uruchamia cały Producent:** `data_ingestion.py` nie ma części `__main__`, więc
  zaimportowanie go w teście pobrałoby dane i połączyło się z Kafką. Funkcja warunku powinna
  leżeć w osobnym, małym pliku.
- **Ręczny bieg testowy na starym kodzie** w dzień roboczy przed 17:00 zapisałby złą cenę.
  Pierwszy taki test dopiero po wdrożeniu nowego kodu.
- **Producent na laptopie** wysyła do brokera na EC2 (domyślny adres w kodzie), więc ręczny
  bieg z laptopa to prawdziwe wiadomości. Testy na laptopie tylko na funkcji, nie na całym
  Producencie.
- **Blok w logu:** przy biegu z `cron` o 18:00 warunek nic nie robi, więc blok zostaje 28
  linii. Komunikat o pominięciu pojawi się tylko w ręcznym biegu przed 17:55.
- **Kontrola o 18:30:** dalej szuka `stan: zapisane` przy każdej spółce, więc dopisek na końcu
  tej samej linii jej nie psuje.
- **Wdrożenie:** nie w poniedziałek 05.10 (pierwszy dzień giełdowy na Pythonie 3.14) i nie
  w oknie 17:55–18:35. Nowy plik przychodzi z `git pull`, `crontab` bez zmian.
- **Za miesiąc:** nowa spółka i kompakcja bez wpływu. Wada „korekty Yahoo wstecz” zostaje,
  bo to osobna sprawa.

## Jak sprawdzimy

1. **Testy na laptopie** (zmyślone godziny, bez sieci):
   - dzień roboczy 16:30 → pomija dziś;
   - 18:00 → bierze dziś;
   - sobota → nie ma czego pomijać;
   - godzina podana w UTC tuż przed i po progu, latem i zimą (np. 26.10 16:00 UTC = 17:00
     polskiego → pomija, 17:00 UTC = 18:00 polskiego → bierze).
2. **Na EC2 po wdrożeniu, w dzień giełdowy przed 17:55:** ręczny bieg Producenta, bez `>>`.
   Mają być 3 linie z dopiskiem o pominięciu, `nowych dni: 0`, zakładka bez zmian, pamięć bez
   dzisiejszej daty.
3. **Ten sam dzień o 18:00 z `cron`:** `nowych dni: 1` × 3, `Odebrano 3`, kontrola `OK`. To jest
   dowód na prawdziwej drodze, że pominięty dzień przyszedł o 18:00 z ceną zamknięcia.

## Decyzje do podjęcia (rekomendacja Claude'a pierwsza)

1. **Próg:**
   - (a) **17:55**: tuż przed `cron`, zgodny z naszym oknem „nie ruszać 17:55–18:35”;
     pominięcie nic nie kosztuje;
   - (b) 17:30: zostawia pół godziny na ręczny bieg po zamknięciu, ale okno 17:30–18:00
     u Yahoo jest niezbadane;
   - (c) 17:15.
2. **Gdzie funkcja:**
   - (a) **nowy mały plik w `kod/`** (nazwa do wyboru, np. `sesja.py`) z czystą funkcją
     i testami w osobnym pliku testów, jak `path.py`;
   - (b) funkcja w `data_ingestion.py` + część `__main__`, czyli przebudowa wcięć całego pliku,
     który chodzi w `cron`.
3. **Komunikat:**
   - (a) **dopisek na końcu linii spółki tylko przy pominięciu**, np. `…, stan: zapisane,
     dziś pominięte (przed 17:55)`;
   - (b) osobna linia (blok w ręcznym biegu urośnie o 3);
   - (c) bez komunikatu (pominięcie byłoby ciche).
4. **Sprawdzenie na EC2:**
   - (a) **ręczny bieg przed 17:55 w dzień giełdowy i bieg `cron` tego samego dnia**;
   - (b) same testy na laptopie.
5. **Termin wdrożenia:**
   - (a) **od wtorku 06.10**, po zgodnej kontroli poniedziałku, w ciągu dnia przed 17:55;
   - (b) poniedziałek 05.10.
