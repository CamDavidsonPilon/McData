import re
import requests
from bs4 import BeautifulSoup

WEB_ARCHIVE_URL = "https://web.archive.org"


def create_calender_url(url, year):
    return "https://web.archive.org/web/%d*/%s" % (year, url)


def extract_timestamp(url):
    t = re.match('/web/(\d{14})/', url)
    return t.groups()[0]


def download_file(url, filename):
    # NOTE the stream=True parameter
    # From SO
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return filename


def get_calender_pages(url, start=2015, end=2020, folder=None):
    for year in range(start, end+1):
        r = requests.get(create_calender_url(url, year))
        if len(r.history) > 0:
            continue

        html = r.text
        soup = BeautifulSoup(html)

        links = map(lambda link: link.get('href'), soup.find_all('a'))
        links = filter(lambda url: '*' not in url, links)
        links = filter(lambda url: re.match('/web/\d{14}/', url), links)
        links = set(links)
        print()
        print("Collected %d links in year %d" % (len(links), year))
        print()
        for link in links:
            timestamp = extract_timestamp(link)
            filename = folder + "/" + timestamp + '.pdf'
            link = WEB_ARCHIVE_URL + link
            download_file(link, filename)
            print(filename)


def run(url, folder):
    get_calender_pages(url, folder=folder)

if __name__ == "__main__":
    url = raw_input('Please enter a URL: ').strip()
    folder = raw_input('Please enter a destination to save pdfs too: ').strip()
    run(url, folder)
