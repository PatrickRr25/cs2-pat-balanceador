# scraper.py

import requests
from bs4 import BeautifulSoup

def obtener_stats(steam_id):
    url = f"https://csstats.gg/player/{steam_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    stats = {
        "steam_id": steam_id,
        "rank": None,
        "skill": None,
        "kd": None,
        "hs": None,
        "winrate": None,
        "adr": None
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Rank y Skill
        skill_block = soup.find("div", class_="skill__value")
        rank_block = soup.find("div", class_="skill__rank")
        stats["skill"] = skill_block.text.strip() if skill_block else "N/A"
        stats["rank"] = rank_block.text.strip() if rank_block else "N/A"

        # Stats individuales
        values = soup.find_all("div", class_="player__stat__value")
        if values and len(values) >= 5:
            stats["kd"] = values[0].text.strip()
            stats["hs"] = values[1].text.strip()
            stats["winrate"] = values[2].text.strip()
            stats["adr"] = values[4].text.strip()

    except Exception as e:
        print(f"❌ Error al obtener stats para {steam_id}: {e}")

    return stats