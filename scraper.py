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
        "hltv_rating": None,
        "kd": None,
        "hs": None,
        "winrate": None,
        "adr": None
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Extraer por ID individual
        def get_stat_by_id(stat_id):
            div = soup.find("div", id=stat_id)
            if div and div.find("span"):
                return div.find("span").text.strip()
            return None

        stats["hltv_rating"] = get_stat_by_id("rating")
        stats["kd"] = get_stat_by_id("kd")
        stats["hs"] = get_stat_by_id("hs")
        stats["winrate"] = get_stat_by_id("winrate")
        stats["adr"] = get_stat_by_id("adr")

        # Skill rank en la parte superior
        skill_block = soup.find("div", class_="skill__value")
        rank_block = soup.find("div", class_="skill__rank")
        stats["rank"] = rank_block.text.strip() if rank_block else None
        stats["skill"] = skill_block.text.strip() if skill_block else None

    except Exception as e:
        print(f"❌ Error al scrapear stats para {steam_id}: {e}")

    return stats