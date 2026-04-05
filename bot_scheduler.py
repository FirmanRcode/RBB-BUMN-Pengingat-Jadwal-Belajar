"""
bot_scheduler.py – Jalankan file ini secara TERPISAH dari Streamlit.
Ini adalah engine bot yang akan mengirim notifikasi Telegram otomatis
sesuai jadwal WIB menggunakan APScheduler.

Cara jalankan:
    python bot_scheduler.py

Biarkan terminal ini tetap terbuka. Bot akan berjalan di background.
"""

import json
import os
import sys
import time
import logging
from datetime import datetime

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from bot_sender import JADWAL, send_telegram_message, build_reminder_message

# ─── Logging Setup ────────────────────────────────────────────────────────────
log_handlers = [logging.StreamHandler(sys.stdout)]
try:
    log_handlers.append(logging.FileHandler("bot_log.txt", encoding="utf-8"))
except Exception:
    pass  # Di Render filesystem mungkin read-only, skip file log

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=log_handlers,
)
log = logging.getLogger(__name__)

# ─── Timezone ─────────────────────────────────────────────────────────────────
WIB = pytz.timezone("Asia/Jakarta")

# ─── Load Config ──────────────────────────────────────────────────────────────
# Prioritas: Environment Variables (Render) → config.json (lokal)
CONFIG_FILE = "config.json"

def load_config():
    # 1️⃣ Coba dari Environment Variables (dipakai saat deploy ke Render)
    bot_token = os.environ.get("BOT_TOKEN", "")
    chat_id   = os.environ.get("CHAT_ID", "")

    if bot_token and chat_id:
        log.info("✅ Konfigurasi dimuat dari Environment Variables (Render mode).")
        return {"bot_token": bot_token, "chat_id": chat_id}

    # 2️⃣ Fallback ke config.json (dipakai saat develop lokal)
    if not os.path.exists(CONFIG_FILE):
        log.error("Tidak ada config.json dan env var BOT_TOKEN/CHAT_ID belum diset!")
        log.error("Lokal: Buka Streamlit → sidebar → simpan konfigurasi.")
        log.error("Render: Set env var BOT_TOKEN dan CHAT_ID di dashboard Render.")
        sys.exit(1)

    with open(CONFIG_FILE, "r") as f:
        cfg = json.load(f)

    if not cfg.get("bot_token") or not cfg.get("chat_id"):
        log.error("Bot Token atau Chat ID masih kosong di config.json!")
        sys.exit(1)

    log.info("✅ Konfigurasi dimuat dari config.json (local mode).")
    return cfg


# ─── Job: Kirim Notif ─────────────────────────────────────────────────────────
def kirim_notif(sesi: dict):
    """Callback APScheduler: kirim notifikasi untuk satu sesi."""
    cfg = load_config()
    now = datetime.now(WIB)
    log.info(f"⏰ Memicu notif sesi: {sesi['Sesi']} – {sesi['Fokus']}")

    pesan = build_reminder_message(sesi, now)
    ok, msg = send_telegram_message(cfg["bot_token"], cfg["chat_id"], pesan)

    if ok:
        log.info(f"✅ Notif berhasil dikirim: {sesi['Sesi']}")
    else:
        log.error(f"❌ Gagal kirim notif [{sesi['Sesi']}]: {msg}")


# ─── Setup Scheduler ──────────────────────────────────────────────────────────
def setup_scheduler() -> BlockingScheduler:
    """
    Daftarkan semua jadwal harian ke APScheduler.
    Setiap notif dikirim 5 menit SEBELUM sesi dimulai agar kamu siap.
    """
    scheduler = BlockingScheduler(timezone=WIB)

    for sesi in JADWAL:
        jam_str, menit_str = sesi["start"].split(":")
        jam   = int(jam_str)
        menit = int(menit_str)

        # Kirim 5 menit sebelum mulai
        menit_trigger = menit - 5
        jam_trigger   = jam
        if menit_trigger < 0:
            menit_trigger += 60
            jam_trigger = (jam - 1) % 24

        # Buat closure yang aman untuk loop
        def make_job(s):
            return lambda: kirim_notif(s)

        scheduler.add_job(
            func=make_job(sesi),
            trigger=CronTrigger(hour=jam_trigger, minute=menit_trigger, timezone=WIB),
            id=f"notif_{sesi['start'].replace(':', '')}",
            name=f"{sesi['Sesi']} – {sesi['Fokus']}",
            replace_existing=True,
            misfire_grace_time=120,  # toleransi 2 menit keterlambatan
        )

        log.info(
            f"📌 Terjadwal: {sesi['Sesi']:20s} | "
            f"Trigger pukul {jam_trigger:02d}:{menit_trigger:02d} WIB "
            f"(5 mnt sebelum {sesi['start']})"
        )

    return scheduler


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  📚 RBB BUMN – Bot Pengingat Jadwal Belajar")
    print("  Engine: APScheduler | Zona Waktu: WIB (UTC+7)")
    print("=" * 60 + "\n")

    cfg = load_config()
    log.info(f"✅ Konfigurasi dimuat. Chat ID: {cfg['chat_id']}")

    # Kirim pesan startup
    now = datetime.now(WIB)
    startup_msg = (
        "🤖 *Bot Pengingat RBB BUMN Aktif\\!*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "✅ Bot berhasil dijalankan dan siap mengirim\n"
        "notifikasi pengingat sesuai jadwal belajar harian\\.\n\n"
        f"🕐 Waktu aktif: `{now.strftime('%H:%M')} WIB`\n\n"
        "📅 Notif akan dikirim *5 menit sebelum* setiap sesi\\.\n\n"
        "💪 Semangat belajar untuk lolos RBB BUMN\\! 🔥"
    )
    ok, msg = send_telegram_message(cfg["bot_token"], cfg["chat_id"], startup_msg)
    if ok:
        log.info("✅ Pesan startup terkirim ke Telegram.")
    else:
        log.warning(f"⚠️  Pesan startup gagal: {msg}")

    # Mulai scheduler
    scheduler = setup_scheduler()
    total_jobs = len(scheduler.get_jobs())
    log.info(f"\n🚀 Scheduler aktif dengan {total_jobs} jadwal terjadwal.")
    log.info("⏳ Bot berjalan... (Ctrl+C untuk berhenti)\n")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("\n🛑 Bot dihentikan oleh pengguna.")
        scheduler.shutdown()
