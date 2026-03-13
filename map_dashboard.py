import streamlit as st
import sqlite3
import folium
from streamlit_folium import st_folium

st.title("🗺 Peta Wilayah Paket")

# ================= DATABASE =================
conn = sqlite3.connect("wilayah.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS wilayah(
id INTEGER PRIMARY KEY AUTOINCREMENT,
kode_paket TEXT,
nama_wilayah TEXT
)
""")

conn.commit()

cursor.execute("SELECT kode_paket,nama_wilayah FROM wilayah")
data = cursor.fetchall()

# ================= KOORDINAT =================
koordinat = {
"Siborong-borong":(2.2096,98.9891),
"Tarutung":(2.0123,98.9697),
"Balige":(2.3344,99.0681),
"Aceh Singkil":(2.2833,97.8000)
}

# ================= MAP =================
m = folium.Map(location=[1.5,100], zoom_start=6)

for kode,nama in data:

    if nama in koordinat:

        lat,lon = koordinat[nama]

        folium.Marker(
            location=[lat,lon],
            popup=f"{kode} - {nama}",
            icon=folium.Icon(color="blue")
        ).add_to(m)

st_folium(m,width=1000,height=600)
