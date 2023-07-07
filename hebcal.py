import datetime
import requests
import json
from expiringdict import ExpiringDict

class HebCal:

    def __init__(self):
        self.cached = ExpiringDict(max_len=100, max_age_seconds=60*5)

    def getRawReadingsData(self, startDate = None):
        date = self.parseDate(startDate)
        endDate = date + datetime.timedelta(days=180)
        formattedStartDate = date.strftime("%Y-%m-%d")
        if formattedStartDate in self.cached:
            return self.cached.get(formattedStartDate)
        else:
            data = self.retrieveData(formattedStartDate, endDate)
            self.cached[formattedStartDate] = data
            return data
        
    def retrieveData(self, formattedStartDate, endDate):
        url = f"https://www.hebcal.com/leyning?cfg=json&triennial=off&start={formattedStartDate}&end={endDate.strftime('%Y-%m-%d')}"
        data = requests.get(url)
        rawDict = json.loads(data.text)
        return rawDict["items"]

    def parseDate(self, dateString):
        if dateString is None:
            return datetime.datetime.now().date()
        try:
            return datetime.datetime.strptime(dateString, "%Y-%m-%d").date()
        except ValueError:
            return datetime.datetime.now().date()