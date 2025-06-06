import streamlit as st
from db import buscar_nicks

st.set_page_config(page_title="CS2 Balanceador", layout="wide")
st.title("Balanceador de Equipos CS2 - 5v5")

# --- Obtener todos los jugadores desde la BD
todos_jugadores = buscar_nicks("")

# Agregar manualmente a Patrick si no está
tu_nick = "P4T"
tu_steam_id = "76561198108579338"

if not any(sid == tu_steam_id for sid, _ in todos_jugadores):
    todos_jugadores.append((tu_steam_id, tu_nick))

# --- Componente para seleccionar un jugador, evitando duplicados
def seleccionar_jugador(label, key_prefix, opciones_filtradas):
    seleccionado = st.selectbox(
        f"{label} - Seleccionar jugador",
        [""] + sorted(opciones_filtradas),
        key=f"{key_prefix}_select"
    )

    if seleccionado:
        # Obtener Steam ID correspondiente
        for sid, nick in todos_jugadores:
            if nick == seleccionado:
                return nick, sid
    return None, None

# --- Función que construye 5 selects únicos por equipo
def seleccionar_jugadores(prefix, jugadores_ocupados):
    equipo = {}
    for i in range(5):
        # Filtrar jugadores no seleccionados aún
        disponibles = [nick for sid, nick in todos_jugadores if sid not in jugadores_ocupados]
        nick, sid = seleccionar_jugador(f"Jugador {i+1} ({prefix})", f"{prefix}_{i}", disponibles)
        if nick and sid:
            equipo[nick] = sid
            jugadores_ocupados.add(sid)
    return equipo

# --- Compartir lista de jugadores ya usados
jugadores_ocupados = set()

# --- Layout de columnas para los equipos
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 Equipo A")
    equipo_a = seleccionar_jugadores("A", jugadores_ocupados)

with col2:
    st.subheader("🔴 Equipo B")
    equipo_b = seleccionar_jugadores("B", jugadores_ocupados)

# --- Confirmar equipos
st.divider()

if st.button("Confirmar equipos"):
    if len(equipo_a) == 5 and len(equipo_b) == 5:
        st.success("✅ Equipos seleccionados correctamente")
        st.write("🔵 Equipo A:", equipo_a)
        st.write("🔴 Equipo B:", equipo_b)
        # Aquí: scraping + cálculo de habilidades + balanceo
    else:
        st.warning("⚠️ Debes seleccionar 5 jugadores por equipo.")