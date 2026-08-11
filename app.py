import streamlit as st
from openai import OpenAI

# 1. Pengaturan Halaman
st.set_page_config(page_title="Generator Konten Edukasi", page_icon="✨")

st.title("Aplikasi Kreator: Belajar lalu Beriman")
st.write("Aplikasi untuk membuat skrip, ilustrasi, dan prompt video edukasi agama anak.")

# 2. Sidebar untuk memasukkan Kunci Keamanan (API Key)
st.sidebar.header("Pengaturan AI")
st.sidebar.write("Untuk menjalankan aplikasi ini, Anda membutuhkan kunci API dari OpenAI.")
api_key = st.sidebar.text_input("Masukkan OpenAI API Key Anda:", type="password")

# 3. Area Input Cerita
ide_konten = st.text_input(
    "Masukkan topik cerita edukasi Anda:", 
    placeholder="Misal: Aku dan Suara Keledaiku..."
)
tombol_buat = st.button("Hasilkan Konten")

# 4. Logika Pemrosesan AI
if tombol_buat:
    # Mengecek apakah API key dan topik sudah diisi
    if not api_key:
        st.warning("Mohon masukkan OpenAI API Key di bilah sebelah kiri terlebih dahulu ya!")
    elif not ide_konten:
        st.warning("Mohon masukkan topik cerita yang ingin dibuat.")
    else:
        # Menghubungkan ke OpenAI
        client = OpenAI(api_key=api_key)
        
        # Menampilkan animasi loading
        with st.spinner("AI sedang merangkai skrip dan menggambar ilustrasi untuk Anda. Mohon tunggu sebentar..."):
            try:
                # A. Perintah Membuat Skrip
                respons_skrip = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Anda adalah penulis skrip cerita edukasi agama untuk anak usia dini. Tuliskan skrip yang menyenangkan, mudah dipahami, dan memiliki pesan moral."},
                        {"role": "user", "content": f"Buatkan skrip video YouTube pendek tentang: {ide_konten}"}
                    ]
                )
                skrip_hasil = respons_skrip.choices[0].message.content
                
                # B. Perintah Membuat Instruksi Video
                respons_video = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Anda adalah sutradara animasi. Buat satu paragraf deskripsi visual yang detail untuk diubah menjadi video oleh AI pembuat video."},
                        {"role": "user", "content": f"Buatkan instruksi visual animasi tanpa suara (b-roll) untuk cerita ini: {ide_konten}"}
                    ]
                )
                prompt_video = respons_video.choices[0].message.content

                # C. Perintah Membuat Gambar (DALL-E 3)
                respons_gambar = client.images.generate(
                    model="dall-e-3",
                    prompt=f"Ilustrasi 3D ramah anak, warna cerah dan lembut, gaya buku cerita anak Islami. Topik: {ide_konten}",
                    size="1024x1024",
                    n=1,
                )
                url_gambar = respons_gambar.data[0].url

                # 5. Menampilkan Hasil di Layar
                st.success("Selesai! Berikut adalah materi konten Anda:")
                tab_skrip, tab_gambar, tab_video = st.tabs(["📝 Skrip Konten", "🎨 Ilustrasi AI", "🎬 Prompt Video"])
                
                with tab_skrip:
                    st.subheader("Skrip Cerita")
                    st.write(skrip_hasil)
                    
                with tab_gambar:
                    st.subheader("Ilustrasi Karakter & Latar")
                    st.image(url_gambar, caption=f"Ilustrasi untuk: {ide_konten}")
                    
                with tab_video:
                    st.subheader("Instruksi Adegan Video (Prompt)")
                    st.info("Salin teks di bawah ini ke pembuat video AI pilihan Anda untuk menjadikannya animasi bergerak.")
                    st.write(prompt_video)

            except Exception as e:
                # Menampilkan pesan jika terjadi kesalahan (misal: kuota API habis)
                st.error(f"Maaf, terjadi kesalahan saat menghubungi AI: {e}")
