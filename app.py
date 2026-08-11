import streamlit as st
import google.generativeai as genai

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Generator Konten Edukasi Anak", page_icon="📚", layout="centered")

st.title("Aplikasi Kreator: Belajar lalu Beriman")
st.write("Aplikasi untuk membuat skrip, ilustrasi, dan prompt video edukasi agama anak menggunakan Gemini.")

# Sidebar untuk memasukkan API Key Gemini
st.sidebar.header("Pengaturan AI")
st.sidebar.write("Untuk menjalankan aplikasi ini, masukkan Gemini API Key kamu.")
api_key = st.sidebar.text_input("Masukkan Google Gemini API Key:", type="password")

# Kolom input topik cerita dari pengguna
topic = st.text_area("Masukkan topik cerita edukasi Anda:", placeholder="Contoh: seorang anak muslimah yang sabar saat belajar mengaji...")

if st.button("Hasilkan Konten"):
    if not api_key:
        st.warning("⚠️ Silakan masukkan Google Gemini API Key terlebih dahulu di sidebar sebelah kiri.")
    elif not topic:
        st.warning("⚠️ Silakan tulis topik cerita edukasi terlebih dahulu.")
    else:
        try:
            # Konfigurasi API Gemini
            genai.configure(api_key=api_key)
            # Menggunakan model Gemini terbaru yang cepat dan cerdas
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt_lengkap = f"""
            Bertindaklah sebagai penulis konten edukasi anak yang kreatif dan Islami. 
            Buatkan untuk topik berikut: "{topic}"
            Berikan output dalam 3 bagian:
            1. Skrip Cerita Singkat
            2. Ide/Deskripsi Ilustrasi Gambar
            3. Prompt Video AI
            """
            
            with st.spinner("Sedang meracik konten ajaib untukmu..."):
                response = model.generate_content(prompt_lengkap)
                
            st.success("Yeay, konten berhasil dibuat!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
