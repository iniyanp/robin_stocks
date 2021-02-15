import datetime
def extractMonthYearFromDateString(date_str):
    tr_date = date_str.split('.')[0]
    dt = datetime.datetime.strptime(tr_date, "%Y-%m-%dT%H:%M:%S")
    return '%s/%s' % (dt.month , dt.year)