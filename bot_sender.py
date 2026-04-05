"""
bot_sender.py – Modul pembantu untuk mengirim pesan Telegram
dan utilitas jadwal.
"""

import requests
from datetime import datetime
import pytz

# ─── Data Jadwal (dipakai bersama app.py dan bot_scheduler.py) ────────────────
JADWAL = [
    {"Waktu": "06:00 – 08:00", "start": "06:00", "end": "08:00", "Sesi": "🌅 Pagi 1",    "Fokus": "Job Hunting & Apply",       "Detail": "Mencari lowongan Data Analyst, menyesuaikan CV, dan mengirimkan lamaran."},
    {"Waktu": "08:00 – 08:30", "start": "08:00", "end": "08:30", "Sesi": "☕ Istirahat",  "Fokus": "Sarapan & Refreshing",       "Detail": "Mandi, sarapan ringan, dan istirahat sejenak."},
    {"Waktu": "08:30 – 10:30", "start": "08:30", "end": "10:30", "Sesi": "📘 Pagi 2",    "Fokus": "TKD (Kemampuan Dasar)",      "Detail": "Latihan soal kognitif harian: Word Classification, Verbal Logic, Number Sequence, Diagram Reasoning."},
    {"Waktu": "10:30 – 12:00", "start": "10:30", "end": "12:00", "Sesi": "🌍 Siang 1",   "Fokus": "Tes Bahasa Inggris",         "Detail": "Latihan Reading comprehension, Structure (Grammar), dan Listening."},
    {"Waktu": "12:00 – 13:30", "start": "12:00", "end": "13:30", "Sesi": "🕌 Istirahat", "Fokus": "ISHOMA",                     "Detail": "Istirahat, Sholat, dan Makan Siang."},
    {"Waktu": "13:30 – 15:30", "start": "13:30", "end": "15:30", "Sesi": "🧠 Siang 2",   "Fokus": "Tes AKHLAK (Core Values)",   "Detail": "Latihan Studi Kasus: Analisis situasi kerja (Amanah, Kompeten, Harmonis, Loyal, Adaptif, Kolaboratif)."},
    {"Waktu": "15:30 – 16:00", "start": "15:30", "end": "16:00", "Sesi": "🙏 Istirahat", "Fokus": "Sholat Ashar & Break",       "Detail": "Peregangan badan, istirahatkan mata dari layar."},
    {"Waktu": "16:00 – 18:00", "start": "16:00", "end": "18:00", "Sesi": "🇮🇩 Sore",     "Fokus": "TWK (Wawasan Kebangsaan)",   "Detail": "Sejarah Pancasila, Implementasi UUD 1945, konsep NKRI, Bhinneka Tunggal Ika, dan latihan soal."},
    {"Waktu": "18:00 – 19:30", "start": "18:00", "end": "19:30", "Sesi": "🌙 Istirahat", "Fokus": "ISHOMA",                     "Detail": "Sholat Maghrib, Isya, Makan Malam, dan rileks."},
    {"Waktu": "19:30 – 21:30", "start": "19:30", "end": "21:30", "Sesi": "💻 Malam 1",   "Fokus": "TKB & Data Analytics",      "Detail": "Latihan query (SQL Server/MySQL), logika Python, visualisasi Power BI, dan baca artikel Digital Mindset."},
    {"Waktu": "21:30 – 22:00", "start": "21:30", "end": "22:00", "Sesi": "✅ Malam 2",   "Fokus": "Review Harian",              "Detail": "Cek progres hari ini, siapkan to-do list dan link lowongan kerja untuk besok pagi."},
]


def send_telegram_message(bot_token: str, chat_id: str, message: str):
    """
    Kirim pesan ke Telegram menggunakan Bot API.

    Returns:
        (True, "OK") jika berhasil
        (False, error_message) jika gagal
    """
    if not bot_token or not chat_id:
        return False, "Bot Token atau Chat ID kosong."

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        if data.get("ok"):
            return True, "OK"
        else:
            err = data.get("description", "Unknown error")
            return False, err
    except requests.exceptions.ConnectionError:
        return False, "Tidak bisa terhubung ke internet. Cek koneksi kamu."
    except requests.exceptions.Timeout:
        return False, "Request timeout (15 detik). Coba lagi."
    except Exception as e:
        return False, str(e)


def get_next_session(now_wib: datetime):
    """
    Cari sesi berikutnya berdasarkan waktu WIB sekarang.
    Kembalikan dict sesi, atau None jika semua sudah selesai.
    """
    now_str = now_wib.strftime("%H:%M")

    for sesi in JADWAL:
        if now_str < sesi["start"]:
            return sesi

    return None  # semua sesi hari ini sudah selesai


def build_reminder_message(sesi: dict, now_wib: datetime) -> str:
    """
    Buat pesan pengingat terformat Markdown untuk Telegram.
    """
    hari_map = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
    }
    hari = hari_map.get(now_wib.strftime("%A"), now_wib.strftime("%A"))

    # Escape karakter khusus MarkdownV2
    def esc(text: str) -> str:
        special = r'\_*[]()~`>#+-=|{}.!'
        return ''.join(f'\\{c}' if c in special else c for c in str(text))

    waktu_esc = esc(sesi['Waktu'])
    sesi_esc  = esc(sesi['Sesi'])
    fokus_esc = esc(sesi['Fokus'])
    detail_esc = esc(sesi['Detail'])
    jam_esc   = esc(now_wib.strftime('%H:%M'))
    hari_esc  = esc(hari)

    pesan = (
        f"🔔 *PENGINGAT JADWAL BELAJAR RBB BUMN*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📅 *{hari_esc}*, pukul `{jam_esc}` WIB\n\n"
        f"➤ *Waktu Sesi:* {waktu_esc}\n"
        f"➤ *Sesi:* {sesi_esc}\n"
        f"➤ *Fokus:* *{fokus_esc}*\n\n"
        f"📝 *Detail:*\n{detail_esc}\n\n"
        f"💪 Semangat\\! Kamu selangkah lebih dekat ke lolos RBB BUMN\\! 🔥"
    )
    return pesan
