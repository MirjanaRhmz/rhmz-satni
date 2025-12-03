import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

URL = "https://www.hidmet.gov.rs/ciril/osmotreni/index.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def parse_table(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")

    if table is None:
        print("❌ Nema tabele – RHMZ možda blokira request ili je promenio strukturu.")
        print("Prvih 300 karaktera HTML-a:")
        print(r.text[:300])
        raise SystemExit(1)

    rows = table.find_all("tr")
    header = [th.get_text(strip=True) for th in rows[0].find_all("th")]

    data = []
    for row in rows[1:]:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols and cols[1].replace("-", "").replace(".", "").isdigit():
            data.append(cols)

    return header, data


# koju tabelu čuvamo
header, data = parse_table(URL)

# format za GitHub Actions output
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
folder = "data"
os.makedirs(folder, exist_ok=True)

filename = f"{folder}/rhmz_{timestamp}.csv"

with open(filename, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

print(f"✔️ Sačuvano: {filename}")
