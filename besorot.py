def readingsToFn(readings):
    return lambda r: { "A": readings[0], "B": readings[1], "C": readings[2] }[r]

parshiot = {
    "Bereshit": lambda _: "John 1:1-18",
    "Lech-Lecha": readingsToFn(("Matthew 1:18-25", "Luke 2:1-20", "John 1:35-51")),
    "Vayetzei": readingsToFn(("Mark 1:14-28", "Luke 4:1-15", "John 4:5-30")),
    "Vayishlach": readingsToFn(("Mark 1:29-45", "Luke 4:16-30", "John 4:31-42")),
}
def getReadings(parasha, year):
    besorahYear = getYear(year)
    return parshiot[parasha](besorahYear) if parasha in parshiot else None

def getYear(year):
    key = {
        0: "B",
        1: "C",
        2: "A",
    }
    return key[year % 3]

if __name__ == "__main__":
    print(f"Nothing to do yet")