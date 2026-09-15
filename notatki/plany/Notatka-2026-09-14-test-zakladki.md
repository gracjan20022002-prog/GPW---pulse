# Notatka projektowa — test „zakładki nie ma"

Napisana 14 września 2026, przed testem. **Status: zatwierdzona 14 września.**
Wszystkie cztery decyzje zgodnie z rekomendacją, z jedną zmianą terminu
(decyzja 1).

**Wykonany 14 września około 18:30, zaraz po wieczornym odczycie.**

| Co | Oczekiwane | Wyszło |
|---|---|---|
| najstarsza wiadomość | 2327 | 2327 |
| Konsument | `Odebrano 15 wiadomości` | tak |
| zakładka po biegu | 2342 | 2342 |
| S3 `live/` | +1 plik na spółkę | 24 → 27 |
| plik CBF | 5 dni, 8–14 września | znak w znak |
| Silver | bez zmian | lokalnie `(2313, 3)`, plik identyczny co do bajta |

Nowe pliki w S3 są bajt w bajt sklejeniem pięciu dziennych plików spółki
(CBF 406 + 4 znaki nowej linii = 410 bajtów, SNT 421, XTB 436).

**Pomyłka w przewidywaniu.** Zaraz po biegu `--describe` pokazał jeszcze
członka grupy zamiast `no active members`. Konsument kończy bez
`consumer.close()`, więc broker trzyma go na liście kilkanaście sekund. Po
minucie było już `no active members`. W lodziarni: kucharz wyszedł bez „do
widzenia" i przez chwilę jeszcze figuruje na liście obecnych.

~~**Zostało:** bieg `cron` 15 września ma pokazać `(2316, 3)` na samym EC2.~~
**Potwierdzone 15 września, odczyt po 18:15:** na EC2 dwa razy `(2316, 3)`
(2313 + 3 nowe dni, powtórki z testu nie dodały wiersza), `Odebrano 3
wiadomości`, zakładka `2345 2345 0` i `no active members`. Brakuje tylko
sygnału awarii, jak przy każdej naprawie.

---

## Sedno w trzech zdaniach

Konsument pamięta, dokąd doczytał wiadomości w Kafce. To jest **zakładka**.
Od 8 września, gdy zakładka zginie, Konsument ma zacząć od **najstarszej**
wiadomości, która jeszcze leży w Kafce (`earliest`), zamiast po cichu
pominąć wszystko, czego nie przeczytał (`latest`). **Nigdy nie
sprawdziliśmy, czy tak się naprawdę dzieje.** Test to sprawdzi: celowo
skasujemy zakładkę i zobaczymy, co Konsument zrobi.

---

## Na innym przykładzie: tablica zamówień w lodziarni

**Wejście.** Na tablicy wiszą kartki z zamówieniami. Najstarsze ktoś po
kilku dniach zdejmuje.

| Kartka | Zamówienie |
|---|---|
| 7 | waniliowe |
| 8 | czekoladowe |
| 9 | truskawkowe |
| 10 | pistacjowe |

Kucharz wczoraj zrobił 7 i 8. Na karteczce-zakładce zapisał: „następna: 9".
W nocy **zakładka zginęła**. Rano kucharz musi zdecydować, od której
kartki zacząć.

**Wyjście — dwie reguły:**

| Reguła | Od której kartki zaczyna | Co zrobi | Skutek |
|---|---|---|---|
| `latest`: „od teraz" | od następnej nowej, czyli 11 | nic z tego, co wisi | 9 i 10 **nigdy nie zrobione**, nikt tego nie zauważy |
| `earliest`: „od najstarszej" | od 7 | 7, 8, 9, 10 | 9 i 10 zrobione, a 7 i 8 **drugi raz** |

Przy `earliest` nic nie ginie. Są za to powtórki. Nie szkodzą, bo kasa
liczy każde zamówienie tylko raz:

| Kucharz oddał | Kasa policzyła |
|---|---|
| 7, 8, 7, 8, 9, 10 | 7, 8, 9, 10 |

---

## Jak to wygląda u nas

| Lodziarnia | Nasz projekt |
|---|---|
| tablica zamówień | topic `gpw_tracker` w Kafce |
| kartka | jedna wiadomość: cena jednej spółki z jednego dnia |
| zdejmowanie starych kartek | broker kasuje wiadomości po 7–14 dniach |
| kucharz | Konsument, `kod/kafka_consumer.py` |
| zakładka | pozycja grupy `gpw_consumer`, zapisywana na końcu biegu |
| kasa liczy raz | Silver usuwa powtórzone dni (`UNION` i `drop_duplicates`) |

**Kiedy zakładka może zginąć naprawdę:**
- Konsument nie ruszy przez ponad 7 dni, na przykład gdy EC2 jest wyłączone;
- ktoś skasuje grupę albo zmieni jej nazwę w kodzie.

---

## Dlaczego dopiero teraz

