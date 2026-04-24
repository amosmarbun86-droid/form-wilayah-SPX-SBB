import streamlit as st
import sqlite3
import hashlib
import os

# ================= SETUP =================
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/wilayah.db", check_same_thread=False)
cursor = conn.cursor()

# ================= TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

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

# ================= DATA AWAL =================
data_awal = [
("1","Siborong-borong",2.2076,98.9916),
("2","Gunung Meriah",2.4500,97.8500),
("3","Simpang Kiri",2.3500,97.8000),
("5","Penyabungan",0.8615,99.5452),
("6","Natal",0.5500,99.1200),
("11","Kota Pinang",1.9150,100.0950),
("12","Tarutung",2.0172,98.9668),
("13","Pandan",1.6856,98.8192),
("14","Barus",2.0125,98.3987),
("15","Dolok Sanggul",2.3303,98.7510),
("16","Pangururan",2.6426,98.7133),
("17","Sidikalang",2.7425,98.3125),
("18-22","Sidikalang",2.7425,98.3125),
("23","Garoga",2.1400,98.7500),
("25","Balige",2.3333,99.0667),
("26","Padang Bolak",1.5000,99.7500),
("27","Barumun",1.3000,99.7000),
("29","Padang Sidempuan Tenggara",1.3800,99.2700),
("30","Sayur Matinggi",1.3000,99.3500),
("32","Padang Sidempuan Batunadua",1.4000,99.3000),
("33","Padang Sidempuan Selatan",1.3700,99.2800),
("35","Porsea",2.5667,99.0833),
("36","Pinang Sori",1.5500,98.9000),
("37","Tapian Nauli",1.6500,98.8000),
("38","Pahae Jae",2.0500,98.8500),
("39","Sinunukan",0.8000,99.4000),
("40","Muara Sipongi",0.9500,99.6000),
("41","Batang Toru",1.5300,99.0700),
("42","Angkola Barat",1.4500,99.2000),
("43","Silangkitang",1.9500,100.1500),
("44","Halongonan",1.7000,99.9000),
("45","Kampung Rakyat",2.0000,100.1000),
("46","Sipirok",1.6500,99.3000),
("47","Sorkam",1.9000,98.7000),
("50","Sipahutar",2.2833,99.0000),
("51","Sosa",1.4000,100.0000),
("52","Aceh Singkil",2.3000,97.8000),
("53","Siabu",1.2000,99.5000),
("54","Sultan Daulat",2.7000,97.9000),
("55","Barumun Tengah",1.3500,99.8000),
("56","Batang Natal",0.7500,99.5000),
("57","Sirandorung",1.8500,98.9000),
("58","Pollung",2.4000,98.7000),
("59","Lintong Nihuta",2.2500,98.9000),
("60","Parlilitan",2.5500,98.6000),
("61","Simangambat",1.5500,100.0000),
("62","Muara Batang Gadis",0.7000,99.3000),
("63","Pakkat",2.4500,98.5000),
("64","Ulu Barumun",1.2500,99.8000),
("65","Simpang Kanan",2.3500,97.8500),
("66","Pahae Julu",2.1000,98.9000),
("67","Laguboti",2.4500,99.0500),
("69","Pangaribuan",2.2000,98.8000),
("70","Sipoholon",2.0333,98.9333),
("71","Angkola Timur",1.4500,99.3000),
("72","Muara Batang Toru",1.4000,99.0500),
("73","Lumban Julu",2.5833,99.1333),
("74","Lubuk barumun",1.3000,99.8500),
("75","Sosa 2",1.4200,100.0200),
("76","Sumbul",2.6000,98.5000),
("77","Huristak",1.5000,99.9000),
("78","Siempat Nempu",2.8000,98.3000),
("79","Hutaraja Tinggi",1.3500,99.9000),
("80","Salak",2.5500,98.3000),
("81","Singkohor",2.4000,97.9000),
("82","Ranto Baek-baek",0.9000,99.4000),
("84","Siantar Naromonda",2.4500,99.2000),
("86","Simanindo",2.6500,98.8000),
("87","Sibabangun",1.830,98.7800),
("90","Angkola Selatan",1.4000,99.2500),
("91","palipi",2.6500,98.6000),
("92","Adian koting",2.1000,98.7000),
("93","Rundeng",2.6500,97.9500),
("94","Tampahan",2.565,99.0600),
("95","Saipar dolok",1.530,99.0500),
]

