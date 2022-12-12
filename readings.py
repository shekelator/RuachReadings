import datetime
import requests
import json
import re
import besorot

hdatePattern = re.compile(r"^(?P<day>\d*) (?P<month>\w*) (?P<year>\d{4})$")
class Service:
    def fromDict(self, d):
        self.date = datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()
        self.hebrewDate = d["hdate"]
        self.name = d["name"]["en"]
        self.hebrewName = d["name"]["he"] if "he" in d["name"] else None
        self.isShabbat = "fullkriyah" in d and "7" in d["fullkriyah"]
        self.maftirReading = ""

        if self.isShabbat:
            self.readings = {k: self.convertReading(v) for k, v in d["fullkriyah"].items()}

            aliyahForThisYear = (self.getHebrewYear() % 5781) + 1  # tell us which year of 7-year reading cycle we are in

            self.torahReading = self.readings[f"{aliyahForThisYear}"]
            self.haftarahReading = d["haftara"] if "haftara" in d else None
            self.besorahReading = besorot.getReadings(self.name, self.getHebrewYear(), self.date)

            if "M" in d["fullkriyah"] and "reason" in d["fullkriyah"]["M"]:
                maftir = d["fullkriyah"]["M"]
                self.maftirReading = self.convertReading(maftir)
                if "reason" in maftir:
                    self.name = f"{self.name} {maftir['reason']}" 

        return self

    def convertReading(self, readingData):
        book = readingData["k"]
        begin = readingData["b"]
        end = readingData["e"]
        return f"{book} {begin}-{end}"

    def getHebrewYear(self): 
        match = hdatePattern.match(self.hebrewDate)
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
    url = f"https://www.hebcal.com/leyning?cfg=json&triennial=off&start={date.strftime('%Y-%m-01')}&end={endDate.strftime('%Y-%m-%d')}"
    data = requests.get(url)
    rawDict = json.loads(data.text)
    return rawDict["items"]

def getReadings(rawItems):
    shabbatServices = filter(lambda s: s.isShabbat, map(lambda i: Service().fromDict(i), rawItems))
    
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