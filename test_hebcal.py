import pytest
import json
import datetime
import requests_mock
import hebcal


class TestHebCal:
    def test_can_get_data(self):
        with requests_mock.Mocker() as m:
            m.get("https://www.hebcal.com/leyning", text=json.dumps({"items": []}))
            resp = hebcal.HebCal().getRawReadingsData("2021-01-01")
            assert resp == []

    def test_returns_cached_data(self):
        with requests_mock.Mocker() as m:
            m.get("https://www.hebcal.com/leyning", text=json.dumps({"items": []}))
            hebCal = hebcal.HebCal()
            resp = hebCal.getRawReadingsData("2021-01-01")
            resp = hebCal.getRawReadingsData("2021-01-01")
            assert m.call_count == 1

    def test_does_not_cache_different_dates(self):
        with requests_mock.Mocker() as m:
            m.get("https://www.hebcal.com/leyning", text=json.dumps({"items": []}))
            hebCal = hebcal.HebCal()
            resp = hebCal.getRawReadingsData("2021-01-01")
            resp = hebCal.getRawReadingsData("2021-02-01")
            assert m.call_count == 2