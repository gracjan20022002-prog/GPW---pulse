import json
import os
import pandas as pd
import pytest
from config import ticker
from data_stream import sprawdz_pliki, zbuduj_dane, wczytaj_poprzednie, zapisz_js
@pytest.fixture
def dzienne():
    return pd.DataFrame({
        "dzien": ["2026-10-22"] * len(ticker) + ["2026-10-23"] * len(ticker),
        "spolka": ticker * 2,
        "cena": [100.0, 200.0, 300.0, 101.0, 202.0, 303.0]
    })
@pytest.fixture
def ranking():
    return pd.DataFrame({
        "spolka": ticker,
        "miesiac": ["2025-01", "2025-02", "2025-03"],
        "ostatnia_cena": [101.0, 202.0, 303.0],
        "zmiana_caly_okres": [10.0, 30.0, 20.0]
    })
@pytest.fixture
def sciezka(tmp_path):
    return os.path.join(tmp_path, "dane.js")
def test_komplet(dzienne, ranking):
    wynik = sprawdz_pliki(dzienne, ranking, ticker, "2026-10-24", 2)
    assert wynik == []
def test_brak_dnia_jednej_spolki(dzienne, ranking):
    wynik = sprawdz_pliki(dzienne.drop(index=0), ranking, ticker, "2026-10-24", 2)
    assert len(wynik) == 1
    assert "różne dni" in wynik[0]
def test_pusta_cena(dzienne, ranking):
    dzienne["cena"]=[100.0, None, 300.0, 101.0, 202.0, 303.0]
    wynik = sprawdz_pliki(dzienne, ranking, ticker, "2026-10-24", 2)
    assert wynik == ["Pusta cena"]
def test_przyszlosc(dzienne, ranking):
    wynik = sprawdz_pliki(dzienne, ranking, ticker, "2026-10-22", 2)
    assert len(wynik) == 1
    assert "przyszłości" in wynik[0]
def test_mniej_sesji(dzienne, ranking):
    wynik = sprawdz_pliki(dzienne, ranking, ticker, "2026-10-24", 3)
    assert wynik == ["Mniej sesji niż poprzednio: 2 < 3"]
def test_ranking_z_innego_dnia(dzienne, ranking):
    ranking["ostatnia_cena"]=[100.0, 202.0, 303.0]
    wynik = sprawdz_pliki(dzienne, ranking, ticker, "2026-10-24", 2)
    assert len(wynik) == 1
    assert ticker[0] in wynik[0]
def test_obca_spolka(dzienne, ranking):
    dzienne["spolka"]=ticker + ticker[:2] + ["ABC.WA"]
    wynik = sprawdz_pliki(dzienne, ranking, ticker, "2026-10-24", 2)
    assert len(wynik) == 1
    assert "ABC.WA" in wynik[0]
def test_powtorzony_dzien(dzienne, ranking):
    dzienne["dzien"]=["2026-10-22"] * 4 + ["2026-10-23"] * 2
    wynik = sprawdz_pliki(dzienne, ranking, ticker, "2026-10-24", 2)
    assert wynik == ["Powtórzony dzień"]
def test_obca_spolka_w_rankingu(dzienne, ranking):
    ranking["spolka"]=ticker[:2] + ["ABC.WA"]
    wynik = sprawdz_pliki(dzienne, ranking, ticker, "2026-10-24", 2)
    assert len(wynik) == 1
    assert "rankingu" in wynik[0]
def test_zbuduj_dane(dzienne, ranking):
    dzienne["cena"]=[100.0, 200.0, 300.0, 101.0, 202.0, 334.20001220703125]
    wynik = zbuduj_dane(dzienne, ranking, ticker)
    assert wynik["daty"] == ["2026-10-22", "2026-10-23"]
    assert wynik["ceny"] == {"CBF": [100.0, 101.0], "XTB": [200.0, 202.0], "SNT": [300.0, 334.2]}
    assert wynik["ranking"][0] == {"spolka": "XTB", "miesiac": "2025-02", "zmiana": 30.0}
    assert wynik["ranking"][2]["spolka"] == "CBF"
def test_wczytaj_brak_pliku(sciezka):
    assert wczytaj_poprzednie(sciezka) == 0
def test_zapisz_js(sciezka):
    zapisz_js({"daty": ["2026-10-22", "2026-10-23"]}, sciezka)
    with open(sciezka, encoding="utf-8") as plik:
        tekst = plik.read()
    assert tekst == 'window.DANE = {"daty": ["2026-10-22", "2026-10-23"]};'
def test_zapisz_i_wczytaj(dzienne, ranking, sciezka):
    zapisz_js(zbuduj_dane(dzienne, ranking, ticker), sciezka)
    assert wczytaj_poprzednie(sciezka) == 2
def test_zapisz_i_nadpisz(sciezka):
    zapisz_js({"daty": ["2026-10-21", "2026-10-22", "2026-10-23"]}, sciezka)
    zapisz_js({"daty": ["2026-10-23"]}, sciezka)
    assert wczytaj_poprzednie(sciezka) == 1
def test_zepsuty_plik(sciezka):
    with open(sciezka, "w", encoding="utf-8") as plik:
        plik.write('window.DANE = {"daty": ["2026-10-22"')
    with pytest.raises(json.JSONDecodeError):
        wczytaj_poprzednie(sciezka)
