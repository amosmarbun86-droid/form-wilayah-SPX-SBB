import streamlit as st
import sqlite3
import folium
from streamlit_folium import st_folium
from koordinat_wilayah import koordinat

st.title("🚚 Dashboard Logistik Wilayah")

conn = sqlite3.connect("wilayah.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT kode_paket,nama_wilayah FROM wilayah")
data = cursor.fetchall()

search = st.text_input("🔎 Cari Wilayah")

# 🔥 normalisasi koordinat
koordinat_fix = {k.strip().lower(): v for k,v in koordinat.items()}

m = folium.Map(location=[1.5,99.5],zoom_start=6)

# ================= MARKER =================
for kode,nama in data:

    nama_fix = nama.strip().lower()

    if nama_fix in koordinat_fix:

        lat,lon = koordinat_fix[nama_fix]

        folium.Marker(
            [lat,lon],
            popup=f"📦 {kode} | {nama}",
            icon=folium.Icon(color="blue",icon="truck")
        ).add_to(m)

# ================= SEARCH =================
if search:

    cursor.execute("""
    SELECT kode_paket,nama_wilayah
    FROM wilayah
    WHERE nama_wilayah LIKE ?
    """,('%'+search+'%',))

    hasil = cursor.fetchall()

    for kode,nama in hasil:

        st.success(f"📦 {kode}")
        st.info(f"📍 {nama}")

        nama_fix = nama.strip().lower()

        if nama_fix in koordinat_fix:

            lat,lon = koordinat_fix[nama_fix]

            folium.Marker(
                [lat,lon],
                popup=f"{kode} | {nama}",
                icon=folium.Icon(color="red")
            ).add_to(m)

# ================= ROUTE =================
route = st.checkbox("🚚 Tampilkan Route Pengiriman")

if route:

    route_wilayah = ["Tarutung","Balige","Sidikalang"]

    points = []

    for r in route_wilayah:

        r_fix = r.strip().lower()

        if r_fix in koordinat_fix:
            points.append(koordinat_fix[r_fix])

    if len(points)>1:
        folium.PolyLine(points,color="red",weight=4).add_to(m)

# ================= SHOW MAP =================
st_folium(m,width=1000,height=600)
