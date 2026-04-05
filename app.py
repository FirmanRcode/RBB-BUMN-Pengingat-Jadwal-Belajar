"""
╔══════════════════════════════════════════════════════════════════╗
║        RBB BUMN - Pengingat Jadwal Belajar                      ║
║        Web App: Streamlit | Bot: pyTelegramBotAPI               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import json
import os
from bot_sender import send_telegram_message, get_next_session

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="📚 RBB BUMN – Jadwal Belajar",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* Header card */
    .header-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(168,85,247,0.25));
        border: 1px solid rgba(99,102,241,0.4);
        border-radius: 20px;
        padding: 30px 40px;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
        text-align: center;
    }

    .header-card h1 {
        color: #e0e7ff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 30px rgba(129,140,248,0.5);
    }

    .header-card p {
        color: #a5b4fc;
        font-size: 1rem;
        margin: 8px 0 0 0;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.15));
        border: 1px solid rgba(99,102,241,0.35);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(99,102,241,0.3);
    }

    .metric-label {
        color: #a5b4fc;
        font-size: 0.78rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #e0e7ff;
        font-size: 1.6rem;
        font-weight: 700;
    }

    /* Section titles */
    .section-title {
        color: #c7d2fe;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 24px 0 14px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Status badge */
    .badge-active {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    .badge-break {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    .badge-done {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15,12,41,0.95), rgba(48,43,99,0.95));
        border-right: 1px solid rgba(99,102,241,0.2);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99,102,241,0.5) !important;
    }

    /* Info/warning/success boxes */
    .info-box {
        background: rgba(99,102,241,0.15);
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 14px 18px;
        color: #c7d2fe;
        margin: 12px 0;
        font-size: 0.9rem;
    }

    .success-box {
        background: rgba(16,185,129,0.15);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 14px 18px;
        color: #6ee7b7;
        margin: 12px 0;
        font-size: 0.9rem;
    }

    .warning-box {
        background: rgba(245,158,11,0.15);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 14px 18px;
        color: #fcd34d;
        margin: 12px 0;
        font-size: 0.9rem;
    }

    /* Next session highlight */
    .next-session-card {
        background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(5,150,105,0.15));
        border: 1px solid rgba(16,185,129,0.4);
        border-radius: 16px;
        padding: 20px 24px;
        margin: 16px 0;
    }

    .next-session-title {
        color: #6ee7b7;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    .next-session-name {
        color: #ecfdf5;
        font-size: 1.2rem;
        font-weight: 700;
    }

    .next-session-detail {
        color: #a7f3d0;
        font-size: 0.88rem;
        margin-top: 4px;
    }

    /* Jam WIB display */
    .jam-display {
        font-size: 3rem;
        font-weight: 700;
        color: #e0e7ff;
        text-shadow: 0 0 40px rgba(129,140,248,0.6);
        text-align: center;
        font-family: 'Inter', monospace;
        letter-spacing: 2px;
    }

    .tanggal-display {
        color: #a5b4fc;
        text-align: center;
        font-size: 0.95rem;
        margin-bottom: 10px;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Data Jadwal ──────────────────────────────────────────────────────────────
JADWAL = [
    {"Waktu": "06:00 – 08:00", "Sesi": "🌅 Pagi 1",    "Fokus": "Job Hunting & Apply",       "Detail": "Mencari lowongan Data Analyst, menyesuaikan CV, dan mengirimkan lamaran."},
    {"Waktu": "08:00 – 08:30", "Sesi": "☕ Istirahat",  "Fokus": "Sarapan & Refreshing",       "Detail": "Mandi, sarapan ringan, dan istirahat sejenak."},
    {"Waktu": "08:30 – 10:30", "Sesi": "📘 Pagi 2",    "Fokus": "TKD (Kemampuan Dasar)",      "Detail": "Latihan soal kognitif harian: Word Classification, Verbal Logic, Number Sequence, Diagram Reasoning."},
    {"Waktu": "10:30 – 12:00", "Sesi": "🌍 Siang 1",   "Fokus": "Tes Bahasa Inggris",         "Detail": "Latihan Reading comprehension, Structure (Grammar), dan Listening."},
    {"Waktu": "12:00 – 13:30", "Sesi": "🕌 Istirahat", "Fokus": "ISHOMA",                     "Detail": "Istirahat, Sholat, dan Makan Siang."},
    {"Waktu": "13:30 – 15:30", "Sesi": "🧠 Siang 2",   "Fokus": "Tes AKHLAK (Core Values)",   "Detail": "Latihan Studi Kasus: Analisis situasi kerja (Amanah, Kompeten, Harmonis, Loyal, Adaptif, Kolaboratif)."},
    {"Waktu": "15:30 – 16:00", "Sesi": "🙏 Istirahat", "Fokus": "Sholat Ashar & Break",       "Detail": "Peregangan badan, istirahatkan mata dari layar."},
    {"Waktu": "16:00 – 18:00", "Sesi": "🇮🇩 Sore",     "Fokus": "TWK (Wawasan Kebangsaan)",   "Detail": "Sejarah Pancasila, Implementasi UUD 1945, konsep NKRI, Bhinneka Tunggal Ika, dan latihan soal."},
    {"Waktu": "18:00 – 19:30", "Sesi": "🌙 Istirahat", "Fokus": "ISHOMA",                     "Detail": "Sholat Maghrib, Isya, Makan Malam, dan rileks."},
    {"Waktu": "19:30 – 21:30", "Sesi": "💻 Malam 1",   "Fokus": "TKB & Data Analytics",      "Detail": "Latihan query (SQL Server/MySQL), logika Python, visualisasi Power BI, dan baca artikel Digital Mindset."},
    {"Waktu": "21:30 – 22:00", "Sesi": "✅ Malam 2",   "Fokus": "Review Harian",              "Detail": "Cek progres hari ini, siapkan to-do list dan link lowongan kerja untuk besok pagi."},
]

# ─── Load / Save Config ───────────────────────────────────────────────────────
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"bot_token": "", "chat_id": ""}

def save_config(token, chat_id):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"bot_token": token, "chat_id": chat_id}, f)

def esc(text: str) -> str:
    """Escape semua karakter reserved MarkdownV2 Telegram."""
    special = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in special else c for c in str(text))

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px 0;">
        <div style="font-size: 2.5rem;">📚</div>
        <div style="color: #e0e7ff; font-weight: 700; font-size: 1.1rem; margin-top: 8px;">RBB BUMN</div>
        <div style="color: #a5b4fc; font-size: 0.8rem;">Pengingat Jadwal Belajar</div>
    </div>
    <hr style="border-color: rgba(99,102,241,0.3); margin: 10px 0 20px 0;">
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-title">⚙️ Konfigurasi Telegram</p>', unsafe_allow_html=True)

    cfg = load_config()

    bot_token = st.text_input(
        "🔑 Bot Token",
        value=cfg.get("bot_token", ""),
        type="password",
        placeholder="Contoh: 123456:ABCdef...",
        help="Dapatkan dari @BotFather di Telegram"
    )

    chat_id = st.text_input(
        "💬 Chat ID",
        value=cfg.get("chat_id", ""),
        placeholder="Contoh: 987654321",
        help="Dapatkan dari @userinfobot di Telegram"
    )

    if st.button("💾 Simpan Konfigurasi"):
        save_config(bot_token, chat_id)
        st.success("✅ Konfigurasi tersimpan!")

    st.markdown("---")
    st.markdown('<p class="section-title">📖 Panduan Cepat</p>', unsafe_allow_html=True)
    with st.expander("Cara Mendapatkan Token & Chat ID"):
        st.markdown("""
        **Bot Token:**
        1. Buka Telegram → cari `@BotFather`
        2. Kirim `/newbot`
        3. Ikuti instruksi → salin **Token**

        **Chat ID:**
        1. Cari `@userinfobot` di Telegram
        2. Kirim `/start`
        3. Salin angka **Id** yang muncul
        """)

    st.markdown("---")
    st.markdown("""
    <div style="color: #6b7280; font-size: 0.75rem; text-align: center; padding: 10px 0;">
        Made with ❤️ for RBB BUMN<br>
        Waktu: WIB (UTC+7)
    </div>
    """, unsafe_allow_html=True)


# ─── Main Content ─────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="header-card">
    <h1>📚 Pengingat Jadwal Belajar RBB BUMN</h1>
    <p>Sistem pengingat otomatis berbasis Telegram Bot • Waktu Indonesia Barat (WIB)</p>
</div>
""", unsafe_allow_html=True)

