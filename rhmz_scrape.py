import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

URLS = [
    "https://www.hidmet.gov.rs/ciril/osmotreni/index.php",
    "https://www.hidmet.gov.rs/ciril/automatske/index.php"
]

def parse_table(url):
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    rows = table.find_all("tr")
    header = [th.get_text(strip=True) for th in rows[0].find_all("th")]

    data = []
    for r in rows[1:]:
        cols = [c.get_text(strip=True) for c in r.find_all("td")]
        if len(cols) < 2:
            continue
        data.append(cols)
    return header, data

now = datetime.now().strftime("%Y-%m-%d_%H%M")
filename = f"data/rhmz_{now}.csv"

os.makedirs("data", exist_ok=True)

with open(filename, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)

    for url in URLS:
        header, data = parse_table(url)
        writer.writerow([f"Source: {url}"])
        writer.writerow(header)
        writer.writerows(data)
        writer.writerow([])
