import streamlit as st
import datetime
import pandas as pd
import qrcode
import os
from io import BytesIO

# ==========================================
# SETUP CONTEXT & CONFIGURATION
# ==========================================
st.set_page_config(page_title="PPDB Online 2026", page_icon="📝", layout="centered")

# ==========================================
# DATABASE HANDLING (STABIL)
# ==========================================
def dapatkan_database():
    file_db = "data_pendaftar.csv"
    if os.path.exists(file_db):
        try:
            return pd.read_csv(file_db)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def simpan_ke_database(nama, nisn, sekolah, hp, jk, tempat, tanggal, alamat):
    file_db = "data_pendaftar.csv"
    
    data_baru = {
        "Nama": [nama],
        "NISN": [nisn],
        "Asal Sekolah": [sekolah],
        "No HP": [hp],
        "Jenis Kelamin": [jk],
        "Tempat Lahir": [tempat],
        "Tanggal Lahir": [str(tanggal)],
        "Alamat": [alamat]
    }
    
    df_input = pd.DataFrame(data_baru)
    df_lama = dapatkan_database()
    
    if not df_lama.empty:
        # Menghindari duplikasi NISN
        if str(nisn) in df_lama["NISN"].astype(str).values:
            return
        df_baru = pd.concat([df_lama, df_input], ignore_index=True)
    else:
        df_baru = df_input
        
    df_baru.to_csv(file_db, index=False)

# ==========================================
# DESAIN WEBSITE
# ==========================================
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #090d16 0%, #111827 100%)!important; }
    .stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp li, .stApp figcaption { color: #ffffff!important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #00d2ff!important; border-bottom-color: #00d2ff!important; font-weight: bold!important; }
    .stTextInput input, .stTextArea textarea, .stDateInput input { background-color: #1f2937!important; color: #ffffff!important; border: 2px solid #00d2ff!important; border-radius: 8px!important; }
    div[data-testid="stContainer"], table { background-color: #111827!important; border: 2px solid #00d2ff!important; border-radius: 12px!important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Formulir Pendaftaran PPDB Online YPS ITIIHADUL WAQIFIN")
tab1, tab2, tab3, tab4 = st.tabs(["Beranda", "Pendaftaran", "Syarat", "Kontak"])

with tab1:
    nama_lengkap = st.text_input("Nama Lengkap", key="nama")
    nisn = st.text_input("NISN (10 Digit)", max_chars=10, key="nisn_input")
    asal_sekolah = st.text_input("Asal Sekolah", key="sekolah")
    kolom_tempat, kolom_tanggal = st.columns(2)
    with kolom_tempat: tempat_lahir = st.text_input("Tempat Lahir", key="tempat")
    with kolom_tanggal: tanggal_lahir = st.date_input("Tanggal Lahir", value=datetime.date(2010, 1, 1), key="tanggal")
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["Pilih...", "Laki-laki", "Perempuan"], key="jk")
    alamat = st.text_area("Alamat Lengkap Rumah", key="alamat")
    no_hp = st.text_input("Nomor HP / WhatsApp Aktif", key="hp")

with tab2:
    st.write("Silakan upload berkas (Foto, KK, Akta, Ijazah).")
    upload_foto = st.file_uploader("Pas Foto", type=["jpg", "jpeg", "png"])
    upload_kk = st.file_uploader("Kartu Keluarga", type=["pdf", "jpg", "jpeg", "png"])
    upload_akta = st.file_uploader("Akta Kelahiran", type=["pdf", "jpg", "jpeg", "png"])
    upload_ijazah = st.file_uploader("Ijazah / SKL", type=["pdf", "jpg", "jpeg", "png"])

with tab3:
    st.subheader("Review & Konfirmasi")
    setuju = st.checkbox("Saya menyatakan data benar.", key="persetujuan")

with tab4:
    query_params = st.query_params
    is_admin = query_params.get("role") == "admin"
    LINK_PUBLIK = "https://web-ppdb-yjbhbdrxgkk2psj4jqhays.streamlit.app"
    
    def buat_qr(link_url):
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(link_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    if is_admin:
        st.subheader("🛠️ Panel Kontrol Admin")
        df = dapatkan_database()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Database (CSV)", csv, "data_pendaftar.csv", "text/csv")
        else:
            st.info("📭 Belum ada data.")
    else:
        if st.session_state.get("persetujuan"):
            if st.button("🚀 Konfirmasi Pendaftaran"):
                simpan_ke_database(nama_lengkap, nisn, asal_sekolah, no_hp, jenis_kelamin, tempat_lahir, tanggal_lahir, alamat)
                st.success("🎉 Berhasil dikirim!")
        st.markdown("### 🌐 Akses Publik")
        st.info(f"Link: {LINK_PUBLIK}")
        st.image(buat_qr(LINK_PUBLIK), width=150)
