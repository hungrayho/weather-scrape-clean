import os
from settings import settings
from downloader.html import download_clean
from downloader.utils import extract_date

if __name__ == '__main__':
    for url in settings.URLS:
        clean_df = download_clean(url)
        year, month = extract_date(url)
        clean_df.to_csv(f'{settings.PATH}{os.sep}{year}-{month}.csv')