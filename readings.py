import datetime
import requests
import json
import re
import besorot


class Service:
    hdatePattern = re.compile(r"^(?P<day>\d*) (?P<month>\w*) (?P<year>\d{4})$")
    holidayNamesPattern = re.compile(r"Sukkot|Pesach|Rosh Hashana")
    cholHaMoedPattern = re.compile(r"Chol ha-Moed")

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

        if "fullkriyah" in d:
            fullkriyah = d["fullkriyah"]
            allTorahReadings = {k: self.convertReading(v) for k, v in fullkriyah.items()}
            maftir = None
            self.isHoliday = bool("M" in fullkriyah and self.isHolidayByName())
        
            aliyahForThisYear = ((self.getHebrewYear() - 5781) % 7) + 1  # tell us which year of 7-year reading cycle we are in

            if self.isShabbat:
                self.torahReading = allTorahReadings[f"{aliyahForThisYear}"]

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

            self.besorahReading = besorot.getReadings(self.name, self.getHebrewYear(), self.date, self.additionalDescription)

        return self

    def convertReading(self, readingData):
        book = readingData["k"]
        begin = readingData["b"]
        end = readingData["e"]
        return f"{book} {begin}-{end}"

    def isCholHaMoed(self):
        return bool(self.cholHaMoedPattern.search(self.name))

    def isHolidayByName(self):
        return bool(self.holidayNamesPattern.search(self.name) and not self.isCholHaMoed())

    def getHebrewYear(self): 
        match = self.hdatePattern.match(self.hebrewDate)
        if match is None:
            return 0
        else:
            return int(match.group("year"))

def parseDate(dateString):
    if dateString is None:
        return datetime.datetime.now().date()
    try:
        return datetime.datetime.strptime(dateString, "%Y-%m-%d").date()
    except ValueError:
        return datetime.datetime.now().date()

def getRawReadingsData(startDate = None):
    date = parseDate(startDate)
    endDate = date + datetime.timedelta(days=180)
    url = f"https://www.hebcal.com/leyning?cfg=json&triennial=off&start={date.strftime('%Y-%m-%d')}&end={endDate.strftime('%Y-%m-%d')}"
    data = requests.get(url)
    rawDict = json.loads(data.text)
    return rawDict["items"]

def getReadings(rawItems):
    shabbatServices = filter(lambda s: s.isShabbat or s.isHoliday, map(lambda i: Service().fromDict(i), rawItems))
    
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