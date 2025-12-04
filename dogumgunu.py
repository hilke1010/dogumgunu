import streamlit as st
from datetime import datetime
import time
from streamlit_lottie import st_lottie
import requests
import pytz # Saat dilimi için

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Mutlu Yıllar Hilal!",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS: TEK EKRAN VE HIZLI RENKLER ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@600&display=swap');

    /* Sayfa kenar boşluklarını sıfırla (Tek ekrana sığsın diye) */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    /* HIZLI AKAN ARKA PLAN (3 Saniye) */
    .stApp {
        background: linear-gradient(-45deg, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #9400D3);
        background-size: 400% 400%;
        animation: gradientBG 3s ease infinite;
        color: white;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Başlık */
    h1 {
        font-family: 'Playfair Display', serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        text-align: center;
        font-size: 1.5rem !important; /* Mobilde yer kaplamasın diye küçülttük */
        margin-bottom: 5px;
        margin-top: 0px;
        line-height: 1.2;
    }

    /* Sayaç Kutuları */
    .timer-container {
        display: flex; justify-content: center; gap: 5px; margin-bottom: 10px;
    }
    .timer-box {
        background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.6);
        border-radius: 10px; padding: 5px; width: 65px; text-align: center;
    }
    .timer-num { font-size: 1.4rem; font-weight: bold; font-family: 'Montserrat', sans-serif; }
    .timer-label { font-size: 0.6rem; }

    /* Buton */
    div.stButton > button {
        width: 100%;
        background-color: #FFD700; color: black; font-weight: bold;
        border-radius: 20px; border: 2px solid white; padding: 8px;
        box-shadow: 0 0 10px #FFD700; margin-bottom: 10px;
    }
    div.stButton > button:hover { background-color: white; transform: scale(1.02); }

    /* Resim (Sığdırma ayarı) */
    div[data-testid="stImage"] img {
        max-height: 300px; /* Ekrana sığması için yükseklik limiti */
        object-fit: contain;
        border-radius: 15px; border: 3px solid white;
        margin-top: 0px;
    }
</style>
""", unsafe_allow_html=True)

# --- ANİMASYON ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

lottie_fireworks = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_tiviyc3p.json")
lottie_moon = load_lottieurl("https://lottie.host/80ec3269-1065-4f40-951c-0e86237227d8/HqE9l5e1vj.json")

# --- TÜRKİYE SAATİ AYARI (Europe/Istanbul) ---
try:
    tr_tz = pytz.timezone('Europe/Istanbul')
except:
    # Eğer pytz yüklenemezse varsayılan sistem saatini kullan (Yedek plan)
    tr_tz = None

def get_turkey_time():
    if tr_tz:
        return datetime.now(tr_tz)
    return datetime.now()

# HEDEF: 5 Aralık 2025, Saat 00:00:00 (Türkiye Saatiyle)
if tr_tz:
    hedef = tr_tz.localize(datetime(2025, 12, 5, 0, 0, 0))
else:
    hedef = datetime(2025, 12, 5, 0, 0, 0)

simdi = get_turkey_time()
kutlama_zamani = simdi >= hedef

# --- ARAYÜZ ---

# 1. Animasyon (Ay) - En Tepeye Küçük
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    if lottie_moon:
        st_lottie(lottie_moon, height=80, key="moon")

# 2. Başlık
if not kutlama_zamani:
    st.markdown("<h1>Hilal'in Doğup Dünyayı<br>Aydınlatmasına Kalan Süre</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1>İyi ki Doğdun Hilal! ❤️</h1>", unsafe_allow_html=True)

# 3. Sayaç (Placeholder)
timer_placeholder = st.empty()

# 4. Buton (Kutlama)
if st.button("🎆 KUTLA 🎆") or kutlama_zamani:
    st.balloons()
    if lottie_fireworks:
        # Havai fişekleri arka planda değil, bir kolon içinde gösterip kaybolmasını sağlayalım
        st_lottie(lottie_fireworks, height=150, key="fw_btn", quality="low")

# 5. Fotoğraf (Alt Kısım)
col1, col2, col3 = st.columns([1, 15, 1])
with col2:
    try:
        st.image("hilal_aile.jpeg", use_container_width=True)
    except:
        st.error("Resim yüklenemedi.")

# --- GERİ SAYIM DÖNGÜSÜ ---
if not kutlama_zamani:
    while True:
        simdi = get_turkey_time()
        kalan = hedef - simdi
        
        if kalan.total_seconds() <= 0:
            st.rerun()
            break
            
        saniye_toplam = int(kalan.total_seconds())
        saat = saniye_toplam // 3600
        dakika = (saniye_toplam % 3600) // 60
        saniye = saniye_toplam % 60

        with timer_placeholder.container():
            st.markdown(f"""
            <div class="timer-container">
                <div class="timer-box"><div class="timer-num">{saat}</div><div class="timer-label">SAAT</div></div>
                <div class="timer-box"><div class="timer-num">{dakika}</div><div class="timer-label">DK</div></div>
                <div class="timer-box"><div class="timer-num">{saniye}</div><div class="timer-label">SN</div></div>
            </div>
            """, unsafe_allow_html=True)
        
        time.sleep(1)
else:
    # Kutlama zamanı geldiyse sayaç yerine yazı yazsın
    with timer_placeholder.container():
        st.markdown("<h3 style='text-align:center; color:#FFD700;'>Zaman Geldi! 🎉</h3>", unsafe_allow_html=True)
