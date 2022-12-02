import pytest
import json
import readings
import datetime

@pytest.fixture()
def hebCalData():
    with open('ex.json', 'r', encoding="utf8") as reader:
        yield json.load(reader)['items']

class TestReadings:

    def test_can_run(self):
        assert 1 == 1

    def test_can_read_items(self, hebCalData):
        assert len(hebCalData) > 1

    def test_can_create_service(self, hebCalData):
        services = list(map(lambda x: readings.Service().fromDict(x), hebCalData))
        assert services[0].date == datetime.date(2022, 11, 3)
        assert services[1].date == datetime.date(2022, 11, 5)
        assert services[1].name == "Lech-Lecha"

    def test_can_get_services(self, hebCalData):
        services = list(readings.getReadings(hebCalData))
        assert services[0].name == "Lech-Lecha"
        assert services[0].date == datetime.date(2022, 11, 5)
        assert services[0].isShabbat == True
        assert services[0].readings["1"] == "Genesis 12:1-12:13"
        assert services[0].readings["3"] == "Genesis 13:5-13:18"

