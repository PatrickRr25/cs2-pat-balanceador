import streamlit as st
import sqlite3
from db import buscar_nicks

# Título de la aplicación
st.title("Balanceador CS2 - Equipos 5v5")

# Columnas para dos equipos
col1, col2 = st.columns(2)

# Diccionarios para guardar selección de jugadores
equipo_a = {}
equipo_b = {}

# Interfaz para ingresar jugadores
with col1:
    st.subheader("Equipo A")
    for i in range(5):
        input_text = st.text_input(f"Jugador A{i+1}", key=f"a{i}")
        if input_text:
            resultados = buscar_nicks(input_text)
            opciones = [f"{nick} ({sid})" for sid, nick in resultados]
            seleccionado = st.selectbox(f"Seleccionar A{i+1}", opciones, key=f"select_a{i}") if opciones else None
            if seleccionado:
                sid = seleccionado.split("(")[-1].replace(")", "")
                nick = seleccionado.split("(")[0].strip()
                equipo_a[nick] = sid

with col2:
    st.subheader("Equipo B")
    for i in range(5):
        input_text = st.text_input(f"Jugador B{i+1}", key=f"b{i}")
        if input_text:
            resultados = buscar_nicks(input_text)
            opciones = [f"{nick} ({sid})" for sid, nick in resultados]
            seleccionado = st.selectbox(f"Seleccionar B{i+1}", opciones, key=f"select_b{i}") if opciones else None
            if seleccionado:
                sid = seleccionado.split("(")[-1].replace(")", "")
                nick = seleccionado.split("(")[0].strip()
                equipo_b[nick] = sid

# Mostrar resultados
if st.button("Confirmar equipos"):
    if len(equipo_a) == 5 and len(equipo_b) == 5:
        st.success("Equipos cargados correctamente.")
        st.write("Equipo A:", equipo_a)
        st.write("Equipo B:", equipo_b)
        # Aquí podés llamar a la función de scraping + balanceo
    else:
        st.warning("Debes seleccionar 5 jugadores por equipo.")