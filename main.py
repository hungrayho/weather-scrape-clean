import os
from settings import settings
from downloader.html import download_clean

if __name__ == '__main__':
    for i, url in enumerate(settings.URLS):
        clean_df = download_clean(url)
        clean_df.to_csv(settings.PATH + os.sep + str(i) + '.csv')