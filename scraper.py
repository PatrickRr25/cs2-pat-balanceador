import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def obtener_stats(steam_id):
    url = f"https://csstats.gg/player/{steam_id}"

    # Configurar navegador headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(url)
    time.sleep(2)  # Esperar carga inicial

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Diccionario de resultados
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
        # Extraer Skill y Rank
        stats["skill"] = soup.find("div", class_="skill__value").text.strip()
        stats["rank"] = soup.find("div", class_="skill__rank").text.strip()

        # Extraer otras estadísticas
        rows = soup.find_all("div", class_="player__stat__value")

        if rows and len(rows) >= 5:
            stats["kd"] = rows[0].text.strip()
            stats["hs"] = rows[1].text.strip()
            stats["winrate"] = rows[2].text.strip()
            stats["adr"] = rows[4].text.strip()
    except Exception as e:
        print(f"❌ Error extrayendo stats para {steam_id}: {e}")

    return stats