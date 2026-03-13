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

cursor.execute("SELECT kode_paket,nama_wilayah FROM wilayah")
data = cursor.fetchall()

# ================= KOORDINAT =================
koordinat = {

"Siborong-borong":(2.2096,98.9891),
"Gunung Meriah":(2.4500,97.9500),
"Simpang Kiri":(2.2700,97.7800),
"Penyabungan":(0.8667,99.5500),
"Natal":(0.5500,99.1500),
"Kota Pinang":(1.9000,100.1000),
"Tarutung":(2.0123,98.9697),
"Pandan":(1.6800,98.7800),
"Barus":(2.0000,98.4000),
"Dolok Sanggul":(2.4600,98.4400),
"Pangururan":(2.6200,98.6300),
"Sidikalang":(2.7420,98.3127),
"Garoga":(2.1800,98.8600),
"Balige":(2.3344,99.0681),
"Padang Bolak":(1.4100,99.6500),
"Barumun":(1.4100,100.0000),
"Porsea":(2.1600,99.0600),
"Pinang Sori":(1.5570,98.9013),
"Tapian Nauli":(1.6900,98.8500),
"Pahae Jae":(2.1500,98.8200),
"Sinunukan":(0.8000,99.3500),
"Batang Toru":(1.7200,99.0700),
"Angkola Barat":(1.6500,99.1000),
"Sipirok":(1.6300,99.2600),
"Sorkam":(1.8000,98.7500),
"Sipahutar":(2.1800,99.0400),
"Sosa":(1.4500,100.1000),
"Aceh Singkil":(2.2833,97.8000),
"Siabu":(1.0200,99.6000),
"Pollung":(2.4500,98.5400),
"Lintong Nihuta":(2.2600,98.8500),
"Parlilitan":(2.5800,98.4600),
"Pakkat":(2.3400,98.3200),
"Simpang Kanan":(2.4000,97.8800),
"Pahae Julu":(2.0500,98.9200),
"Laguboti":(2.2700,99.1000),
"Pangaribuan":(2.0700,99.0700),
"Sipoholon":(2.0600,98.9400),
"Angkola Timur":(1.5400,99.1700),
"Muara Batang Toru":(1.6200,99.0600),
"Lumban Julu":(2.5200,98.9200),
"Sumbul":(2.5700,98.5500),
"Siempat Nempu":(2.8300,98.2800),
"Salak":(2.6800,98.4100),
"Singkohor":(2.3300,97.9200),
"Ranto Baek-baek":(0.9000,99.4000),
"Siantar Naromonda":(2.3000,99.1500),
"Angkola Selatan":(1.5200,99.2500)

}

# ================= MAP =================
m = folium.Map(location=[1.5,100], zoom_start=6)

for kode,nama in data:

    if nama in koordinat:

        lat,lon = koordinat[nama]

        folium.Marker(
            location=[lat,lon],
            popup=f"{kode} - {nama}",
            icon=folium.Icon(color="blue",icon="truck")
        ).add_to(m)

st_folium(m,width=1000,height=600)
