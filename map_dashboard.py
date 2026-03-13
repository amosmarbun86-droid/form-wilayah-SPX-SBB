import streamlit as st
import sqlite3
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Peta Wilayah Paket",
    page_icon="🗺",
    layout="wide"
)

st.title("🗺 Peta Wilayah Paket")

# ================= DATABASE =================
conn = sqlite3.connect("wilayah.db")
cursor = conn.cursor()

cursor.execute("SELECT kode_paket,nama_wilayah FROM wilayah")
data = cursor.fetchall()

# ================= KOORDINAT =================
koordinat = {
"Siborong-borong":(2.2096,98.9891),
"Tarutung":(2.0123,98.9697),
"Balige":(2.3344,99.0681),
"Aceh Singkil":(2.2833,97.8000),
"Sidikalang":(2.7420,98.3127),
"Pinang Sori":(1.5570,98.9013),
"Salak":(2.6800,98.4100)
}

# ================= MAP =================
m = folium.Map(
    location=[1.5,100],
    zoom_start=6
)

# ================= MARKER =================
for kode,nama in data:

    if nama in koordinat:

        lat,lon = koordinat[nama]

        folium.Marker(
            location=[lat,lon],
            popup=f"{kode} - {nama}",
            icon=folium.Icon(color="blue",icon="truck")
        ).add_to(m)

# ================= ROUTE =================
route = [
koordinat["Siborong-borong"],
koordinat["Tarutung"],
koordinat["Balige"]
]

folium.PolyLine(
route,
color="red",
weight=4
).add_to(m)

st_folium(m,width=1000,height=600)
