
import streamlit as st
from db import buscar_nicks

st.set_page_config(page_title="CS2 Balanceador", layout="wide")
st.title("Balanceador de Equipos CS2 - 5v5")

# Obtener todos los jugadores una sola vez (búsqueda vacía devuelve todos)
todos_jugadores = buscar_nicks("")

# Extraer solo los nombres de usuario
opciones_jugadores = sorted(list({nick for _, nick in todos_jugadores}))  # eliminar duplicados y ordenar
opciones_jugadores.insert(0, "")  # Placeholder vacío

# Componente por jugador con selectbox estático
def seleccionar_jugador(label, key_prefix):
    seleccionado = st.selectbox(
        f"{label} - Seleccionar jugador",
        opciones_jugadores,
        key=f"{key_prefix}_select",
        index=0,
        placeholder="Selecciona un jugador..."
    )

    if seleccionado:
        # Obtener Steam ID desde la lista original
        for sid, nick in todos_jugadores:
            if nick == seleccionado:
                return nick, sid
    return None, None

# Función para construir 5 inputs por equipo
def seleccionar_jugadores(prefix):
    equipo = {}
    for i in range(5):
        nick, sid = seleccionar_jugador(f"Jugador {i+1} ({prefix})", f"{prefix}_{i}")
        if nick and sid:
            equipo[nick] = sid
    return equipo

# Crear columnas para equipos
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 Equipo A")
    equipo_a = seleccionar_jugadores("A")

with col2:
    st.subheader("🔴 Equipo B")
    equipo_b = seleccionar_jugadores("B")

st.divider()

if st.button("Confirmar equipos"):
    if len(equipo_a) == 5 and len(equipo_b) == 5:
        st.success("✅ Equipos seleccionados correctamente")
        st.write("🔵 Equipo A:", equipo_a)
        st.write("🔴 Equipo B:", equipo_b)
        # Aquí: scraping + cálculo de habilidades + balanceo
    else:
        st.warning("⚠️ Debes seleccionar 5 jugadores por equipo.")