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

        def get_span_by_id(element_id):
            div = soup.find("div", id=element_id)
            if div and div.find("span"):
                return div.find("span").text.strip()
            return None

        # IDs directos del HTML
        stats["hltv_rating"] = get_span_by_id("rating")         # HLTV Rating
        stats["kd"] = get_span_by_id("kpd")                     # Kill/Death
        stats["hs"] = get_span_by_id("hs")                      # Headshot %
        stats["winrate"] = get_span_by_id("winrate")            # Win Rate %
        stats["adr"] = get_span_by_id("adr")                    # ADR (Damage)

        # Rango y nivel de habilidad
        skill_block = soup.find("div", class_="skill__value")
        rank_block = soup.find("div", class_="skill__rank")
        stats["skill"] = skill_block.text.strip() if skill_block else None
        stats["rank"] = rank_block.text.strip() if rank_block else None

    except Exception as e:
        print(f"❌ Error al obtener stats de {steam_id}: {e}")

    return stats