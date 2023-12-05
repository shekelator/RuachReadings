import datetime
import re
import besorot


class Service:
    hdatePattern = re.compile(
        r"^(?P<day>\d*) (?P<month>[\w']*) (?P<year>\d{4})$")
    holidayNamesPattern = re.compile(
        r"Sukkot|Pesach|Rosh Hashana|Shavuot|Yom Kippur|Shmini Atzeret")
    cholHaMoedPattern = re.compile(r"Chol ha-Moed")
    minchaPattern = re.compile(r"\(Mincha\)")
    roshChodeshPattern = re.compile(r"Rosh Chodesh")

    def fromDict(self, d):
        self.date = datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()
        self.hebrewDate = d["hdate"]
        self.name = d["name"]["en"].replace(" (on Shabbat)", "")
        self.hebrewName = d["name"]["he"] if "he" in d["name"] else None
        self.isShabbat = "fullkriyah" in d and "7" in d["fullkriyah"]
        self.torahReading = None
        self.maftirReading = None
        self.haftarahReading = None
        self.additionalDescription = None
        self.besorahReading = None
        self.isHoliday = False
        self.isMincha = bool(self.minchaPattern.search(self.name))

        if "fullkriyah" in d:
            fullkriyah = d["fullkriyah"]
            allTorahReadings = {k: self.convertReading(v) for k, v in fullkriyah.items()}
            maftir = None
            self.isHoliday = bool("M" in fullkriyah and self.isHolidayByName())

            if self.isShabbat:
                self.torahReading = allTorahReadings[getAliyahForYear(self.getHebrewYear(), self.name, self.hebrewDate)]
                self.fullTorahReading = d["summary"].split(";")[0].strip()

            if self.isHoliday:
                # holidays don't typically have 7 aliyot, so just show the whole reading from the summaryParts property
                if "summaryParts" in d:
                    self.torahReading = self.convertReading(d["summaryParts"][0]).split(";")[0]

            self.haftarahReading = d["haftara"] if "haftara" in d else None

            if "M" in fullkriyah and (self.isHoliday or self.isCholHaMoed() or "reason" in fullkriyah["M"]):
                maftir = fullkriyah["M"]
                self.maftirReading = self.convertReading(maftir)

            if "reason" in d:
                if "haftara" in d["reason"]:
                    self.additionalDescription = d["reason"]["haftara"]
                elif "M" in d["reason"]:
                    self.additionalDescription = d["reason"]["M"]

            self.besorahReading = besorot.getReadings(
                self.name, self.getHebrewYear(), self.date, self.additionalDescription)

        return self

    def convertReading(self, readingData):
        book = readingData["k"]
        begin = readingData["b"]
        end = readingData["e"]
        return f"{book} {begin}-{end}"

    def isCholHaMoed(self):
        return bool(self.cholHaMoedPattern.search(self.name))

    def isRoshChodesh(self):
        return (self.name and bool(self.roshChodeshPattern.search(self.name))) or (self.additionalDescription and bool(self.roshChodeshPattern.search(self.additionalDescription)))

    def isShabbatChanukah(self):
        return self.additionalDescription and "on Shabbat" in self.additionalDescription and "Chanukah" in self.additionalDescription

    def isHolidayByName(self):
        return bool(self.holidayNamesPattern.search(self.name) and not self.isCholHaMoed())

    def getHebrewYear(self):
        match = self.hdatePattern.match(self.hebrewDate)
        if match is None:
            return 0
        else:
            return int(match.group("year"))



# tell us which year of 7-year reading cycle we are in. 
def getAliyahForYear(year, parasha, hebrewDate):
    aliyahForThisYear = ((year - 5781) % 7) + 1

    # When the year turns over on Tishrei 1 (RH), we don't change the aliyah until after Simchat Torah
    if parasha.lower() in ["ha'azinu", "v'zot haberakhah", "vayeilech", "nitzavim-vayeilech"] and "Tishrei" in hebrewDate:
        aliyahForThisYear -= 1

    return f"{aliyahForThisYear}"

def getShortenedHafarah(service):
    if service.haftarahReading is None:
        return None

    if service.isShabbatChanukah():
        return "Zechariah 2:14-3:10"

    if service.isRoshChodesh():
        return "Isaiah 66:5-24"

    shortenedHaftarahMap = {
        ("Ki Tavo", "Isaiah 60:1-22"): "Isaiah 60:1-7",
        ("Chukat-Balak", "Micah 5:6-6:8"): "Micah 6:1-6:8",
        ("Balak", "Micah 5:6-6:8"): "Micah 6:1-6:8",
        ("Nitzavim-Vayeilech", "Isaiah 61:10-63:9"): "Isaiah 61:10-62:12",
    }
    if shortenedHaftarahMap.get((service.name, service.haftarahReading)) is not None:
        return shortenedHaftarahMap.get((service.name, service.haftarahReading))
    return service.haftarahReading


def getReadings(rawItems):
    shabbatServices = filter(lambda s: (s.isShabbat or s.isHoliday) and (
        not s.isMincha), map(lambda i: Service().fromDict(i), rawItems))

    return shabbatServices

def getReadingsForDate(rawItems, date):
    services = list(getReadings(rawItems))
    servicesOnDate = list(filter(lambda r: r.date == date, services))
    if not servicesOnDate:
        return (None, None, None)
    else:
        service = servicesOnDate[0]
        return (service.torahReading, service.haftarahReading, service.maftirReading)


if __name__ == "__main__":
    import sys
    print(f"Url is {getReadings()}")
