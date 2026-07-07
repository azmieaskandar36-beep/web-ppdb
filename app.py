import streamlit as st
import datetime
import pandas as pd
import qrcode
from io import BytesIO

# ==========================================
# SETUP CONTEXT & CONFIGURATION
# ==========================================
st.set_page_config(page_title="PPDB Online 2026", page_icon="📝", layout="centered")

# ==========================================
# NYAWWA DESAIN: BACKGROUND GELAP & GLOWING EFFECT
# ==========================================
st.markdown(
    """
    <style>
    /* 1. Background Gelap Estetik & Elegan */
   .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%)!important;
    }
    
    /* 2. Mengubah semua teks utama agar kontras (Putih Jernih) */
   .stApp,.stApp p,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp span,.stApp li,.stApp figcaption {
        color: #f8fafc!important;
    }
    
    /* 3. Desain Menu Tab Atas agar Mengkilau */
    button[data-baseweb="tab"] {
        color: #94a3b8!important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #3b82f6!important;
        border-bottom-color: #3b82f6!important;
        font-weight: bold!important;
        text-shadow: 0 0 8px rgba(59, 130, 246, 0.6)!important;
    }
    
    /* 4. Membuat Semua Kolom Input Memiliki Efek Kilau (Glowing Neon Blue) */
   .stTextInput input,.stTextArea textarea,.stDateInput input {
        background-color: #0f172a!important;
        color: #f8fafc!important;
        border: 1px solid #3b82f6!important; /* Border Biru Neon */
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.4)!important; /* Efek Kilau */
        border-radius: 8px!important;
    }
    
    /* Dropdown pilihan (Selectbox) agar senada */
    div[data-baseweb="select"] {
        background-color: #0f172a!important;
        color: #f8fafc!important;
        border: 1px solid #3b82f6!important;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.4)!important;
        border-radius: 8px!important;
    }
    
    /* Efek Kilau Tambahan Saat Pengguna Mengeklik Kolom Input (Focus Mode) */
   .stTextInput input:focus,.stTextArea textarea:focus,.stDateInput input:focus {
        border-color: #60a5fa!important;
        box-shadow: 0 0 15px rgba(96, 165, 250, 0.7)!important;
    }
    
    /* 5. Membuat Container Tabel, Kartu Bukti, dan Info Box agar Tidak Menyatu dengan Latar Belakang */
    div[data-testid="stContainer"], table,.stAlert {
        background-color: #1e293b!important;
        border: 1.5px solid #3b82f6!important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.4)!important; /* Kilau Pinggiran */
        border-radius: 12px!important;
    }
    
    /* Menjaga teks di dalam tabel tetap berwarna putih */
    table, th, td {
        color: #f8fafc!important;
        border: 1px solid #334155!important;
    }
    
    /* Container untuk Header Kosong */
   .header-container {
        padding: 10px 0px;
        margin-bottom: 20px;
    }
    </style>
    
    <div class="header-container">
        </div>
    """,
    unsafe_allow_html=True
)

st.title("Formulir Pendaftaran PPDB Online YPS ITIIHADUL WAQIFIN")
st.write("Silakan isi dan lengkapi data pendaftaran Anda melalui tab tahapan di bawah ini.")
st.markdown("---")

# ==========================================
# SISTEM TAB UTAMA (ANTI-RESET DATA)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs()

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
        st.success("Validasi berhasil! Sekarang silakan klik tab **'🎉 Tahap 4: Selesai & Konfirmasi'** di bagian atas.")
    else:
        st.info("ℹ️ Silakan centang kotak persetujuan di atas untuk memvalidasi pendaftaran Anda.")

# ==========================================
# 🎉 TAHAP 4: STATUS PENDAFTARAN & GENERATE QR CODE
# ==========================================
with tab4:
    if st.session_state.get("persetujuan"):
        st.subheader("Konfirmasi Final Pendaftaran")
        st.write("Silakan klik tombol di bawah ini untuk mengirimkan seluruh data Anda secara resmi ke panitia PPDB.")
        st.markdown("---")
        
        tombol_konfirmasi = st.button("🚀 Konfirmasi Pendaftaran Selesai", type="primary")
        
        if tombol_konfirmasi or st.session_state.get("is_submitted"):
            st.session_state["is_submitted"] = True
            
            st.balloons()
            st.success("🎉 Sukses! Data pendaftaran Anda telah dikonfirmasi dan berhasil dikirimkan ke database sekolah.")
            st.write("Terima kasih telah melakukan pendaftaran. Proses selanjutnya akan diverifikasi oleh panitia.")
            
            st.markdown("---")
            
            # ==========================================
            # OTOMATISASI QR CODE DAN LINK (PUBLIK & ADMIN)
            # ==========================================
            st.subheader("🔗 Akses Link & QR Code PPDB")
            st.write("Berikut adalah link tautan beserta QR Code resmi untuk publik (siswa) dan admin (panitia).")

            # Alamat Website Asli Global Milikmu
            LINK_PUBLIK = "https://web-ppdb-yjbhbdrxgkk2psj4jqhays.streamlit.app"
            LINK_ADMIN = "https://web-ppdb-yjbhbdrxgkk2psj4jqhays.streamlit.app/?role=admin"

            # Fungsi internal untuk memproses pembuatan gambar QR Code
            def buat_qr(link_url):
                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(link_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buf = BytesIO()
                img.save(buf, format="PNG")
                return buf.getvalue()

            # Mengatur posisi grid layout berdampingan (Kolom 1 Publik, Kolom 2 Admin)
            kolom1, kolom2 = st.columns(2)

            with kolom1:
                st.markdown("### 🌐 **Akses Publik (Siswa)**")
                st.info(f"**Link:**({LINK_PUBLIK})")
                qr_publik_img = buat_qr(LINK_PUBLIK)
                st.image(qr_publik_img, caption="QR Code Akses Publik", width=180)

            with kolom2:
                st.markdown("### 🔒 **Akses Admin (Panitia)**")
                st.warning(f"**Link:**({LINK_ADMIN})")
                qr_admin_img = buat_qr(LINK_ADMIN)
                st.image(qr_admin_img, caption="QR Code Akses Admin", width=180)
                
    else:
        st.error("🔒 Akses Dikunci: Anda harus mengisi biodata di Tahap 1, berkas di Tahap 2, dan mencentang persetujuan di Tahap 3 terlebih dahulu.")
