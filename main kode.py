import streamlit as st
import sqlite3
import hashlib

# ================= DATABASE =================
conn = sqlite3.connect("wilayah.db", check_same_thread=False)
cursor = conn.cursor()

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
conn.commit()

# ================= DATA AWAL =================
data_wilayah = [
("1","Siborong-borong"),
("2","Gunung Meriah"),
("3","Simpang Kiri"),
("5","Penyabungan"),
("6","Natal"),
("11","Kota Pinang"),
("12","Tarutung"),
("13","Pandan"),
("14","Barus"),
("15","Dolok Sanggul"),
("16","Pangururan"),
("17","Sidikalang"),
("18-22","Sidikalang"),
("23","Garoga"),
("25","Balige"),
("26","Padang Bolak"),
("27","Barumun"),
("29","Padang Sidempuan Tenggara"),
("30","Sayur Matinggi"),
("32","Padang Sidempuan Batunadua"),
("33","Padang Sidempuan Selatan"),
("35","Porsea"),
("36","Pinang Sori"),
("37","Tapian Nauli"),
("38","Pahae Jae"),
("39","Sinunukan"),
("40","Muara Sipongi"),
("41","Batang Toru"),
("42","Angkola Barat"),
("43","Silangkitang"),
("44","Halongonan"),
("45","Kampung Rakyat"),
("46","Sipirok"),
("47","Sorkam"),
("50","Sipahutar"),
("51","Sosa"),
("52","Aceh Singkil"),
("53","Siabu"),
("54","Sultan Daulat"),
("55","Barumun Tengah"),
("56","Batang Natal"),
("57","Sirandorung"),
("58","Pollung"),
("59","Lintong Nihuta"),
("60","Parlilitan"),
("61","Simangambat"),
("62","Muara Batang Gadis"),
("63","Pakkat"),
("64","Ulu Barumun"),
("65","Simpang Kanan"),
("66","Pahae Julu"),
("67","Laguboti"),
("69","Pangaribuan"),
("70","Sipoholon"),
("71","Angkola Timur"),
("72","Muara Batang Toru"),
("73","Lumban Julu"),
("75","Sosa 2"),
("76","Sumbul"),
("77","Huristak"),
("78","Siempat Nempu"),
("79","Hutaraja Tinggi"),
("80","Salak"),
("81","Singkohor"),
("82","Ranto Baek-baek"),
("84","Siantar Naromonda"),
("90","Angkola Selatan")
]

cursor.execute("SELECT COUNT(*) FROM wilayah")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
    "INSERT INTO wilayah (kode_paket,nama_wilayah) VALUES (?,?)",
    data_wilayah
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

# ================= DASHBOARD =================
else:

    st.title("Dashboard Admin Wilayah")

    if st.button("Logout"):

        st.session_state.login=False
        st.rerun()

# ================= TAMBAH WILAYAH =================

    st.subheader("Tambah Wilayah")

    with st.form("form"):

        kode=st.text_input("Kode Paket")
        nama=st.text_input("Nama Wilayah")

        simpan=st.form_submit_button("Simpan")

    if simpan:

        try:

            cursor.execute(
            "INSERT INTO wilayah (kode_paket,nama_wilayah) VALUES (?,?)",
            (kode,nama)
            )

            conn.commit()

            st.success("Data berhasil disimpan")

            st.rerun()

        except:

            st.error("Kode sudah ada")

# ================= DATA WILAYAH =================

    st.subheader("Data Wilayah")

    cursor.execute("SELECT id,kode_paket,nama_wilayah FROM wilayah")
    data=cursor.fetchall()

    for row in data:

        col1,col2,col3=st.columns([2,4,1])

        with col1:
            st.write(row[1])

        with col2:
            st.write(row[2])

        with col3:

            if st.button("Hapus",key=row[0]):

                cursor.execute(
                "DELETE FROM wilayah WHERE id=?",
                (row[0],)
                )

                conn.commit()

                st.success("Data dihapus")

                st.rerun()

# ================= EDIT WILAYAH =================

    st.divider()

    st.subheader("Edit Wilayah")

    cursor.execute("SELECT id,kode_paket,nama_wilayah FROM wilayah")
    data_edit=cursor.fetchall()

    pilih=st.selectbox(
    "Pilih Wilayah",
    data_edit,
    format_func=lambda x:f"{x[1]} | {x[2]}"
    )

    kode_baru=st.text_input("Kode Baru",pilih[1])
    nama_baru=st.text_input("Wilayah Baru",pilih[2])

    if st.button("Update"):

        cursor.execute(
        """
        UPDATE wilayah
        SET kode_paket=?,nama_wilayah=?
        WHERE id=?
        """,
        (kode_baru,nama_baru,pilih[0])
        )

        conn.commit()

        st.success("Data diperbarui")

        st.rerun()
