import streamlit as st
from db import buscar_nicks

st.set_page_config(page_title="CS2 Balanceador", layout="wide")
st.title("Balanceador de Equipos CS2 - 5v5")

# Componente por jugador con UX mejorado
def autocompletar_jugador(label, key_prefix):
    # Ya seleccionado
    if st.session_state.get(f"{key_prefix}_seleccionado", False):
        seleccionado = st.session_state.get(f"{key_prefix}_final")
        st.success(f"✅ {label} seleccionado: `{seleccionado}`")
        sid = seleccionado.split("(")[-1].replace(")", "")
        nick = seleccionado.split(" (")[0]
        return nick, sid

    # Entrada de texto
    search_text = st.text_input(
        f"{label} - Buscar nickname",
        placeholder="Nickname",
        key=f"{key_prefix}_text"
    )

    # Mostrar botón para buscar
    buscar = st.button("🔍 Buscar", key=f"{key_prefix}_buscar")

    if buscar:
        resultados = buscar_nicks(search_text)
        if not resultados:
            st.info("❌ No se encontraron coincidencias.")
        else:
            opciones = [f"{nick} ({sid})" for sid, nick in resultados]
            seleccionado = st.selectbox(
                f"{label} - Selecciona jugador",
                opciones,
                key=f"{key_prefix}_select"
            )
            if seleccionado:
                st.session_state[f"{key_prefix}_seleccionado"] = True
                st.session_state[f"{key_prefix}_final"] = seleccionado
                st.rerun()

    return None, None

# Función para construir 5 inputs por equipo
def seleccionar_jugadores(prefix):
    equipo = {}
    for i in range(5):
        nick, sid = autocompletar_jugador(f"Jugador {i+1} ({prefix})", f"{prefix}_{i}")
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