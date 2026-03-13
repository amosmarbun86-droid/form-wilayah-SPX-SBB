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

m = folium.Map(location=[1.5,99.5],zoom_start=6)

for kode,nama in data:

    if nama in koordinat:

        lat,lon = koordinat[nama]

        folium.Marker(
            [lat,lon],
            popup=f"📦 {kode} | {nama}",
            icon=folium.Icon(color="blue",icon="truck")
        ).add_to(m)

if search:

    cursor.execute("""
    SELECT kode_paket,nama_wilayah
    FROM wilayah
    WHERE nama_wilayah LIKE ?
    """,('%'+search+'%',))

    hasil = cursor.fetchone()

    if hasil:

        kode,nama = hasil

        st.success(f"📦 Kode Paket : {kode}")
        st.info(f"📍 Wilayah : {nama}")

        if nama in koordinat:

            lat,lon = koordinat[nama]

            m = folium.Map(location=[lat,lon],zoom_start=10)

            folium.Marker(
                [lat,lon],
                popup=f"{kode} | {nama}",
                icon=folium.Icon(color="red")
            ).add_to(m)

route = st.checkbox("🚚 Tampilkan Route Pengiriman")

if route:

    route_wilayah = ["Tarutung","Balige","Sidikalang"]

    points = []

    for r in route_wilayah:

        if r in koordinat:
            points.append(koordinat[r])

    if len(points)>1:

        folium.PolyLine(points,color="red",weight=4).add_to(m)

st_folium(m,width=1000,height=600)
