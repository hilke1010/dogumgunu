import streamlit as st
from datetime import datetime
import time
from streamlit_lottie import st_lottie
import requests

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Mutlu Yıllar Hilal!",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS TASARIMI (HIZLI RENKLER VE ŞIKLIK) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display:wght@700&family=Montserrat:wght@600&display=swap');

    /* HIZLI AKAN RENKLİ ARKA PLAN (3 Saniye) */
    .stApp {
        background: linear-gradient(-45deg, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #9400D3);
        background-size: 400% 400%;
        animation: gradientBG 3s ease infinite; /* 3 saniye yaptık, çok hızlı akacak */
        color: white;
    }
    
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Hilal İkonu */
    .hilal-icon {
        font-size: 5rem;
        text-align: center;
        text-shadow: 0 0 20px #FFF, 0 0 40px #FFD700;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float { 0%{transform: translateY(0px);} 50%{transform: translateY(-20px);} 100%{transform: translateY(0px);} }

    /* Başlık */
    h1 {
        font-family: 'Playfair Display', serif;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
        text-align: center;
        font-size: 2.2rem !important;
        margin-bottom: 10px;
    }

    /* Geri Sayım Kutuları */
    .timer-container {
        display: flex; justify-content: center; gap: 10px; margin-top: 10px;
    }
    .timer-box {
        background: rgba(0,0,0,0.3); border: 2px solid rgba(255,255,255,0.8);
        border-radius: 15px; padding: 10px; width: 80px; text-align: center;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
    }
    .timer-num { font-size: 1.8rem; font-weight: bold; font-family: 'Montserrat', sans-serif; }
    .timer-label { font-size: 0.8rem; }

    /* Buton Stili - Streamlit butonunu özelleştirme */
    div.stButton > button {
        width: 100%;
        background-color: #FFD700;
        color: black;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid white;
        padding: 15px;
        box-shadow: 0 0 20px #FFD700;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #FFF;
        transform: scale(1.05);
    }

    /* Resim */
    img { border-radius: 20px; border: 4px solid #FFF; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
</style>
""", unsafe_allow_html=True)

# --- YARDIMCI FONKSİYONLAR ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

lottie_fireworks = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_tiviyc3p.json")
lottie_moon = load_lottieurl("https://lottie.host/80ec3269-1065-4f40-951c-0e86237227d8/HqE9l5e1vj.json")

# --- HEDEF ZAMAN (5 Aralık 2025 00:00) ---
bugun = datetime.now()
hedef = datetime(2025, 12, 5, 0, 0, 0)
kutlama_zamani = bugun >= hedef

# --- ARAYÜZ ---

# 1. Animasyon (Ay)
if lottie_moon:
    st_lottie(lottie_moon, height=130, key="moon")

# 2. Buton Aksiyonu (En üste koyduk ki her an basılabilsin)
# Butona basılırsa veya saat 00:00 ise kutlama başlasın
if st.button("🎆 Hilal'in Doğum Gününü Kutla 🎆") or kutlama_zamani:
    st.balloons()
    if lottie_fireworks:
        st_lottie(lottie_fireworks, height=300, key="fireworks_btn", quality="low")
    if not kutlama_zamani:
        st.success("Erken kutlama! Sabırsızlanıyoruz! 🎉")

# 3. Ana İçerik
if kutlama_zamani:
    # --- SAAT 00:00 OLDUĞUNDA ---
    st.markdown("<h1>İyi ki Doğdun Hilal! ❤️</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; font-family:Great Vibes; color:#FFD700;'>Sen bizim her şeyimizsin...</h3>", unsafe_allow_html=True)
else:
    # --- GERİ SAYIM ---
    st.markdown("<h1>Hilal'in Doğup Dünyayı<br>Aydınlatmasına Kalan Süre</h1>", unsafe_allow_html=True)

# 4. Fotoğraf
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    try:
        st.image("hilal_aile.jpeg", use_container_width=True)
    except:
        st.error("hilal_aile.jpeg bekleniyor...")

# 5. Sayaç (Sadece zaman gelmediyse göster)
if not kutlama_zamani:
    placeholder = st.empty()
    while True:
        simdi = datetime.now()
        kalan = hedef - simdi
        
        if kalan.total_seconds() <= 0:
            st.rerun() # Zaman dolunca sayfayı yenile
            break
            
        gun = kalan.days
        saniye_toplam = kalan.seconds
        saat = saniye_toplam // 3600
        dakika = (saniye_toplam % 3600) // 60
        saniye = saniye_toplam % 60

        with placeholder.container():
            st.markdown(f"""
            <div class="timer-container">
                <div class="timer-box"><div class="timer-num">{saat}</div><div class="timer-label">SAAT</div></div>
                <div class="timer-box"><div class="timer-num">{dakika}</div><div class="timer-label">DK</div></div>
                <div class="timer-box"><div class="timer-num">{saniye}</div><div class="timer-label">SN</div></div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(1)