Do dziś na naszej „tablicy" wisiała sterta z 1 września: około 2300
wiadomości, czyli zalew. Gdybyśmy wcześniej skasowali zakładkę, Konsument
przerobiłby całą stertę drugi raz.

**Dziś około 18:00–18:05 broker zdejmuje tę stertę.** Zostaje 15 wiadomości:
3 spółki × 5 dni (8, 9, 10, 11 i 14 września). Najstarsza będzie miała
numer **2327**. Test przeczyta dokładnie te 15.

Termin jest ograniczony. Około 21 września broker zdejmie kolejną paczkę
i liczby trzeba będzie policzyć od nowa.

---

## Plan testu w skrócie

Dokładne komendy dostaniesz po zatwierdzeniu.

1. **Sprawdzamy tablicę:** najstarsza wiadomość ma numer 2327. Inny numer
   oznacza koniec testu.
2. **Zapisujemy stan przed testem:** zakładka na 2342, liczba plików
   w S3 `live/`.
3. **Kasujemy grupę `gpw_consumer`**, a razem z nią zakładkę.
4. **Uruchamiamy Konsumenta ręcznie.**
5. **Sprawdzamy wynik**, a wieczorem jeszcze zwykły bieg `cron`.

## Co ma wyjść

| Co | Oczekiwane | Co to znaczy |
|---|---|---|
| Konsument | `Odebrano 15 wiadomości` | zaczął od najstarszej, czyli `earliest` działa |
| zakładka po biegu | 2342 | zapisał nową zakładkę |
| S3 `live/` | po 1 nowym pliku na spółkę, w każdym 5 dni | powtórki trafiły do S3 |
| wieczorem Silver | `(2316, 3)`, jak bez testu | powtórki niczego nie zepsuły |

Jak czytać złe wyniki:
- `Odebrano 0` znaczy, że zakładka nie została skasowana;
- więcej wierszy w Silverze znaczy, że powtórki przeszły.

---

## Co może pójść źle

- **Sterta z 1 września nadal wisi** (numer 22 zamiast 2327). Konsument
  wlałby 2300 powtórek. *Chroni:* krok 1.
- **Test w tej samej chwili co `cron` o 18:00.** Dwa Konsumenty naraz
  i liczby się rozjadą. *Chroni:* kończymy przed 17:50.
- **Ręczny bieg bez `KAFKA_BOOTSTRAP=localhost:9094`.** Konsument nie
  połączy się z brokerem i pokaże błąd. Nic się nie psuje: wieczorny `cron`
  sam przeczyta od najstarszej wiadomości.
- **Literówka w nazwie grupy.** Nic się nie skasuje. *Wykryje to*
  `Odebrano 0`.
- **Za miesiąc:** w `live/` zostaną 3 pliki z powtórkami. Kompakcja
  1 października je odsieje i skasuje. Wypisze tylko o 3 pliki więcej
  w `Usunięto N plików`.

---

## Decyzje do zatwierdzenia

1. **Kiedy.** Jutro, 15 września, z końcem przed 17:50. Wieczorny bieg tego
   samego dnia od razu pokaże, że powtórki nic nie zmieniły.
   *Inaczej:* jutro po 18:15, wtedy ten dowód przyjdzie dzień później.
   **Polecam: przed 17:50.**
   **Decyzja Gracjana:** być może dziś, zaraz po wieczornym odczycie,
   ale tylko jeśli wszystko w odczycie się zgodzi, a tablica pokaże 2327.
   Inaczej jutro przed 17:50. Liczba `Odebrano 15` jest w obu terminach ta
   sama. Przy teście dziś dowód z Silvera przyjdzie jutro o 18:10,
   z `(2316, 3)`.
2. **Sprawdzenie tablicy już dziś po 18:15.** Jedna komenda tylko do
   odczytu. Potwierdzi, że sterta zniknęła.
   **Polecam: tak.**
3. **Jak usunąć zakładkę.** Skasować całą grupę. Druga droga to przestawić
   zakładkę na początek, ale wtedy zakładka dalej istnieje i `earliest`
   w ogóle się nie włączy.
   **Polecam: skasować grupę.**
4. **Gdzie pisze ręczny bieg.** Na ekran, żeby `errors.txt` zawierał tylko
   biegi `cron`.
   **Polecam: na ekran.**

---

## Osobna sprawa, zauważona przy okazji

Nie jest częścią testu i **nie jest sprawdzona**.

Biblioteka Kafki w Pythonie domyślnie **sama** przesuwa zakładkę co
5 sekund. Nasz Konsument zapisuje wiadomości do S3 dopiero po takim
5-sekundowym czekaniu. Może więc przesunąć zakładkę, **zanim** wiadomości
trafią do S3. Gdyby zapis do S3 się wtedy wywrócił, wiadomości byłyby
„przeczytane", a w S3 by ich nie było.

W lodziarni: kucharz odhacza zamówienie, zanim lody wyjdą z kuchni.

**Propozycja:** dopisać to do przeglądu jako osobny punkt i sprawdzić
osobno.
