import streamlit as st
import sqlite3

# Configuración de página
st.set_page_config(page_title="CS2 Balanceador", layout="wide")
st.title("Balanceador de Equipos CS2 - 5v5")

# Cargar todos los jugadores de la base de datos
@st.cache_data
def cargar_jugadores():
    conn = sqlite3.connect("steam_friends_cs2.db")
    cursor = conn.cursor()
    cursor.execute("SELECT steam_id, nickname FROM friends")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

todos_los_jugadores = cargar_jugadores()

# Componente por jugador
def autocompletar_jugador(label, key_prefix, jugadores):
    if st.session_state.get(f"{key_prefix}_final"):
        seleccionado = st.session_state[f"{key_prefix}_final"]
        st.success(f"✅ {label} seleccionado: `{seleccionado}`")
        nick = seleccionado.split(" (")[0]
        sid = seleccionado.split("(")[-1].replace(")", "")
        return nick, sid

    opciones = [f"{nick} ({sid})" for sid, nick in jugadores]

    seleccionado = st.selectbox(
        f"{label} - Escribe y selecciona jugador",
        opciones,
        key=f"{key_prefix}_select"
    )

    if seleccionado:
        st.session_state[f"{key_prefix}_final"] = seleccionado
        st.rerun()

    return None, None

# Selector de jugadores para cada equipo
def seleccionar_jugadores(prefix):
    equipo = {}
    for i in range(5):
        nick, sid = autocompletar_jugador(f"Jugador {i+1} ({prefix})", f"{prefix}_{i}", todos_los_jugadores)
        if nick and sid:
            equipo[nick] = sid
    return equipo

# Dos columnas para equipos
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 Equipo A")
    equipo_a = seleccionar_jugadores("A")

with col2:
    st.subheader("🔴 Equipo B")
    equipo_b = seleccionar_jugadores("B")

# Confirmación
st.divider()

if st.button("Confirmar equipos"):
    if len(equipo_a) == 5 and len(equipo_b) == 5:
        st.success("✅ Equipos seleccionados correctamente")
        st.write("🔵 Equipo A:", equipo_a)
        st.write("🔴 Equipo B:", equipo_b)
        # Aquí irá el scraping + skill score + balanceo
    else:
        st.warning("⚠️ Debes seleccionar 5 jugadores en cada equipo.")