import streamlit as st
import sqlite3
import folium
from streamlit_folium import st_folium
import os

st.title("🚚 Dashboard Logistik Wilayah")

# ================= SETUP =================
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/wilayah.db", check_same_thread=False)
cursor = conn.cursor()

# ================= AUTO INIT =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS wilayah (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kode_paket TEXT UNIQUE,
    nama_wilayah TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS koordinat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_wilayah TEXT UNIQUE,
    lat REAL,
    lon REAL
)
""")

conn.commit()

# ================= AMBIL DATA =================
cursor.execute("SELECT kode_paket,nama_wilayah FROM wilayah")
data = cursor.fetchall()

cursor.execute("SELECT nama_wilayah,lat,lon FROM koordinat")
data_koordinat = cursor.fetchall()

koordinat = {
    nama.strip().lower(): (lat, lon)
    for nama, lat, lon in data_koordinat
}

search = st.text_input("🔎 Cari Kode / Wilayah")

m = folium.Map(location=[1.5,99.5], zoom_start=6)

# ================= SEARCH =================
if search:

    keyword = "%" + search.lower() + "%"

    cursor.execute("""
        SELECT kode_paket,nama_wilayah
        FROM wilayah
        WHERE LOWER(nama_wilayah) LIKE ?
        OR LOWER(kode_paket) LIKE ?
    """,(keyword,keyword))

    hasil = cursor.fetchall()

    if hasil:

        nama_awal = hasil[0][1].strip().lower()

        if nama_awal in koordinat:
            lat, lon = koordinat[nama_awal]
            m = folium.Map(location=[lat, lon], zoom_start=10)

        for kode,nama in hasil:

            st.success(f"📦 {kode}")
            st.info(f"📍 {nama}")

            nama_fix = nama.strip().lower()

            if nama_fix in koordinat:

                lat,lon = koordinat[nama_fix]

                folium.Marker(
                    [lat,lon],
                    popup=f"{kode} | {nama}",
                    icon=folium.Icon(color="red")
                ).add_to(m)

    else:
        st.warning("Wilayah tidak ditemukan")

# ================= DEFAULT =================
else:

    for kode,nama in data:

        nama_fix = nama.strip().lower()

        if nama_fix in koordinat:

            lat,lon = koordinat[nama_fix]

            folium.Marker(
                [lat,lon],
                popup=f"{kode} | {nama}",
                icon=folium.Icon(color="blue")
            ).add_to(m)

# ================= ROUTE =================
route = st.checkbox("🚚 Tampilkan Route")

if route:

    route_wilayah = ["Tarutung","Balige","Sidikalang"]
    points = []

    for r in route_wilayah:

        r_fix = r.strip().lower()

        if r_fix in koordinat:
            points.append(koordinat[r_fix])

    if len(points)>1:
        folium.PolyLine(points,color="red",weight=4).add_to(m)

st_folium(m,width=1000,height=600)
