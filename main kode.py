import streamlit as st
import sqlite3
import hashlib
import os
import json

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

# ================= BACKUP =================
def backup():
    cursor.execute("SELECT kode_paket,nama_wilayah FROM wilayah")
    wilayah = cursor.fetchall()

    cursor.execute("SELECT nama_wilayah,lat,lon FROM koordinat")
    koordinat = cursor.fetchall()

    with open("data/backup.json","w") as f:
        json.dump({"wilayah":wilayah,"koordinat":koordinat},f)

# ================= RESTORE =================
cursor.execute("SELECT COUNT(*) FROM wilayah")
if cursor.fetchone()[0] == 0 and os.path.exists("data/backup.json"):

    with open("data/backup.json") as f:
        data = json.load(f)

    cursor.executemany(
        "INSERT INTO wilayah (kode_paket,nama_wilayah) VALUES (?,?)",
        data["wilayah"]
    )

    cursor.executemany(
        "INSERT INTO koordinat (nama_wilayah,lat,lon) VALUES (?,?,?)",
        data["koordinat"]
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

# ================= ADMIN =================
else:

    st.title("Dashboard Admin Wilayah")

    if st.button("Logout"):
        st.session_state.login=False
        st.rerun()

    # ===== TAMBAH =====
    st.subheader("Tambah Wilayah + Koordinat")

    with st.form("form"):
        kode = st.text_input("Kode Paket")
        nama = st.text_input("Nama Wilayah")
        lat = st.number_input("Latitude", format="%.6f")
        lon = st.number_input("Longitude", format="%.6f")
        simpan = st.form_submit_button("Simpan")

    if simpan:
        try:
            cursor.execute(
                "INSERT INTO wilayah (kode_paket,nama_wilayah) VALUES (?,?)",
                (kode.strip(), nama.strip())
            )

            cursor.execute(
                "INSERT INTO koordinat (nama_wilayah,lat,lon) VALUES (?,?,?)",
                (nama.strip(), lat, lon)
            )

            conn.commit()
            backup()

            st.success("Data tersimpan")
            st.rerun()

        except Exception as e:
            st.error(e)

    # ===== DATA =====
    st.subheader("Data Wilayah")

    cursor.execute("SELECT id,kode_paket,nama_wilayah FROM wilayah")
    data = cursor.fetchall()

    for row in data:

        col1,col2,col3 = st.columns([2,4,1])

        col1.write(row[1])
        col2.write(row[2])

        if col3.button("Hapus",key=row[0]):

            cursor.execute("DELETE FROM wilayah WHERE id=?", (row[0],))
            cursor.execute("DELETE FROM koordinat WHERE nama_wilayah=?", (row[2],))

            conn.commit()
            backup()
            st.rerun()

    # ===== EDIT =====
    st.divider()
    st.subheader("Edit Wilayah")

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
        SET kode_paket=?,nama_wilayah=?
        WHERE id=?
        """,(kode_baru.strip(), nama_baru.strip(), pilih[0]))

        conn.commit()
        backup()

        st.success("Update berhasil")
        st.rerun()

    if st.button("Backup Sekarang"):
        backup()
        st.success("Backup OK")