# Jam & Tanggal WIB
WIB = pytz.timezone("Asia/Jakarta")
now_wib = datetime.now(WIB)
hari_map = {
    "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
    "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
}
hari_indo = hari_map.get(now_wib.strftime("%A"), now_wib.strftime("%A"))
bulan_map = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}
tanggal_str = f"{hari_indo}, {now_wib.day} {bulan_map[now_wib.month]} {now_wib.year}"

col_time, col_next = st.columns([1, 1.5])

with col_time:
    st.markdown(f"""
    <div class="metric-card" style="padding: 28px 20px;">
        <div class="metric-label">🕐 Jam Sekarang (WIB)</div>
        <div class="jam-display">{now_wib.strftime('%H:%M:%S')}</div>
        <div class="tanggal-display">{tanggal_str}</div>
    </div>
    """, unsafe_allow_html=True)

with col_next:
    next_sesi = get_next_session(now_wib)
    if next_sesi:
        st.markdown(f"""
        <div class="next-session-card">
            <div class="next-session-title">⏭️ Sesi Berikutnya</div>
            <div class="next-session-name">{next_sesi['Sesi']} – {next_sesi['Fokus']}</div>
            <div class="next-session-detail">⏰ {next_sesi['Waktu']}</div>
            <div class="next-session-detail" style="margin-top:8px; color: #d1fae5;">{next_sesi['Detail'][:80]}...</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="next-session-card" style="background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.15)); border-color: rgba(99,102,241,0.4);">
            <div class="next-session-title" style="color: #a5b4fc;">✨ Status</div>
            <div class="next-session-name" style="color: #e0e7ff;">Semua sesi hari ini selesai!</div>
            <div class="next-session-detail" style="color: #c7d2fe;">Istirahat yang cukup, mulai lagi besok pukul 06:00 💪</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Metrics ──────────────────────────────────────────────────────────────────
total_belajar = 9  # sesi aktif (bukan istirahat)
total_istirahat = 4
total_jam = 16

col1, col2, col3, col4 = st.columns(4)
metrics = [
    ("📋", "Total Sesi", f"{len(JADWAL)} Sesi"),
    ("📖", "Sesi Belajar", f"{total_belajar} Sesi"),
    ("☕", "Istirahat", f"{total_istirahat} Sesi"),
    ("⏱️", "Total Durasi", f"{total_jam} Jam"),
]
for col, (icon, label, value) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.6rem; margin-bottom: 6px;">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabel Jadwal ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">📅 Jadwal Belajar Harian (WIB)</p>', unsafe_allow_html=True)

df = pd.DataFrame(JADWAL)

# Beri warna tipe sesi
def color_sesi(row):
    if "Istirahat" in row["Sesi"]:
        return ["background-color: rgba(245,158,11,0.08)"] * len(row)
    else:
        return ["background-color: rgba(99,102,241,0.06)"] * len(row)

styled_df = df.style.apply(color_sesi, axis=1)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=420,
    hide_index=True,
    column_config={
        "Waktu":  st.column_config.TextColumn("⏰ Waktu (WIB)", width=140),
        "Sesi":   st.column_config.TextColumn("📌 Sesi", width=130),
        "Fokus":  st.column_config.TextColumn("🎯 Fokus Materi", width=200),
        "Detail": st.column_config.TextColumn("📝 Detail Kegiatan & Latihan", width=450),
    }
)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Test Notifikasi ──────────────────────────────────────────────────────────
st.markdown('<p class="section-title">🔔 Uji Coba Notifikasi Telegram</p>', unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("📨 Test Kirim Notif Sekarang", key="test_now"):
        cfg_now = load_config()
        if not cfg_now["bot_token"] or not cfg_now["chat_id"]:
            st.markdown("""
            <div class="warning-box">
                ⚠️ <strong>Konfigurasi belum lengkap!</strong><br>
                Isi Bot Token dan Chat ID di sidebar kiri terlebih dahulu.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("📤 Mengirim pesan ke Telegram..."):
                pesan = (
                    f"🔔 *TEST NOTIFIKASI \\– RBB BUMN*\n\n"
                    f"📚 *Aplikasi Pengingat Jadwal Belajar*\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🕐 Waktu: `{esc(now_wib.strftime('%H:%M'))} WIB`\n"
                    f"📅 Tanggal: {esc(tanggal_str)}\n\n"
                    f"✅ Bot kamu berhasil terhubung\\!\n"
                    f"Notifikasi otomatis akan dikirim sesuai jadwal harian\\.\n\n"
                    f"💪 *Semangat belajar untuk RBB BUMN\\!*"
                )
                ok, msg = send_telegram_message(cfg_now["bot_token"], cfg_now["chat_id"], pesan)
                if ok:
                    st.markdown(f"""
                    <div class="success-box">
                        ✅ <strong>Berhasil!</strong> Pesan terkirim ke Telegram kamu. Cek HP sekarang!
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="warning-box">
                        ❌ <strong>Gagal mengirim:</strong> {msg}<br>
                        Pastikan Bot Token dan Chat ID sudah benar.
                    </div>
                    """, unsafe_allow_html=True)

with col_btn2:
    if st.button("📋 Test Kirim Jadwal Lengkap", key="test_jadwal"):
        cfg_now = load_config()
        if not cfg_now["bot_token"] or not cfg_now["chat_id"]:
            st.markdown("""
            <div class="warning-box">
                ⚠️ Isi Bot Token dan Chat ID di sidebar terlebih dahulu.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("📤 Mengirim jadwal ke Telegram..."):
                lines = ["📅 *JADWAL BELAJAR HARIAN \\– RBB BUMN*\n━━━━━━━━━━━━━━━━━━━━\n"]
                for item in JADWAL:
                    emoji = "☕" if "Istirahat" in item["Sesi"] else "📖"
                    waktu  = esc(item['Waktu'])
                    sesi   = esc(item['Sesi'])
                    fokus  = esc(item['Fokus'])
                    lines.append(f"{emoji} *{waktu}*\n{sesi} \\– {fokus}\n")
                lines.append("\n💪 Semangat\\! Kamu bisa\\! 🔥")
                pesan = "\n".join(lines)
                ok, msg = send_telegram_message(cfg_now["bot_token"], cfg_now["chat_id"], pesan)
                if ok:
                    st.markdown('<div class="success-box">✅ <strong>Jadwal lengkap terkirim!</strong> Cek Telegram kamu.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="warning-box">❌ <strong>Gagal:</strong> {msg}</div>', unsafe_allow_html=True)

with col_btn3:
    if st.button("🔄 Refresh Halaman", key="refresh"):
        st.rerun()

# ─── Status Bot ───────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="section-title">📡 Status Sistem</p>', unsafe_allow_html=True)

cfg_status = load_config()
col_s1, col_s2 = st.columns(2)

with col_s1:
    if cfg_status["bot_token"]:
        token_preview = cfg_status["bot_token"][:8] + "..." + cfg_status["bot_token"][-4:]
        st.markdown(f"""
        <div class="metric-card" style="text-align:left;">
            <div class="metric-label">🔑 Status Bot Token</div>
            <span class="badge-active">✅ Tersimpan</span>
            <div style="color: #9ca3af; font-size: 0.8rem; margin-top: 8px;">{token_preview}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card" style="text-align:left;">
            <div class="metric-label">🔑 Status Bot Token</div>
            <span class="badge-break">⚠️ Belum diisi</span>
        </div>
        """, unsafe_allow_html=True)

with col_s2:
    if cfg_status["chat_id"]:
        st.markdown(f"""
        <div class="metric-card" style="text-align:left;">
            <div class="metric-label">💬 Status Chat ID</div>
            <span class="badge-active">✅ Tersimpan</span>
            <div style="color: #9ca3af; font-size: 0.8rem; margin-top: 8px;">ID: {cfg_status['chat_id']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card" style="text-align:left;">
            <div class="metric-label">💬 Status Chat ID</div>
            <span class="badge-break">⚠️ Belum diisi</span>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color: #4b5563; font-size: 0.8rem; padding: 20px 0; border-top: 1px solid rgba(99,102,241,0.15);">
    📚 RBB BUMN Jadwal Belajar v1.0 &nbsp;|&nbsp; Dibuat dengan ❤️ menggunakan Streamlit + Telegram Bot
    <br>Waktu Zona: WIB (UTC+7) &nbsp;|&nbsp; 100% Gratis
</div>
""", unsafe_allow_html=True)
