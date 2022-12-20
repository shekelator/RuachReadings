import pytest
import json
import readings
import datetime

@pytest.fixture()
def hebCalData():
    with open('ex.json', 'r', encoding="utf8") as reader:
        yield json.load(reader)['items']

class TestReadings:

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
        assert services[0].additionalDescription == None
        assert services[0].date == datetime.date(2022, 11, 5)
        assert services[0].isShabbat == True
        assert services[0].torahReading == "Genesis 13:5-13:18"

    def test_holiday_can_also_be_shabbat(self, hebCalData):
        data = [        {
            "date": "2023-09-16",
            "hdate": "1 Tishrei 5784",
            "name": {
                "en": "Rosh Hashana I (on Shabbat)",
                "he": "רֹאשׁ הַשָּׁנָה יוֹם א׳ (בְּשַׁבָּת)"
            },
            "fullkriyah": {
                "1": { "p": 4, "k": "Genesis", "b": "21:1", "e": "21:4", "v": 4 },
                "2": { "p": 4, "k": "Genesis", "b": "21:5", "e": "21:8", "v": 4 },
                "3": { "p": 4, "k": "Genesis", "b": "21:9", "e": "21:12", "v": 4 },
                "4": { "p": 4, "k": "Genesis", "b": "21:13", "e": "21:17", "v": 5 },
                "5": { "p": 4, "k": "Genesis", "b": "21:18", "e": "21:21", "v": 4 },
                "6": { "p": 4, "k": "Genesis", "b": "21:22", "e": "21:27", "v": 6 },
                "7": { "p": 4, "k": "Genesis", "b": "21:28", "e": "21:34", "v": 7 },
                "M": { "p": 41, "k": "Numbers", "b": "29:1", "e": "29:6", "v": 6 }
            },
            "summary": "Genesis 21:1-34; Numbers 29:1-6",
            "summaryParts": [
                { "k": "Genesis", "b": "21:1", "e": "21:34" },
                { "k": "Numbers", "b": "29:1", "e": "29:6" }
            ],
            "haft": { "k": "I Samuel", "b": "1:1", "e": "2:10", "v": 38 },
            "haftara": "I Samuel 1:1-2:10"
        }]
        service = list(readings.getReadings(data))[0]
        assert service.name == "Rosh Hashana I"
        assert service.isShabbat == True
        assert service.isHoliday == True
        assert service.torahReading == "Genesis 21:1-21:34"
        assert service.maftirReading == "Numbers 29:1-29:6"



    def test_can_get_torah_and_haft_for_date(self, hebCalData):
        services = list(readings.getReadings(hebCalData))
        (torah, haftarah, maftir) = readings.getReadingsForDate(hebCalData, datetime.date(2022, 12, 3))
        assert torah == "Genesis 29:18-30:13"
        assert haftarah == "Hosea 12:13-14:10"
        assert maftir == None

    def test_includes_maftir(self, hebCalData):
        services = list(readings.getReadings(hebCalData))
        (torah, haftarah, maftir) = readings.getReadingsForDate(hebCalData, datetime.date(2022, 12, 24))
        assert maftir == "Numbers 7:42-7:47"

    def test_includes_maftir_reason(self, hebCalData):
        services = list(filter(lambda s: s.date == datetime.date(2022, 12, 24), readings.getReadings(hebCalData)))[0]
        assert services.additionalDescription == "Shabbat Rosh Chodesh Chanukah"

    def test_can_get_hebrew_year(self, hebCalData):
        data = [{
            'date': '2022-11-05',
            'hdate': '11 Cheshvan 5783',
            'name': {'en': 'Lech-Lecha', 'he': 'לֶךְ־לְךָ'},
            'parshaNum': 3,
            'summary': 'Genesis 12:1-17:27',
            'fullkriyah': {'1': {'k': 'Genesis', 'b': '12:1', 'e': '12:13', 'v': 13}, '2': {'k': 'Genesis', 'b': '12:14', 'e': '13:4', 'v': 11}, '3': {'k': 'Genesis', 'b': '13:5', 'e': '13:18', 'v': 14}, '4': {'k': 'Genesis', 'b': '14:1', 'e': '14:20', 'v': 20}, '5': {'k': 'Genesis', 'b': '14:21', 'e': '15:6', 'v': 10}, '6': {'k': 'Genesis', 'b': '15:7', 'e': '17:6', 'v': 37}, '7': {'k': 'Genesis', 'b': '17:7', 'e': '17:27', 'v': 21}, 'M': {'k': 'Genesis', 'b': '17:24', 'e': '17:27', 'v': 4}}, 'haft': {'k': 'Isaiah', 'b': '40:27', 'e': '41:16', 'v': 21},
            'haftara': 'Isaiah 40:27-41:16',
            'triennial': {'1': {'k': 'Genesis', 'b': '12:1', 'e': '12:3', 'v': 3}, '2': {'k': 'Genesis', 'b': '12:4', 'e': '12:9', 'v': 6}, '3': {'k': 'Genesis', 'b': '12:10', 'e': '12:13', 'v': 4}, '4': {'k': 'Genesis', 'b': '12:14', 'e': '12:20', 'v': 7}, '5': {'k': 'Genesis', 'b': '13:1', 'e': '13:4', 'v': 4}, '6': {'k': 'Genesis', 'b': '13:5', 'e': '13:11', 'v': 7}, '7': {'k': 'Genesis', 'b': '13:12', 'e': '13:18', 'v': 7}, 'M': {'k': 'Genesis', 'b': '13:16', 'e': '13:18', 'v': 3}},
            'triYear': 1,
            'triHaftara': 'Judges 6:24-32',
            'triHaft': {'k': 'Judges', 'b': '6:24', 'e': '6:32', 'note': "Gideon smashes dad's idol // Abraham and Terach's idols (midrash)", 'v': 9}
        },{
            'date': '2022-11-05',
            'hdate': '11 Cheshvan 5782',
            'name': {'en': 'Lech-Lecha', 'he': 'לֶךְ־לְךָ'},
            'parshaNum': 3,
            'summary': 'Genesis 12:1-17:27',
            'fullkriyah': {'1': {'k': 'Genesis', 'b': '12:1', 'e': '12:13', 'v': 13}, '2': {'k': 'Genesis', 'b': '12:14', 'e': '13:4', 'v': 11}, '3': {'k': 'Genesis', 'b': '13:5', 'e': '13:18', 'v': 14}, '4': {'k': 'Genesis', 'b': '14:1', 'e': '14:20', 'v': 20}, '5': {'k': 'Genesis', 'b': '14:21', 'e': '15:6', 'v': 10}, '6': {'k': 'Genesis', 'b': '15:7', 'e': '17:6', 'v': 37}, '7': {'k': 'Genesis', 'b': '17:7', 'e': '17:27', 'v': 21}, 'M': {'k': 'Genesis', 'b': '17:24', 'e': '17:27', 'v': 4}}, 'haft': {'k': 'Isaiah', 'b': '40:27', 'e': '41:16', 'v': 21},
            'haftara': 'Isaiah 40:27-41:16',
            'triennial': {'1': {'k': 'Genesis', 'b': '12:1', 'e': '12:3', 'v': 3}, '2': {'k': 'Genesis', 'b': '12:4', 'e': '12:9', 'v': 6}, '3': {'k': 'Genesis', 'b': '12:10', 'e': '12:13', 'v': 4}, '4': {'k': 'Genesis', 'b': '12:14', 'e': '12:20', 'v': 7}, '5': {'k': 'Genesis', 'b': '13:1', 'e': '13:4', 'v': 4}, '6': {'k': 'Genesis', 'b': '13:5', 'e': '13:11', 'v': 7}, '7': {'k': 'Genesis', 'b': '13:12', 'e': '13:18', 'v': 7}, 'M': {'k': 'Genesis', 'b': '13:16', 'e': '13:18', 'v': 3}},
            'triYear': 1,
            'triHaftara': 'Judges 6:24-32',
            'triHaft': {'k': 'Judges', 'b': '6:24', 'e': '6:32', 'note': "Gideon smashes dad's idol // Abraham and Terach's idols (midrash)", 'v': 9}
        }]
        services = list(readings.getReadings(data))
        assert services[1].getHebrewYear() == 5782
        assert services[0].getHebrewYear() == 5783


    def test_shabbat_chol_hamoed_sukkot(self, hebCalData):
        (torah, haftarah, maftir) = readings.getReadingsForDate(hebCalData, datetime.date(2024, 10, 19))
        assert torah == "Exodus 34:4-34:10"
        assert maftir == "Numbers 29:17-29:22"
        assert haftarah == "Ezekiel 38:18-39:16"

    def test_marks_holidays_correctly(self, hebCalData):
        holidayDates = [datetime.date(2023, 4, 6), datetime.date(2023, 4, 7)]
        allServicesByDate = { r.date : r for r in readings.getReadings(hebCalData) }
        for date in holidayDates:
            assert allServicesByDate[date].isHoliday == True

        nonHolidayDates = [datetime.date(2023, 4, 8), datetime.date(2024, 9, 7)]
        for date in nonHolidayDates:
            assert allServicesByDate[date].isHoliday == False

    def test_gets_maftir_for_chol_hamoed(self, hebCalData):
        (torah, haftarah, maftir) = readings.getReadingsForDate(hebCalData, datetime.date(2023, 4, 6))
        assert maftir == "Numbers 28:16-28:25"

    def test_holidays_have_readings(self, hebCalData):
        holidayDates = [datetime.date(2023, 4, 6)]  # todo add shavuot, sukkot, HH, etc.
        allServicesByDate = { r.date : r for r in readings.getReadings(hebCalData) }
        for date in holidayDates:
            assert allServicesByDate[date].torahReading != None
            assert allServicesByDate[date].haftarahReading != None
            assert allServicesByDate[date].maftirReading != None
            assert allServicesByDate[date].besorahReading != None

    def test_gets_holiday_besorah_for_holidays(self, hebCalData):
        holidayDates = [
            (datetime.date(2023, 4, 6), "1 Corinthians 11:23-26"),
            (datetime.date(2023, 4, 8), "Revelation 5:1-14"), # Pesach Shabbat Chol ha-Moed
            (datetime.date(2025, 3, 1), "Mark 12:41-44"),  # Shabbat shekalim
            (datetime.date(2024, 10, 3), "Romans 8:31-39"),  # Rosh Hashana I
            (datetime.date(2024, 10, 4), "1 Thessalonians 4:13-18"),  # Rosh Hashana II
            (datetime.date(2024, 10, 3), "Romans 8:31-39"),  # Rosh Hashana I
            (datetime.date(2024, 10, 5), "Luke 15:11-32"),  # Shabbat Shuva
            (datetime.date(2024, 10, 12), "Hebrews 9:1-14"),  # Yom Kippur
            (datetime.date(2025, 3, 8), "Revelation 6:9-7:8"),  # Shabbat Zachor
            (datetime.date(2025, 3, 22), "Hebrews 9:11-14"),  # Shabbat Parah
            (datetime.date(2025, 3, 29), "1 Corinthians 5:6-8"),  # Shabbat HaChodesh
            (datetime.date(2025, 4, 12), "Luke 1:5-22"),  # Shabbat HaGadol
            (datetime.date(2025, 4, 13), "1 Corinthians 11:23-26"),  # Pesach I
            (datetime.date(2025, 4, 19), "1 Corinthians 10:1-11"),  # Pesach VII

            # TODO might need a test for two Shabbat chol ha-moeds during pesach

        ]
        allServicesByDate = { r.date : r for r in readings.getReadings(hebCalData) }
        for date, besorah in holidayDates:
            assert allServicesByDate[date].besorahReading == besorah



## cases remaining to cover:
# * Festivals (e.g. chanukah) + rosh chodesh (multiple maftir readings)
# * Special shabbats (e.g. shekalim) on rosh chodesh (multiple maftir readings)
