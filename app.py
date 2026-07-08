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
# SIMULASI DATABASE SERVER (EPHEMERAL DISK)
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
    
    # Menghitung nomor registrasi unik berdasarkan 5 digit terakhir NISN secara aman
    reg_suffix = str(nisn)[-5:] if (nisn and len(str(nisn)) >= 5) else "12345"
    
    baru = pd.DataFrame()
    
    df_lama = dapatkan_database()
    if not df_lama.empty:
        # Menghindari duplikasi data jika tombol diklik berkali-kali
        if str(nisn) in df_lama.astype(str).values:
            return
        df_baru = pd.concat([df_lama, baru], ignore_index=True)
    else:
        df_baru = baru
    df_baru.to_csv(file_db, index=False)

# ==========================================
# DESAIN WEBSITE: BACKGROUND GELAP & EFEK NEON KILAU
# ==========================================
st.markdown(
    """
    <style>
    /* Background Gelap Estetik & Elegan */
   .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 100%)!important;
    }
    
    /* Mengubah semua teks utama agar kontras (Putih Jernih) */
   .stApp,.stApp p,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp span,.stApp li,.stApp figcaption {
        color: #ffffff!important;
    }
    
    /* Warna teks khusus untuk status error agar tetap terbaca */
   .stAlert p {
        color: #ff4b4b!important;
    }
    
    /* Desain Menu Tab Atas agar Mengkilau */
    button[data-baseweb="tab"] {
        color: #9ca3af!important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00d2ff!important;
        border-bottom-color: #00d2ff!important;
        font-weight: bold!important;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.8)!important;
    }
    
    /* Membuat Semua Kolom Input Memiliki Efek Kilau Biru Neon */
   .stTextInput input,.stTextArea textarea,.stDateInput input {
        background-color: #1f2937!important;
        color: #ffffff!important;
        border: 2px solid #00d2ff!important; /* Border Biru Neon */
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.5)!important; /* Efek Kilau */
        border-radius: 8px!important;
    }
    
    div[data-baseweb="select"] {
        background-color: #1f2937!important;
        color: #ffffff!important;
        border: 2px solid #00d2ff!important;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.5)!important;
        border-radius: 8px!important;
    }
    
   .stTextInput input:focus,.stTextArea textarea:focus,.stDateInput input:focus {
        border-color: #00f0ff!important;
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.9)!important;
    }
    
    /* Membuat Container Tabel, Kartu Bukti, dan Info Box agar Menonjol */
    div[data-testid="stContainer"], table,.stAlert {
        background-color: #111827!important;
        border: 2px solid #00d2ff!important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4)!important;
        border-radius: 12px!important;
    }
    
    table, th, td {
        color: #ffffff!important;
        border: 1px solid #374151!important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Formulir Pendaftaran PPDB Online YPS ITIIHADUL WAQIFIN")
st.write("Silakan isi dan lengkapi data pendaftaran Anda melalui tab tahapan di bawah ini.")
st.markdown("---")

# ==========================================
# SISTEM TAB UTAMA (ANTI-RESET DATA)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["Beranda", "Pendaftaran", "Syarat", "Kontak"])

# ==========================================
# 📝 TAHAP 1: FORMULIR BIODATA
# ==========================================
with tab1:
    st.subheader("Formulir Biodata Calon Siswa")
    
    nama_lengkap = st.text_input("Nama Lengkap", key="nama")
    nisn = st.text_input("NISN (10 Digit)", max_chars=10, key="nisn_input")
    asal_sekolah = st.text_input("Asal Sekolah", key="sekolah")
    
    kolom_tempat, kolom_tanggal = st.columns(2)
    with kolom_tempat:
        tempat_lahir = st.text_input("Tempat Lahir", key="tempat")
    with kolom_tanggal:
        tanggal_lahir = st.date_input("Tanggal Lahir", value=datetime.date(2010, 1, 1), key="tanggal")
        
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["Pilih...", "Laki-laki", "Perempuan"], key="jk")
    alamat = st.text_area("Alamat Lengkap Rumah", key="alamat")
    no_hp = st.text_input("Nomor HP / WhatsApp Aktif", key="hp")
    
    st.info("💡 Selesai mengisi? Silakan langsung klik tab **'📂 Tahap 2: Berkas'** di bagian atas untuk melanjutkan.")

# ==========================================
# 📂 TAHAP 2: PENGUPLOADAN BERKAS PENTING
# ==========================================
with tab2:
    st.subheader("Penguploadan Berkas Penting")
    st.write("Silakan unggah dokumen pendukung dalam format PDF atau gambar (Maksimal 2MB per file).")
    st.markdown("---")
    
    upload_foto = st.file_uploader("Upload Pas Foto Formal (3x4)", type=["jpg", "jpeg", "png"], key="foto")
    upload_kk = st.file_uploader("Upload Kartu Keluarga (KK)", type=["pdf", "jpg", "jpeg", "png"], key="kk_file")
    upload_akta = st.file_uploader("Upload Akta Kelahiran", type=["pdf", "jpg", "jpeg", "png"], key="akta")
    upload_ijazah = st.file_uploader("Upload Ijazah / Surat Keterangan Lulus (SKL)", type=["pdf", "jpg", "jpeg", "png"], key="ijazah")
    
    st.info("💡 Selesai upload? Silakan langsung klik tab **'🔍 Tahap 3: Review Data'** di bagian atas untuk memeriksa data.")

# ==========================================
# 🔍 TAHAP 3: REVIEW & KONFIRMASI DATA
# ==========================================
with tab3:
    st.subheader("Review & Konfirmasi Data")
    st.warning("⚠️ Periksa kembali semua data Anda di bawah ini. Data yang sudah benar siap untuk dikirim!")
    st.markdown("---")
    
    st.markdown("### 📝 Rangkuman Biodata Calon Siswa")
    st.write(f"• **Nama Lengkap:** {nama_lengkap if nama_lengkap else '❌ Belum diisi'}")
    st.write(f"• **NISN:** {nisn if nisn else '❌ Belum diisi'}")
    st.write(f"• **Asal Sekolah:** {asal_sekolah if asal_sekolah else '❌ Belum diisi'}")
    st.write(f"• **Tempat, Tanggal Lahir:** {tempat_lahir if tempat_lahir else '❌ Belum diisi'}, {tanggal_lahir}")
    st.write(f"• **Jenis Kelamin:** {jenis_kelamin}")
    st.write(f"• **No. HP / WhatsApp:** {no_hp if no_hp else '❌ Belum diisi'}")
    st.write(f"• **Alamat Rumah:** {alamat if alamat else '❌ Belum diisi'}")
    
    st.markdown("---")
    st.markdown("### 📂 Status Berkas Dokumen")
    st.write(f"• Pas Foto 3x4: {'✅ Sudah Terunggah' if upload_foto is not None else '❌ Belum Terunggah'}")
    st.write(f"• Kartu Keluarga (KK): {'✅ Sudah Terunggah' if upload_kk is not None else '❌ Belum Terunggah'}")
    st.write(f"• Akta Kelahiran: {'✅ Sudah Terunggah' if upload_akta is not None else '❌ Belum Terunggah'}")
    st.write(f"• Ijazah / SKL: {'✅ Sudah Terunggah' if upload_ijazah is not None else '❌ Belum Terunggah'}")
    
    st.markdown("---")
    setuju = st.checkbox("Saya menyatakan dengan sadar bahwa semua data yang saya masukkan di atas adalah benar, sah, dan sesuai dengan dokumen aslinya.", key="persetujuan")
    
    if setuju:
        st.success("Validasi berhasil! Sekarang silakan klik tab **'🎉 Tahap 4: Selesai'** di bagian atas.")
    else:
        st.info("ℹ️ Silakan centang kotak persetujuan di atas untuk memvalidasi pendaftaran Anda.")

# ==========================================
# 🎉 TAHAP 4: STATUS PENDAFTARAN & INTEGRASI KEAMANAN
# ==========================================
with tab4:
    # 🔒 DETEKSI PINTOU BELAKANG ADMIN (Apakah URL memiliki?role=admin)
    query_params = st.query_params
    is_admin = query_params.get("role") == "admin"
    
    # ALAMAT WEBSITE PPDB GLOBAL KAMU
    LINK_PUBLIK = "https://web-ppdb-yjbhbdrxgkk2psj4jqhays.streamlit.app"
    LINK_ADMIN = "https://web-ppdb-yjbhbdrxgkk2psj4jqhays.streamlit.app/?role=admin"

    # Fungsi internal untuk membuat gambar QR Code
    def buat_qr(link_url):
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(link_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    if is_admin:
        # ==========================================
        # TAMPILAN KHUSUS LAPTOP ADMIN (AZMI)
        # ==========================================
        st.subheader("🛠️ Panel Kontrol Admin (Panitia PPDB)")
        st.write("Selamat datang Azmi! Berikut adalah database pendaftar PPDB Online yang tersimpan secara terpusat di server:")
        
        # Load database CSV terpusat
        df_pendaftar = dapatkan_database()
        
        if not df_pendaftar.empty:
            st.dataframe(df_pendaftar, use_container_width=True)
            
            # Buat tombol unduh untuk data CSV tersebut
            csv_data = df_pendaftar.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Unduh Seluruh Data Pendaftar (Excel/CSV)",
                data=csv_data,
                file_name="PPDB_2026_Database_Lengkap.csv",
                mime="text/csv",
                type="primary"
            )
        else:
            st.info("📭 Belum ada data calon siswa baru yang tersimpan di database server saat ini.")
            
        st.markdown("---")
        st.subheader("🔗 Dokumen Referensi Akses Sistem")
        
        # Tampilkan kedua link & QR Code hanya untuk referensi admin
        kolom1, kolom2 = st.columns(2)
        with kolom1:
            st.markdown("### 🌐 **Akses Publik (Siswa)**")
            st.info(f"**Link:** {LINK_PUBLIK}")
            qr_publik_img = buat_qr(LINK_PUBLIK)
            st.image(qr_publik_img, caption="QR Code Akses Publik", width=180)
        with kolom2:
            st.markdown("### 🔒 **Akses Admin (Panitia)**")
            st.warning(f"**Link:** {LINK_ADMIN}")
            qr_admin_img = buat_qr(LINK_ADMIN)
            st.image(qr_admin_img, caption="QR Code Akses Admin", width=180)

    else:
        # ==========================================
        # TAMPILAN JALUR UMUM (CALON SISWA / PUBLIK)
        # ==========================================
        if st.session_state.get("persetujuan"):
            st.subheader("Konfirmasi Final Pendaftaran")
            st.write("Silakan klik tombol di bawah ini untuk mengirimkan seluruh data Anda secara resmi ke panitia PPDB.")
            st.markdown("---")
            
            tombol_konfirmasi = st.button("🚀 Konfirmasi Pendaftaran Selesai", type="primary")
            
            if tombol_konfirmasi or st.session_state.get("is_submitted"):
                if tombol_konfirmasi and not st.session_state.get("is_submitted"):
                    st.session_state["is_submitted"] = True
                    # TULIS DATA SECARA PERMANEN KE SERVER DATABASE
                    simpan_ke_database(
                        st.session_state.get("nama"),
                        st.session_state.get("nisn_input"),
                        st.session_state.get("sekolah"),
                        st.session_state.get("hp"),
                        st.session_state.get("jk"),
                        st.session_state.get("tempat"),
                        st.session_state.get("tanggal"),
                        st.session_state.get("alamat")
                    )
                
                st.balloons()
                st.success("🎉 Sukses! Data pendaftaran Anda telah dikonfirmasi dan berhasil dikirimkan ke database sekolah.")
                st.write("Terima kasih telah melakukan pendaftaran. Proses selanjutnya akan diverifikasi oleh panitia.")
                
                st.markdown("---")
                
                # TAMPILKAN HANYA DATA PUBLIK (Siswa tidak akan pernah melihat link admin!)
                st.subheader("🔗 Link & QR Code Bukti Pendaftaran")
                st.write("Silakan simpan alamat tautan atau screenshot QR Code di bawah ini sebagai bukti sah pendaftaran Anda.")
                
                st.info(f"**Link PPDB Online:** {LINK_PUBLIK}")
                qr_publik_img = buat_qr(LINK_PUBLIK)
                st.image(qr_publik_img, caption="QR Code Akses Publik", width=180)
        else:
            st.error("🔒 Akses Dikunci: Anda harus mengisi biodata di Tahap 1, berkas di Tahap 2, dan mencentang persetujuan di Tahap 3 terlebih dahulu.")
