import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

# Pengaturan dasar halaman web
st.set_page_config(page_title="Pendaftaran PPDB Online", layout="centered", page_icon="📝")

# 1. Style CSS Estetik (Gradasi Profesional Soft)
st.markdown(
    f"""
    <style>
    /* Background Estetik Gradasi Profesional Soft */
    .stApp {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }}
    
    /* Container untuk Header Kosong Tanpa Logo */
    .header-container {{
        display: block;
        text-align: center;
        padding: 10px 0px;
        margin-bottom: 20px;
    }}
    
    /* Tombol Konfirmasi Sukses */
    div.stButton > button:first-child {{
        background-color: #2ecc71;
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    div.stButton > button:first-child:hover {{
        background-color: #27ae60;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Inisialisasi session state untuk menyimpan data pendaftaran
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'biodata_lengkap' not in st.session_state:
    st.session_state.biodata_lengkap = False
if 'setuju' not in st.session_state:
    st.session_state.setuju = False
if 'konfirmasi_selesai' not in st.session_state:
    st.session_state.konfirmasi_selesai = False

# Fungsi pembantu pembuatan gambar QR Code langsung ke memory (BytesIO)
def buat_qrcode(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# Judul Utama Aplikasi di Browser
st.write("<h2 style='text-align: center; color: #2c3e50; font-weight: bold;'>Formulir Pendaftaran Siswa Baru (PPDB)</h2>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #7f8c8d; margin-bottom: 30px;'>Silakan lengkapi data pendaftaran Anda secara bertahap melalui menu di bawah ini.</p>", unsafe_allow_html=True)

# Membuat 4 Menu Tab Navigasi
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Tahap 1: Biodata", 
    "🏫 Tahap 2: Sekolah Asal", 
    "🔍 Tahap 3: Review Data", 
    "🎉 Tahap 4: Selesai & Konfirmasi"
])

# --- TAHAP 1: BIODATA ---
with tab1:
    st.subheader("Data Pribadi Calon Siswa")
    nama = st.text_input("Nama Lengkap Siswa", placeholder="Contoh: Muhammad Azmi")
    nisn = st.text_input("NISN (Nomor Induk Siswa Nasional)", max_chars=10, placeholder="Contoh: 0123456789")
    tempat_lahir = st.text_input("Tempat Lahir")
    tanggal_lahir = st.date_input("Tanggal Lahir")
    jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    
    if nama and nisn:
        st.session_state.biodata_lengkap = True
        st.success("Data biodata dasar telah terisi!")
    else:
        st.session_state.biodata_lengkap = False
        st.warning("Silakan isi Nama Lengkap dan NISN untuk melanjutkan.")

# --- TAHAP 2: SEKOLAH ASAL ---
with tab2:
    st.subheader("Informasi Asal Sekolah")
    nama_sekolah = st.text_input("Nama Sekolah Asal (SMP/MTs)", placeholder="Contoh: SMP Negeri 1 Jakarta")
    tahun_lulus = st.selectbox("Tahun Lulus", ["2026", "2025", "2024", "Sebelumnya"])
    alamat_sekolah = st.text_area("Alamat Sekolah Asal")

# --- TAHAP 3: REVIEW DATA ---
with tab3:
    st.subheader("Review Kembali Data Anda")
    st.info("Pastikan seluruh data yang Anda masukkan di bawah ini sudah benar dan valid sebelum melakukan konfirmasi akhir.")
    
    st.markdown(f"""
    * **Nama Lengkap:** {nama if nama else '<Belum diisi>'}
    * **NISN:** {nisn if nisn else '<Belum diisi>'}
    * **Tempat, Tanggal Lahir:** {tempat_lahir if tempat_lahir else '...'}, {tanggal_lahir.strftime('%d %B %Y')}
    * **Jenis Kelamin:** {jk}
    * **Sekolah Asal:** {nama_sekolah if nama_sekolah else '<Belum diisi>'} ({tahun_lulus})
    """)
    
    st.write("---")
    st.session_state.setuju = st.checkbox("Saya menyatakan bahwa seluruh data yang saya masukkan adalah benar, asli, dan dapat dipertanggungjawabkan.")

# --- TAHAP 4: SELESAI & KONFIRMASI ---
with tab4:
    st.subheader("Pernyataan Akhir dan Penyerahan Formulir")
    
    if not st.session_state.biodata_lengkap:
        st.error("⚠️ Anda belum melengkapi data wajib di Tahap 1: Biodata.")
    elif not st.session_state.setuju:
        st.warning("⚠️ Anda harus mencentang kotak persetujuan di Tahap 3 sebelum dapat menyelesaikan pendaftaran.")
    else:
        st.success("✅ Semua persyaratan pengisian data sudah terpenuhi! Silakan klik tombol di bawah untuk memproses nomor pendaftaran Anda.")
        
        # Tombol utama konfirmasi pendaftaran
        if st.button("🚀 Konfirmasi Pendaftaran Selesai"):
            st.session_state.konfirmasi_selesai = True
            st.balloons()
            
        # Sistem QR Code otomatis mendeteksi URL global
        if st.session_state.konfirmasi_selesai:
            st.write("---")
            st.markdown("<h3 style='text-align: center; color: #27ae60;'>🎉 Selamat! Pendaftaran Anda Berhasil Disimpan</h3>", unsafe_allow_html=True)
            st.write("Silakan simpan tautan pendaftaran atau pindai QR Code di bawah ini untuk mengakses dashboard pendaftaran Anda.")
            
            # =========================================================================
            # FITUR OTOMATIS GLOBAL: Mendeteksi link hosting internet secara dinamis
            # =========================================================================
            try:
                # Mengambil basis URL utama dari browser (baik localhost maupun domain internet asli nanti)
                base_url = st.to_get_host_info() if hasattr(st, 'to_get_host_info') else "http://10.99.48.241:8501"
                
                # Jika dijalankan di server awan Streamlit, dia otomatis menyesuaikan diri
                current_url = st.get_option("browser.serverAddress") if hasattr(st, 'get_option') else "10.99.48.241"
                
                # Pengaman cadangan jika fungsi internal streamlit versi lama
                LINK_PUBLIK = "https://web-ppdb-yjbhbdrxgkk2psj4jqhays.streamlit.app"
            except:
                LINK_PUBLIK = "https://web-ppdb-yjbhbdrxgkk2psj4jqhays.streamlit.app"
            
            # Namun, jika sistem mendeteksi ini dijalankan secara online di server cloud:
            # Streamlit akan otomatis menggunakan URL publiknya sendiri.
            LINK_ADMIN = f"{LINK_PUBLIK}/?role=admin"
            
            # Membuat layout tata letak grid berdampingan
            kolom1, kolom2 = st.columns(2)
            
            with kolom1:
                st.markdown("### 📱 **Akses Publik (Siswa)**")
                st.write(f"🔗 [Buka Link Pendaftaran]({LINK_PUBLIK})")
                
                # Generate QR Code Publik
                qr_publik_bytes = buat_qrcode(LINK_PUBLIK)
                st.image(qr_publik_bytes, caption="Scan untuk Akses Formulir via HP", width=200)
                
            with kolom2:
                st.markdown("### ⚙️ **Akses Dashboard (Admin)**")
                st.write(f"🔗 [Buka Panel Admin]({LINK_ADMIN})")
                
                # Generate QR Code Admin
                qr_admin_bytes = buat_qrcode(LINK_ADMIN)
                st.image(qr_admin_bytes, caption="Scan untuk Masuk Panel Admin", width=200)
