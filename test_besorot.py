import pytest
import json
from besorot import getReadings, getYear
import datetime

class TestBesorot:

    def test_can_get_year(self):
        assert getYear(5783) == "A"
        assert getYear(5784) == "B"
        assert getYear(5785) == "C"
        assert getYear(5791) == "C"

    def test_can_get_for_parasha(self):
        assert getReadings("Bereshit", 5783) == "John 1:1-18"

    def test_can_get_reading_by_year(self):
        assert getReadings("Lech-Lecha", 5783) == "Matthew 1:18-25"
        assert getReadings("Lech-Lecha", 5784) == "Luke 2:1-20"
        assert getReadings("Lech-Lecha", 5785) == "John 1:35-51"