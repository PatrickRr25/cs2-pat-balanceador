import streamlit as st
import re
import json
from playwright.sync_api import sync_playwright

# -------------------------------
# FUNCIONES
# -------------------------------

@st.cache_data(ttl=3600)  # Cachear por 1 hora
def obtener_stats_desde_json(steam_id):
    url = f"https://csstats.gg/player/{76561198108579338}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_timeout(5000)
        html = page.content()
        match = re.search(r"var\s+stats\s*=\s*(\{.*?\});", html, re.DOTALL)
        if not match:
            browser.close()
            return {}
        json_str = match.group(1)
        try:
            stats = json.loads(json_str)
        except:
            browser.close()
            return {}
        browser.close()
        return stats

def calcular_metricas_avanzadas(stats):
    resultado = {}
    fk = stats.get("FK", 0)
    fd = stats.get("FD", 0)
    resultado["entry_success_rate"] = fk / (fk + fd) if (fk + fd) > 0 else None
    resultado["entry_success_ct"] = stats.get("FK_CT_SPR")
    resultado["entry_success_t"] = stats.get("FK_T_SPR")
    resultado["assists"] = stats.get("A", 0)
    utility_damage = 0
    weapons = stats.get("weapons", {})
    for arma in ["hegrenade", "molotov", "incgrenade"]:
        dmg = weapons.get(arma, {}).get("dmg", 0)
        utility_damage += dmg
    resultado["utility_damage"] = utility_damage
    return resultado

def filtrar_stats_completo(stats):
    campos_directos = ["wr", "adr", "hs", "kpd", "rating", "1v1", "1v2", "1v3", "1v4", "1v5", "1vX"]
    resultado = {campo: stats.get(campo) for campo in campos_directos}
    resultado["rank"] = stats.get("best", {}).get("rank")
    mapas = stats.get("maps", {})
    top_mapas = sorted(mapas.items(), key=lambda item: item[1].get("played", 0), reverse=True)[:3]
    resultado["top_maps"] = [nombre for nombre, _ in top_mapas]
    resultado.update(calcular_metricas_avanzadas(stats))
    return resultado

# -------------------------------
# INTERFAZ STREAMLIT
# -------------------------------

st.title("CS2 Balanceador - Perfil de Jugador")

steam_id = st.text_input("Ingresa el SteamID64 del jugador:", "76561198108579338")

if steam_id:
    with st.spinner("Obteniendo estadísticas..."):
        stats = obtener_stats_desde_json(steam_id)
        if stats:
            perfil = filtrar_stats_completo(stats)
            st.subheader("📊 Perfil del Jugador")
            st.json(perfil)
        else:
            st.error("No se pudieron obtener las estadísticas.")