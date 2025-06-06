import streamlit as st
from db import buscar_nicks

st.set_page_config(page_title="CS2 Balanceador", layout="wide")
st.title("Balanceador de Equipos CS2 - 5v5")

# Función para mostrar input con autocompletado dinámico
def autocompletar_jugador(label, key_prefix):
    search_text = st.text_input(f"{label} - Buscar nickname", key=f"{key_prefix}_text")

    resultados = buscar_nicks(search_text) if search_text else []
    opciones = [f"{nick} ({sid})" for sid, nick in resultados] if resultados else []

    seleccionado = st.selectbox(f"{label} - Seleccionar jugador", opciones, key=f"{key_prefix}_select") if opciones else None

    if seleccionado:
        sid = seleccionado.split("(")[-1].replace(")", "")
        nick = seleccionado.split("(")[0].strip()
        return nick, sid
    return None, None

# Función que permite seleccionar 5 jugadores
def seleccionar_jugadores(prefix):
    equipo = {}
    for i in range(5):
        nick, sid = autocompletar_jugador(f"Jugador {i+1} ({prefix})", f"{prefix}_{i}")
        if nick and sid:
            equipo[nick] = sid
    return equipo

# Crear dos columnas
col1, col2 = st.columns(2)

# Selección dinámica para cada equipo
with col1:
    st.subheader("Equipo A")
    equipo_a = seleccionar_jugadores("A")

with col2:
    st.subheader("Equipo B")
    equipo_b = seleccionar_jugadores("B")

# Confirmación de equipos
st.divider()
if st.button("Confirmar equipos"):
    if len(equipo_a) == 5 and len(equipo_b) == 5:
        st.success("Equipos seleccionados correctamente ✅")
        st.write("🔵 Equipo A:", equipo_a)
        st.write("🔴 Equipo B:", equipo_b)
        # Aquí se invocará scraping + cálculo de skill + balanceo
    else:
        st.warning("Debes seleccionar 5 jugadores en cada equipo.")