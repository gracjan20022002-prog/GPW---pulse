import pandas as pd
from datetime import date
from config import ticker
from path import sprawdz_daty
def test_brak_spolki_we_wtorek():
    df = pd.DataFrame({
        "spolka": ticker + ticker[1:],
        "data": ["2026-09-21 17:00:00"] * len(ticker) + ["2026-09-22 17:00:00"] * (len(ticker)-1)})
    wynik = sprawdz_daty(df, ticker, date(2026, 9, 22))
    assert len(wynik) == 2
    assert ticker[0] in wynik[0]
def test_sobota():
    df = pd.DataFrame({
        "spolka": ticker * 2,
        "data": ["2026-09-24 17:00:00"] * len(ticker) + ["2026-09-25 17:00:00"] * len(ticker)
    })
    wynik = sprawdz_daty(df, ticker, date(2026, 9, 26))
    assert wynik == []
def test_przyszlosc():
    df = pd.DataFrame({
        "spolka": ticker * 2 + [ticker[1]],
        "data": ["2026-09-21 17:00:00"] * len(ticker) + ["2026-09-22 17:00:00"] * len(ticker) + ["2026-09-23 17:00:00"]
    })
    wynik = sprawdz_daty(df, ticker, date(2026, 9, 22))
    assert len(wynik) ==2
    assert ticker[1] in wynik[0]
    assert "przyszłości" in wynik[0]
def test_rozna_liczba_dni():
    df = pd.DataFrame({
        "spolka": ticker * 2 + [ticker[0]],
        "data": ["2026-09-21 17:00:00"] * len(ticker) + ["2026-09-22 17:00:00"] * len(ticker) + ["2026-09-18 17:00:00"]
    })
    wynik = sprawdz_daty(df, ticker, date(2026, 9, 22))
    assert len(wynik) == 1
    assert ticker[0] in wynik[0]
def test_komplet_wtorek():
    df = pd.DataFrame({
        "spolka": ticker * 2,
        "data": ["2026-09-21 17:00:00"] * len(ticker) + ["2026-09-22 17:00:00"] * len(ticker)
    })
    wynik = sprawdz_daty(df, ticker, date(2026, 9, 22))
    assert wynik == []
def test_komplet_poniedzialek():
    df = pd.DataFrame({
        "spolka": ticker * 2,
        "data": ["2026-09-18 17:00:00"] * len(ticker) + ["2026-09-21 17:00:00"] * len(ticker)
    })
    wynik = sprawdz_daty(df, ticker, date(2026, 9, 21))
    assert wynik == []

def test_brak_spolki_w_sobote():
    df = pd.DataFrame({
        "spolka": ticker[1:] * 2,
        "data": ["2026-09-24 17:00:00"] * (len(ticker)-1) + ["2026-09-25 17:00:00"] * (len(ticker)-1)
    })
    wynik = sprawdz_daty(df, ticker, date(2026, 9, 26))
    assert len(wynik) == 1
    assert ticker[0] in wynik[0]
