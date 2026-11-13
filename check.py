
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://cfc.scenecinemas.com/home"
TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
FILE = "seen.json"

html = requests.get(
    URL,
    timeout=20,
    headers={"User-Agent": "Mozilla/5.0"}
).text

soup = BeautifulSoup(html, "html.parser")

movies = {}

for a in soup.select('a[href*="/movie-details/"]'):
    name = a.get("title") or a.get_text(strip=True)

    if name:
        link = urljoin(URL, a["href"])
        movies[link] = name

print("لقيت", len(movies), "فيلم")

if not movies:
    raise SystemExit("مفيش أفلام اتعرفت")

if os.path.exists(FILE):
    with open(FILE, encoding="utf-8") as f:
        seen = set(json.load(f))
else:
    seen = set()

new_movies = set(movies) - seen

for link in sorted(new_movies):
    message = f"🎬 فيلم جديد نزل!\n{movies[link]}\n{link}"

    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )
    response.raise_for_status()

with open(FILE, "w", encoding="utf-8") as f:
    json.dump(
        sorted(seen | set(movies)),
        f,
        ensure_ascii=False,
        indent=2
    )
