import streamlit as st
from datetime import datetime
import time
from streamlit_lottie import st_lottie
import requests

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Doğum Günü",
    page_icon="🎉",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- TASARIM (CSS) - PROFESYONEL VE PARTİ HAVASI ---
st.markdown("""
<style>
    /* Google Font: Profesyonel ve Şık (Playfair Display) */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Montserrat:wght@300;600&display=swap');

    /* Arka Plan: Renk Geçişleri ve Animasyon */
    .stApp {
        background: linear-gradient(-45deg, #FF6B6B, #556270, #4ECDC4, #C7F464);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: white;
        overflow-x: hidden; /* Yan kaydırmayı engelle */
    }

    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Parti Efekti: Yukarı süzülen şekiller */
    .circles {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 0; /* Arka planda kalsın */
        pointer-events: none;
    }
    .circles li {
        position: absolute;
        display: block;
        list-style: none;
        width: 20px;
        height: 20px;
        background: rgba(255, 255, 255, 0.2);
        animation: animate 25s linear infinite;
        bottom: -150px;
        border-radius: 50%; /* Yuvarlak partiküller */
    }
    /* Farklı boyut ve konumlarda partiküller */
    .circles li:nth-child(1) { left: 25%; width: 80px; height: 80px; animation-delay: 0s; }
    .circles li:nth-child(2) { left: 10%; width: 20px; height: 20px; animation-delay: 2s; animation-duration: 12s; }
    .circles li:nth-child(3) { left: 70%; width: 20px; height: 20px; animation-delay: 4s; }
    .circles li:nth-child(4) { left: 40%; width: 60px; height: 60px; animation-delay: 0s; animation-duration: 18s; }
    .circles li:nth-child(5) { left: 65%; width: 20px; height: 20px; animation-delay: 0s; }
    .circles li:nth-child(6) { left: 75%; width: 110px; height: 110px; animation-delay: 3s; }
    .circles li:nth-child(7) { left: 35%; width: 150px; height: 150px; animation-delay: 7s; }
    .circles li:nth-child(8) { left: 50%; width: 25px; height: 25px; animation-delay: 15s; animation-duration: 45s; }
    .circles li:nth-child(9) { left: 20%; width: 15px; height: 15px; animation-delay: 2s; animation-duration: 35s; }
    .circles li:nth-child(10){ left: 85%; width: 150px; height: 150px; animation-delay: 0s; animation-duration: 11s; }

    @keyframes animate {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; border-radius: 0; }
        100% { transform: translateY(-1000px) rotate(720deg); opacity: 0; border-radius: 50%; }
    }

    /* Yazı Stili: Profesyonel */
    h1 {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        color: #FFFFFF;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
        font-size: 2.2rem !important;
        font-weight: 700;
        margin-top: -20px;
        line-height: 1.3;
        z-index: 10;
        position: relative;
    }

    /* Geri Sayım Kutusu */
    .timer-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 20px 0;
        z-index: 10;
        position: relative;
    }
    .timer-item {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 10px;
        border-radius: 8px;
        width: 75px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .timer-num { font-family: 'Montserrat', sans-serif; font-size: 1.5rem; font-weight: bold; }
    .timer-label { font-family: 'Montserrat', sans-serif; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; }

    /* FOTOĞRAF AYARLARI (SIĞDIRMA) */
    /* Streamlit'in resim kapsayıcısına müdahale ediyoruz */
    div[data-testid="stImage"] img {
        width: 100%;            /* Genişliği kolona yay */
        height: auto;           /* Yüksekliği orantılı ayarla */
        max-height: 400px;      /* Çok uzunsa 400px'te dur */
        object-fit: contain;    /* Resmi kesmeden kutuya sığdır */
        border-radius: 15px;    /* Köşeleri yuvarla */
        border: 3px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }

    /* İçeriği yukarı çekme */
    .block-container { padding-top: 1rem; }

</style>

<!-- Parti Efekti için HTML Yapısı -->
<ul class="circles">
    <li></li><li></li><li></li><li></li><li></li>
    <li></li><li></li><li></li><li></li><li></li>
</ul>
""", unsafe_allow_html=True)


# --- YARDIMCI FONKSİYONLAR ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None


# Şık bir Ay Animasyonu
lottie_moon = load_lottieurl("https://lottie.host/80ec3269-1065-4f40-951c-0e86237227d8/HqE9l5e1vj.json")
# Minik yıldızlar veya süsler
lottie_stars = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_j3u7o9.json")

# --- HEDEF TARİH ---
hedef_tarih = datetime(2025, 12, 5, 0, 0, 0)

# --- ARAYÜZ ---

# 1. Animasyon (Ay) - En Üstte Ortada
if lottie_moon:
    st_lottie(lottie_moon, height=120, key="moon", quality="high")

# 2. Profesyonel Başlık
st.markdown("""
<h1>Hilal'in Doğup<br>Dünyayı Aydınlatmasına<br>Kalan Süre</h1>
""", unsafe_allow_html=True)

# 3. Geri Sayım Sayacı (Placeholder)
placeholder = st.empty()

# 4. Fotoğraf
# Fotoğrafı ortalamak için kolon kullanıyoruz ama CSS ile sığdırmayı hallettik
col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    try:
        # Dosya adı hilal_aile.jpeg
        st.image("hilal_aile.jpeg", use_container_width=True)
    except:
        st.error("Lütfen 'hilal_aile.jpeg' dosyasını proje klasörüne ekleyin.")

# --- DÖNGÜ ---
while True:
    simdi = datetime.now()
    kalan = hedef_tarih - simdi

    if kalan.total_seconds() < 0:
        gun, saat, dakika, saniye = 0, 0, 0, 0
    else:
        gun = kalan.days
        saniye_toplam = kalan.seconds
        saat = saniye_toplam // 3600
        dakika = (saniye_toplam % 3600) // 60
        saniye = saniye_toplam % 60

    with placeholder.container():
        st.markdown(f"""
        <div class="timer-container">
            <div class="timer-item">
                <div class="timer-num">{gun}</div>
                <div class="timer-label">Gün</div>
            </div>
            <div class="timer-item">
                <div class="timer-num">{saat}</div>
                <div class="timer-label">Saat</div>
            </div>
            <div class="timer-item">
                <div class="timer-num">{dakika}</div>
                <div class="timer-label">Dk</div>
            </div>
            <div class="timer-item">
                <div class="timer-num">{saniye}</div>
                <div class="timer-label">Sn</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(1)