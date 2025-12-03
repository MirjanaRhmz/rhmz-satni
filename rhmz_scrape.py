import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

url = "https://www.hidmet.gov.rs/ciril/osmotreni/index.php"

response = requests.get(url)
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table")

if len(tables) < 2:
    print("Nedostaju tabele! RHMZ možda menja stranicu.")
    exit()

now = datetime.now().strftime("%d-%m-%y %H:%M")
now_file = datetime.now().strftime("%Y%m%d_%H%M")

# folder
folder = "rhmz_osmotreni_arhiva"
os.makedirs(folder, exist_ok=True)

csv_name = f"rhmz_sve_stanice_{now_file}.csv"
csv_path = os.path.join(folder, csv_name)

def extract_table(table, writer):
    rows = table.find_all("tr")

    # header
    header = [th.get_text(strip=True) for th in rows[0].find_all("th")]
    header.append("datetime_download")
    writer.writerow(header)

    # data rows
    for row in rows[1:]:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]

        # preskoči prazne i kraće od 3 kolone
        if len(cols) < 3:
            continue

        # preskoči fusnote (npr. "(1) Podaci ažurirani…")
        if cols[0].startswith("("):
            continue

        cols.append(now)
        writer.writerow(cols)


with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)

    # 1. glavna mreža
    extract_table(tables[0], writer)

    # 2. automatske stanice (dopunska mreža)
    extract_table(tables[1], writer)

print("Sačuvano:", csv_path)
