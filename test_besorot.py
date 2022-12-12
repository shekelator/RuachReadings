import pytest
import json
from besorot import getReadings, getYear
import datetime

calendarDate = datetime.datetime.now().date
class TestBesorot:

    def test_can_get_year(self):
        assert getYear(5783) == "A"
        assert getYear(5784) == "B"
        assert getYear(5785) == "C"
        assert getYear(5791) == "C"

    def test_can_get_for_parasha(self):
        assert getReadings("Bereshit", 5783, calendarDate) == "John 1:1-18"

    def test_can_get_reading_by_year(self):
        assert getReadings("Lech-Lecha", 5783, calendarDate) == "Matthew 1:18-25"
        assert getReadings("Lech-Lecha", 5784, calendarDate) == "Luke 2:1-20"
        assert getReadings("Lech-Lecha", 5785, calendarDate) == "John 1:35-51"

    def test_can_get_reading_where_all_years_are_the_same(self):
        assert getReadings("Re'eh", 5783, calendarDate) == "Luke 24:33-49"
        assert getReadings("Re'eh", 5784, calendarDate) == "Luke 24:33-49"
        assert getReadings("Re'eh", 5785, calendarDate) == "Luke 24:33-49"

    def test_returns_none_for_unknown_parasha(self):
        assert getReadings("Unknown", 5783, calendarDate) == None

    def test_shabbat_before_christmas(self):
        assert getReadings("Miketz", 5783, datetime.date(2022, 12, 24)) == "Philippians 2:5-11"
        assert getReadings("Vayigash", 5784, datetime.date(2023, 12, 24)) == "Colossians 1:15-20"
        assert getReadings("Vayeshev", 5785, datetime.date(2024, 12, 24)) == "1 John 1:1-4"
        assert getReadings("Miketz", 5786, datetime.date(2025, 12, 24)) == "Philippians 2:5-11"

    def test_most_years_matotmasei_are_combined(self):
        assert getReadings("Balak", 5783, datetime.date(2022, 7, 8)) == "Mark 15:1-15"
        assert getReadings("Pinchas", 5784, datetime.date(2023, 7, 27)) == "Luke 23:26-32"

    def test_years_matotmasei_are_separate(self):
        assert getReadings("Balak", 5795, datetime.date(2035, 7, 14)) == "Mark 15:1-15"
        assert getReadings("Pinchas", 5795, datetime.date(2035, 7, 21)) == "Luke 22:7-20"
