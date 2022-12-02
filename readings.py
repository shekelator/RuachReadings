import datetime
import requests
import json

class Service:
    def fromDict(self, d):
        self.date =  datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()
        self.name = d["name"]["en"]
        self.isShabbat = "7" in d["fullkriyah"]
        self.readings = {k: self.convertReading(v) for k, v in d["fullkriyah"].items()}
        return self

    def convertReading(self, readingData):
        book = readingData["k"]
        begin = readingData["b"]
        end = readingData["e"]
        return f"{book} {begin}-{end}"


def getRawReadingsData():
    date = datetime.datetime.now()
    endDate = date + datetime.timedelta(days=180)
    date.strftime("%d-%m-%Y")
    url = f"https://www.hebcal.com/leyning?cfg=json&start={date.strftime('%Y-%m-01')}&end={endDate.strftime('%Y-%m-%d')}"
    data = requests.get(url)
    rawDict = json.loads(data.text)
    return data["items"]

def getReadings(rawItems):
    shabbatot = filter(lambda r: 'fullkriyah' in r, rawItems)
    shabbatServices = map(lambda i: Service().fromDict(i), shabbatot)
    
    return shabbatServices

    

if __name__ == "__main__":
    import sys
    # fib(int(sys.argv[1]))
    print(f"Url is {getReadings()}")