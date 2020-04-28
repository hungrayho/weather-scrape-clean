from settings import URLS, PATH
from downloader.html import download_clean

if __name__ == '__main__':
    for i, url in enumerate(urls):
        clean_df = download_clean(url)
        clean_df.to_csv(PATH + str(i) + '.csv')