import datetime
import requests
import json

class Service:
    def fromDict(self, d):
        self.date =  datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()
        return self

def getReadings():
    date = datetime.datetime.now()
    endDate = date + datetime.timedelta(days=180)
    date.strftime("%d-%m-%Y")
    url = f"https://www.hebcal.com/leyning?cfg=json&start={date.strftime('%Y-%m-01')}&end={endDate.strftime('%Y-%m-%d')}"
    data = requests.get(url)
    print(url)

    return json.loads(data.text)
    

if __name__ == "__main__":
    import sys
    # fib(int(sys.argv[1]))
    print(f"Url is {getReadings()}")