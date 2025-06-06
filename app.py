import streamlit as st
import pandas as pd
import sqlite3
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.set_page_config(page_title="CS2 Balanceador", layout="wide")
st.title("Balanceador de Equipos CS2 - 5v5")

DB_PATH = "steam_friends_cs2.db"

# Cargar todos los jugadores de la base de datos
@st.cache_data
def cargar_jugadores():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT steam_id, nickname FROM friends", conn)
    conn.close()
    return df

df_jugadores = cargar_jugadores()

# Configuración para cada tabla (AgGrid)
def mostrar_selector_equipo(titulo, key):
    st.subheader(titulo)

    gb = GridOptionsBuilder.from_dataframe(df_jugadores)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_grid_options(domLayout='normal')
    gb.configure_default_column(filter=True, sortable=True, resizable=True)

    grid_options = gb.build()

    grid_response = AgGrid(
        df_jugadores,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=300,
        key=key
    )

    seleccionados = grid_response["selected_rows"]
    return seleccionados

# Dos columnas para los equipos
col1, col2 = st.columns(2)

with col1:
    seleccionados_a = mostrar_selector_equipo("🔵 Equipo A", key="equipo_a")

with col2:
    seleccionados_b = mostrar_selector_equipo("🔴 Equipo B", key="equipo_b")

st.divider()

if st.button("Confirmar equipos"):
    if len(seleccionados_a) == 5 and len(seleccionados_b) == 5:
        equipo_a = {jugador["nickname"]: jugador["steam_id"] for jugador in seleccionados_a}
        equipo_b = {jugador["nickname"]: jugador["steam_id"] for jugador in seleccionados_b}

        st.success("✅ Equipos seleccionados correctamente")
        st.write("🔵 Equipo A:", equipo_a)
        st.write("🔴 Equipo B:", equipo_b)
        # Aquí vendrá el scraping + cálculo + balance
    else:
        st.warning("⚠️ Debes seleccionar 5 jugadores en cada equipo.")