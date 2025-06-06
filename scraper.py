from playwright.sync_api import sync_playwright

def obtener_stats(steam_id):
    url = f"https://csstats.gg/player/{steam_id}"
    stats = {
        "steam_id": steam_id,
        "rank": None,
        "kd": None,
        "hltv_rating": None,
        "clutch_success": None,
        "winrate": None,
        "hs": None,
        "adr": None,
        "entry_success": None,
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)

        # Esperar a que cargue contenido
        page.wait_for_selector("div#kpd")

        def safe_text(selector):
            try:
                return page.locator(selector).first.inner_text().strip()
            except:
                return None

        # Extraer datos
        stats["rank"] = safe_text(".rank-block .rank-block__value")
        stats["kd"] = safe_text("div#kpd span")
        stats["hltv_rating"] = safe_text("div#rating span")
        stats["clutch_success"] = safe_text("div#clutch span")
        stats["winrate"] = safe_text("div#winrate span")
        stats["hs"] = safe_text("div#hs span")
        stats["adr"] = safe_text("div#adr span")
        stats["entry_success"] = safe_text("div#entry span")  # Si hay selector identificable

        browser.close()
    return stats

# Solo para pruebas
if __name__ == "__main__":
    ejemplo_steam_id = "76561198108579338"
    data = obtener_stats(ejemplo_steam_id)
    for k, v in data.items():
        print(f"{k}: {v}")