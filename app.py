import streamlit as st
import sqlite3
from scraper import obtener_stats

# Configuración de página
st.set_page_config(page_title="CS2 Balanceador", layout="wide")
st.title("Balanceador de Equipos CS2 - 5v5")

# --- Cargar jugadores desde base de datos
@st.cache_data
def cargar_jugadores():
    conn = sqlite3.connect("steam_friends_cs2.db")
    cursor = conn.cursor()
    cursor.execute("SELECT steam_id, nickname FROM friends")
    jugadores = cursor.fetchall()
    conn.close()
    return jugadores

# Agregar manualmente a Patrick si no está
jugadores = cargar_jugadores()
tu_steam_id = "76561198108579338"
tu_nick = "Pat"
if not any(sid == tu_steam_id for sid, _ in jugadores):
    jugadores.append((tu_steam_id, tu_nick))

# --- Función para seleccionar un jugador + scrapear sus stats
def seleccionar_jugador(label, key_prefix, disponibles):
    seleccionado = st.selectbox(
        f"{label} - Selecciona jugador",
        [""] + sorted(disponibles),
        key=f"{key_prefix}_select"
    )

    if seleccionado:
        sid = next(sid for sid, nick in jugadores if nick == seleccionado)
        st.session_state[f"{key_prefix}_nick"] = seleccionado
        st.session_state[f"{key_prefix}_sid"] = sid

        # Scraping automático si aún no existe
        if f"{key_prefix}_stats" not in st.session_state:
            st.session_state[f"{key_prefix}_stats"] = obtener_stats(sid)

        return seleccionado, sid
    return None, None

# --- Selección de equipo
def seleccionar_jugadores(prefix, jugadores_ocupados):
    equipo = {}
    for i in range(5):
        disponibles = [nick for sid, nick in jugadores if sid not in jugadores_ocupados]
        nick, sid = seleccionar_jugador(f"Jugador {i+1} ({prefix})", f"{prefix}_{i}", disponibles)
        if nick and sid:
            equipo[nick] = sid
            jugadores_ocupados.add(sid)

            # Mostrar stats en tiempo real
            stats = st.session_state.get(f"{prefix}_{i}_stats")
            if stats:
                with st.expander(f"📊 Stats de {nick}"):
                    st.write({
                        "Rank": stats["rank"],
                        "Skill": stats["skill"],
                        "K/D": stats["kd"],
                        "HS%": stats["hs"],
                        "Winrate": stats["winrate"],
                        "ADR": stats["adr"]
                    })
    return equipo

# --- Control de duplicados
jugadores_ocupados = set()

# --- Interfaz de columnas para equipos
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 Equipo A")
    equipo_a = seleccionar_jugadores("A", jugadores_ocupados)

with col2:
    st.subheader("🔴 Equipo B")
    equipo_b = seleccionar_jugadores("B", jugadores_ocupados)

# --- Confirmación final
st.divider()

if st.button("Confirmar equipos"):
    if len(equipo_a) == 5 and len(equipo_b) == 5:
        st.success("✅ Equipos seleccionados correctamente")
        st.write("🔵 Equipo A:", equipo_a)
        st.write("🔴 Equipo B:", equipo_b)
        # Aquí se puede aplicar cálculo de habilidad y balance
    else:
        st.warning("⚠️ Debes seleccionar 5 jugadores por equipo.")