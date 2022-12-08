def readingsToFn(readings):
    return lambda r: { "A": readings[0], "B": readings[1], "C": readings[2] }[r]

parshiot = {
    "Bereshit": lambda _: "John 1:1-18",
    "Lech-Lecha": readingsToFn(("Matthew 1:18-25", "Luke 2:1-20", "John 1:35-51")),
    "Vayetzei": readingsToFn(("Mark 1:14-28", "Luke 4:1-15", "John 4:5-30")),
    "Vayishlach": readingsToFn(("Mark 1:29-45", "Luke 4:16-30", "John 4:31-42")),
    "Vayeshev": readingsToFn(("Matthew 5:1-16", "Luke 4:31-44", "John 4:43-54")),
    "Miketz": readingsToFn(("Matthew 5:17-26", "Luke 5:1-11", "John 5:1-15")),
    "Vayigash": readingsToFn(("Matthew 5:27-48", "Luke 5:12-26", "John 5:16-29")),
    "Vayechi": readingsToFn(("Matthew 6:1-18", "Luke 5:27-39", "John 5:30-47")),
    "Shemot": readingsToFn(("Matthew 6:19-34", "Luke 6:1-16", "John 6:1-15")),
    "Vaera": readingsToFn(("Matthew 7:1-12", "Luke 6:17-38", "John 6:16-29")),
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