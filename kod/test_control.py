import os
from config import ticker
from control import sprawdz_blok, wytnij_blok
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, "kod", "dane_testowe", "blok_2026-09-18.txt"), encoding = "utf-8") as plik:
    WZOR = plik.read()
def test_zwykly_dzien():
    assert len(sprawdz_blok(WZOR, ticker, "2026-09-18")) == 0
def test_sobota():
    blok = WZOR.replace("nowych dni: 1, wysłane: 1", "nowych dni: 0, wysłane: 0").replace("Odebrano 3", "Odebrano 0")
    wynik = sprawdz_blok(blok, ticker, "2026-09-18")
    assert len(wynik) == 0
def test_martwy_broker():
    blok = WZOR.replace("stan: zapisane", "stan: nietknięte")
    wynik = sprawdz_blok(blok, ticker, "2026-09-18")
    assert len(wynik) == 3
def test_bez_odebrano():
    blok = WZOR.replace("Odebrano 3 wiadomości", "")
    wynik = sprawdz_blok(blok, ticker, "2026-09-18")
    assert len(wynik) == 1
def test_blad_yahoo_xtb():
    blok = WZOR.replace("XTB.WA: nowych dni: 1, wysłane: 1, stan: zapisane", "XTB.WA: Brak odczytu")
    wynik = sprawdz_blok(blok, ticker, "2026-09-18")
    assert len(wynik) == 1
    assert "XTB.WA" in wynik[0]
def test_martwy_gold():
    blok = WZOR.replace("S3: wysłano dane_dzienne.csv\nS3: wysłano ranking.csv", "Traceback (most recent call last):")
    wynik = sprawdz_blok(blok, ticker, "2026-09-18")
    assert len(wynik) == 2
def test_bieg_nie_z_dzis():
    wynik = sprawdz_blok(WZOR, ticker, "2026-09-19")
    assert len(wynik) == 1
def test_pusty_tekst():
    blok = ""
    wynik = sprawdz_blok(blok, ticker, "2026-09-18")
    assert len(wynik) == 6
def test_dwa_dni():
    log = WZOR.replace("2026-09-18", "2026-09-17") + "\n" + WZOR
    blok = wytnij_blok(log)
    linie = blok.splitlines()
    assert len(linie) == 28 
    assert "2026-09-17" not in blok
def test_powtorna_kontrola():
    log = WZOR.replace("Odebrano 3 wiadomości", "") + "\nKontrola: AWARIA - Konsument nie ukończył zadania: Brak linii 'Odebrano'"
    blok = wytnij_blok(log)
    wynik = sprawdz_blok(blok, ticker, "2026-09-18")
    assert len(wynik) == 1
def test_bez_startu():
    assert wytnij_blok("jakaś linia\ndruga linia") == ""