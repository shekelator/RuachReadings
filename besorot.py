def readingsToFn(readings):
    return lambda r: { "A": readings[0], "B": readings[1], "C": readings[2] }[r]

def singleReadingToFn(reading):
    return lambda r: reading

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
    "Bo": readingsToFn(("Matthew 7:13-29", "Luke 7:1-17", "John 6:30-51")),
    "Beshalach": readingsToFn(("Mark 2:1-12", "Luke 7:18-35", "John 6:52-71")),
    "Yitro": readingsToFn(("Matthew 11:2-19", "Luke 7:36-50", "John 7:1-13")),
    "Mishpatim": readingsToFn(("Matthew 11:20-30", "Luke 8:1-21", "John 7:14-24")),
    "Terumah": readingsToFn(("Matthew 13:1-23", "Luke 8:22-39", "John 7:25-36")),
    "Tetzaveh": readingsToFn(("Matthew 14:12-33", "Luke 8:40-56", "John 7:37-52")),
    "Ki Tisa": readingsToFn(("Matthew 15:1-20", "Luke 9:1-17", "John 8:1-11")),
    "Vayakhel": readingsToFn(("Matthew 15:21-28", "Luke 9:18-27", "John 8:12-20")),
    "Pekudei": readingsToFn(("Matthew 15:29-39", "Luke 9:28-36", "John 8:21-30")),
    "Vayakhel-Pekudei": readingsToFn(("Matthew 15:21-39", "Luke 9:18-36", "John 8:12-30")),
    "Vayikra": readingsToFn(("Matthew 16:1-20", "Luke 10:25-42", "John 8:31-47")),
    "Tzav": readingsToFn(("Matthew 16:21-17:13", "Luke 11:1-13", "John 8:48-59")),
    "Shmini": readingsToFn(("Matthew 17:14-27", "Luke 12:13-34", "John 9:1-17")),
    "Tazria": readingsToFn(("Matthew 18:1-18", "Luke 13:1-9", "John 9:18-23")),
    "Metzora": readingsToFn(("Matthew 18:19-35", "Luke 13:10-17", "John 9:24-41")),
    "Tazria-Metzora": readingsToFn(("Matthew 18:1-18", "Luke 13:1-17", "John 9:18-41")),
    "Achrei Mot": readingsToFn(("Matthew 19:1-12", "Luke 14:1-11", "John 10:1-10")),
    "Kedoshim": readingsToFn(("Matthew 19:13-30", "Matthew 19:13-30", "John 10:11-21")),
    "Achrei Mot-Kedoshim": readingsToFn(("Matthew 19:1-12", "Luke 14:1-24", "John 10:1-21")),
    "Emor": readingsToFn(("Matthew 20:1-19", "Luke 14:25-33", "John 10:22-42")),
    "Behar": readingsToFn(("Matthew 21:1-17", "Luke 16:1-9", "John 11:1-16")),
    "Bechukotai": readingsToFn(("Matthew 21:18-27", "Luke 16:10-17", "John 11:17-37")),
    "Behar-Bechukotai": readingsToFn(("Matthew 21:1-17", "Luke 16:1-17", "John 11:1-37")),
    "Bamidbar": readingsToFn(("Mark 12:28-34", "Luke 16:19-31", "John 11:38-57")),
    "Nasso": readingsToFn(("Mark 13:14-27", "Luke 18:1-17", "John 12:1-26")),
    "Beha'alotcha": readingsToFn(("Mark 14:1-11", "Luke 18:31-43", "John 13:1-20")),
    "Sh'lach": readingsToFn(("Matthew 26:17-30", "Luke 19:1-28", "John 14:1-24")),
    "Korach": readingsToFn(("Mark 14:32-50", "Luke 19:29-48", "John 15:1-17")),
    "Chukat": readingsToFn(("", "", "")),  # TODO figure out how to determine if matt-masei are combined
    "Balak": readingsToFn(("", "", "")),
    "Chukat-Balak": readingsToFn(("Mark 14:53-72", "Luke 20:1-18", "")),
    "Pinchas": readingsToFn(("", "", "")),
    "Matot": readingsToFn(("Matthew 27:27-32", "Luke 23:26-32", "John 18:1-27")),
    "Masei": readingsToFn(("Matthew 27:33-44", "Luke 23:33-43", "John 18:28-19:16")),
    "Matot-Masei": readingsToFn(("Matthew 27:33-44", "Luke 23:33-43", "John 18:28-19:16")),
    "Devarim": readingsToFn(("Matthew 27:45-61", "Luke 23:44-56", "John 19:17-41")),
    "Vaetchanan": readingsToFn(("Matthew 27:62-28:10", "Luke 24:1-11", "John 20:1-18")),
    "Eikev": readingsToFn(("Luke 24:13-32", "Luke 24:13-32", "Luke 24:13-32")),
    "Re'eh": singleReadingToFn("Luke 24:33-49"),
    "Shoftim": singleReadingToFn("John 20:19-29"),
    "Ki Teitzei": singleReadingToFn("John 21:1-25"),
    "Ki Tavo": singleReadingToFn("1 Cor. 15:1-11"),
    "Nitzavim": singleReadingToFn("Matthew 28:16-20"),
    "Nitzavim-Vayeilech": singleReadingToFn("Matthew 28:16-20"),
    "Ha'Azinu": singleReadingToFn("Romans 15:7-13"),
    # "Vezot Haberakhah": readingsToFn(("", "", "")),
    # TODO holidays
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