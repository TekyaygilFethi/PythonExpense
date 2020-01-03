import  re
import datetime
import pandas as pd
import Levenshtein
from date_detector import Parser
import IdeconOCRHelper.ValidationFolder.NumberValidation as numberValidation


parser = Parser()

month_strings = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz','Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
day_strings = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"]
df = pd.DataFrame({'month': month_strings})


formats=["%Y-%m-%d","%d-%m-%Y","%Y/%m/%d","%d/%m/%Y","%Y.%m.%d","%d.%m.%Y"]

regexs = [
r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})",
r"(\d{2})[-|\/|.](\d{1,2})[-|\/|.](\d{2,4})",
r"(.{1,2})[-|/|.](.{1,2})[-|/|.](.{2,4})",
r"(..)[-|\/|.](..)[-|\/|.](..)"
]


def get(text):
    val = None

    for regex in regexs:
        text = text.replace(" ", "")
        val = process(text,regex)
        if val != None:
            break

    if val == None:
        text = text.replace(" ", "")
        for match in parser.parse(text):
            return "{}/{}/{}".format(match.date.day,match.date.month,match.date.year)

    if val == None:
       return find_dates(text)

    return val

def process(text,regex):
    matches = re.finditer(regex,text, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        date = "{}".format(match.group(0))
        #seçilen tarihin içinde sadece rakam mı var yoksa yazıda varmı onu öğrenip tahmin yapıp geri gönderiyor
        date = numberValidation.onlyNumberValidate(date)
        for format in formats:
            if validate(date,format) == 1:
                return date
    else:
        return None

def validate(date,format):
    try:
        datetime.datetime.strptime(date, format)
        return 1
    except:
        return 0

def find_dates(text):
    day = ""
    month=""
    year=""

    matches = re.findall(r"\d.*?[12]\d{3}", text, re.MULTILINE)
    for match in matches:
        matches_year = re.findall(r"[12]\d{3}", match, re.MULTILINE)
        if matches_year:
            match = match.replace(matches_year[0], "")
            year= matches_year[0]

        matches_month = re.findall(r"[a-zA-Z]+", match, re.MULTILINE)
        if matches_year:
            match = match.replace(matches_month[0], "")
            month = matches_month[0]

        day = match.replace(" ","")

        df['dist'] = df['month'].apply(lambda month: Levenshtein.distance(month, month))
        idxmin = df['dist'].idxmin()
        month =  month_strings[idxmin]
        return "{}/{}/{}".format(day,idxmin+1,year)