import datetime
import requests
import json

class HebCal:

    

    def getRawReadingsData(self, startDate = None):
        date = self.parseDate(startDate)
        endDate = date + datetime.timedelta(days=180)
        formattedStartDate = date.strftime("%Y-%m-%d")
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