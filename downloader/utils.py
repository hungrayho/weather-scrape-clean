import re

def extract_date(url):
    """
    extracts year and month from url containing yyyymm
    """
    yearmonth = re.search(r'\d+', url)
    return yearmonth[0][0:4], yearmonth[0][4:]
