import requests
import logging
from bs4 import BeautifulSoup

import mod

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
}

base_url = "https://thunderstore.io"
search_url = "https://thunderstore.io/c/lethal-company/?q={query}&ordering=last-updated&section=mods"

cached_mods = set()
cache_urls = set()

def get_page(url):
    if url in cache_urls:
        return None
    cache_urls.add(url)
    data = requests.get(url, headers=headers)
    
    if data.status_code == 200:
        logging.info(f"fetcher.py fetching {url}")
    else:
        logging.error(f"fetcher.py [{data.status_code}] fetching of {url} failed")
    return data.text

def download(url, out):
    data = requests.get(url, headers=headers)
    if data.status_code == 200:
        with open(out, "wb") as f:
            f.write(data.content)
        logging.info(f"fetcher.py download of {url} successfull")
    else:
        logging.error(f"fetcher.py [{data.status_code}] downloading of {url} failed")

def find_elem(arr, string, skip=False):
    it = iter(arr)
    res = ""
    for obj in it:
        if obj.text.strip() == string:
            if skip:
                return obj
            
            return next(it)

def parse(content):
    soup = BeautifulSoup(content, "lxml")

    # parse name
    h1 = soup.find("h1", {"class": "mt-0"})
    name = h1.text

    # parse filename
    tds = soup.find_all("td")
    filename = find_elem(tds, "Dependency string").text
    filename_ext = filename + ".zip"

    # get version
    version = filename.split("-")[-1]

    # get author
    author = filename.split("-")[0]

    # parse url
    btns = soup.find_all('a', {'class': 'btn btn-primary w-100 text-large'})
    url = find_elem(btns, "Manual Download", 1).get("href")

    # parse deps
    slots = soup.find_all('h5', {'class': 'mt-0'})
    deps = []
    for slot in slots:
        url2 = base_url + slot.a.get("href")
        page = get_page(url2)
        if not page:
            continue
        _mod = parse(page)
        deps.append(_mod)

    return mod.Mod(name, version, url, author, filename_ext, "./temp/" + filename_ext, deps)
