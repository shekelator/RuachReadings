import datetime
import requests
import json
import re

hdatePattern = re.compile(r"^(?P<day>\d*) (?P<month>\w*) (?P<year>\d{4})$")
class Service:
    def fromDict(self, d):
        self.date = datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()
        self.hebrewDate = d["hdate"]
        self.name = d["name"]["en"]
        self.isShabbat = "fullkriyah" in d and "7" in d["fullkriyah"]

        if self.isShabbat:
            self.readings = {k: self.convertReading(v) for k, v in d["fullkriyah"].items()}

            aliyahForThisYear = (self.getHebrewYear() % 5780) + 1  # tell us which year of 7-year reading cycle we are in

            self.torahReading = self.readings[f"{aliyahForThisYear}"]
            self.haftarahReading = d["haftara"] if "haftara" in d else None

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

def getRawReadingsData():
    date = datetime.datetime.now()
    endDate = date + datetime.timedelta(days=180)
    date.strftime("%d-%m-%Y")
    url = f"https://www.hebcal.com/leyning?cfg=json&start={date.strftime('%Y-%m-01')}&end={endDate.strftime('%Y-%m-%d')}"
    data = requests.get(url)
    rawDict = json.loads(data.text)
    return rawDict["items"]

def getReadings(rawItems):
    shabbatot = filter(lambda r: 'fullkriyah' in r, rawItems)
    shabbatServices = map(lambda i: Service().fromDict(i), shabbatot)
    
    return shabbatServices

def getReadingsForDate(rawItems, date):
    services = list(getReadings(rawItems))
    servicesOnDate = list(filter(lambda r: r.date == date, services))
    if not servicesOnDate:
        return (None, None)
    else:
        service = servicesOnDate[0]
        return (service.torahReading, service.haftarahReading)
    

if __name__ == "__main__":
    import sys
    # fib(int(sys.argv[1]))
    print(f"Url is {getReadings()}")