cursor.execute("SELECT COUNT(*) FROM wilayah")
if cursor.fetchone()[0] == 0:
    for kode,nama,lat,lon in data_awal:

        cursor.execute(
            "INSERT OR IGNORE INTO wilayah (kode_paket,nama_wilayah) VALUES (?,?)",
            (kode,nama)
        )

        cursor.execute(
            "INSERT OR IGNORE INTO koordinat (nama_wilayah,lat,lon) VALUES (?,?,?)",
            (nama,lat,lon)
        )

    conn.commit()

# ================= LOGIN =================
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def login(u,p):
    cursor.execute(
        "SELECT * FROM admin WHERE username=? AND password=?",
        (u,hash_password(p))
    )
    return cursor.fetchone()

cursor.execute("SELECT * FROM admin")
if cursor.fetchone() is None:
    cursor.execute(
        "INSERT INTO admin (username,password) VALUES (?,?)",
        ("admin",hash_password("admin123"))
    )
    conn.commit()

if "login" not in st.session_state:
    st.session_state.login=False

# ================= LOGIN PAGE =================
if not st.session_state.login:

    st.title("Login Admin")

    u=st.text_input("Username")
    p=st.text_input("Password",type="password")

    if st.button("Login"):
        if login(u,p):
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Login salah")

# ================= DASHBOARD ADMIN =================
else:

    st.title("Dashboard Admin Wilayah")

    if st.button("Logout"):
        st.session_state.login=False
        st.rerun()

    # ================= TAMBAH =================
    st.subheader("Tambah Wilayah")

    with st.form("form"):
        kode = st.text_input("Kode Paket")
        nama = st.text_input("Nama Wilayah")
        lat = st.number_input("Latitude", format="%.6f")
        lon = st.number_input("Longitude", format="%.6f")
        simpan = st.form_submit_button("Simpan")

    if simpan:

        if not kode or not nama:
            st.warning("Kode & nama wajib diisi")
        else:
            try:
                cursor.execute(
                    "INSERT INTO wilayah (kode_paket,nama_wilayah) VALUES (?,?)",
                    (kode.strip(), nama.strip())
                )

                cursor.execute(
                    "INSERT OR IGNORE INTO koordinat (nama_wilayah,lat,lon) VALUES (?,?,?)",
                    (nama.strip(), lat, lon)
                )

                conn.commit()

                st.success("Data berhasil ditambahkan")
                st.rerun()

            except:
                st.error("Kode sudah ada")

    # ================= DATA =================
    st.subheader("Data Wilayah")

    cursor.execute("SELECT id,kode_paket,nama_wilayah FROM wilayah")
    data = cursor.fetchall()

    if len(data) == 0:

        st.warning("Belum ada data wilayah")

    else:

        for row in data:

            col1,col2,col3 = st.columns([2,4,1])

            col1.write(row[1])
            col2.write(row[2])

            if col3.button("Hapus",key=row[0]):

                cursor.execute("DELETE FROM wilayah WHERE id=?", (row[0],))
                cursor.execute("DELETE FROM koordinat WHERE nama_wilayah=?", (row[2],))

                conn.commit()

                st.success("Data dihapus")
                st.rerun()

    # ================= EDIT =================
    st.divider()
    st.subheader("Edit Wilayah")

    if len(data) == 0:

        st.warning("Belum ada data untuk diedit")

    else:

        pilih = st.selectbox(
            "Pilih Wilayah",
            data,
            format_func=lambda x:f"{x[1]} | {x[2]}"
        )

        kode_baru = st.text_input("Kode Baru", pilih[1])
        nama_baru = st.text_input("Wilayah Baru", pilih[2])

        if st.button("Update"):

            cursor.execute("""
            UPDATE wilayah
            SET kode_paket=?, nama_wilayah=?
            WHERE id=?
            """,(kode_baru.strip(), nama_baru.strip(), pilih[0]))

            conn.commit()

            st.success("Data diperbarui")
            st.rerun()
