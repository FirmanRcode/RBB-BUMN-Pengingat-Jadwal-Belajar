# 📚 RBB BUMN – Pengingat Jadwal Belajar

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)](https://streamlit.io)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-26A5E4?logo=telegram)](https://core.telegram.org/bots)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> Aplikasi pengingat jadwal belajar harian berbasis **Streamlit Web UI** + **Telegram Bot** otomatis, dirancang khusus untuk persiapan **Rekrutmen Bersama BUMN (RBB)**.  
> **100% GRATIS** | Zona Waktu: **WIB (UTC+7)**

---

## ✨ Fitur Utama

| Fitur | Keterangan |
|-------|-----------|
| 🖥️ **Web UI Streamlit** | Tampilan jadwal interaktif dengan jam WIB real-time |
| 🔔 **Bot Telegram Otomatis** | Notifikasi dikirim **5 menit sebelum** setiap sesi |
| 📋 **11 Sesi Harian** | TKD, TWK, TKB, AKHLAK, Bahasa Inggris, Data Analytics |
| 📨 **Test Notif Instan** | Tombol uji coba kirim pesan langsung ke Telegram kamu |
| 💾 **Konfigurasi Aman** | Token & Chat ID disimpan lokal, tidak ter-upload ke GitHub |

---

## 📅 Jadwal Belajar

| Waktu (WIB) | Sesi | Fokus |
|-------------|------|-------|
| 06:00 – 08:00 | 🌅 Pagi 1 | Job Hunting & Apply |
| 08:00 – 08:30 | ☕ Istirahat | Sarapan & Refreshing |
| 08:30 – 10:30 | 📘 Pagi 2 | TKD (Kemampuan Dasar) |
| 10:30 – 12:00 | 🌍 Siang 1 | Tes Bahasa Inggris |
| 12:00 – 13:30 | 🕌 Istirahat | ISHOMA |
| 13:30 – 15:30 | 🧠 Siang 2 | Tes AKHLAK (Core Values) |
| 15:30 – 16:00 | 🙏 Istirahat | Sholat Ashar & Break |
| 16:00 – 18:00 | 🇮🇩 Sore | TWK (Wawasan Kebangsaan) |
| 18:00 – 19:30 | 🌙 Istirahat | ISHOMA |
| 19:30 – 21:30 | 💻 Malam 1 | TKB & Data Analytics |
| 21:30 – 22:00 | ✅ Malam 2 | Review Harian |

---

## 🚀 Cara Menjalankan

### 1. Clone Repositori

```bash
git clone https://github.com/USERNAME/rbb-bumn-jadwal-belajar.git
cd rbb-bumn-jadwal-belajar
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Konfigurasi Telegram

```bash
# Salin file contoh
cp config.example.json config.json
```

Lalu edit `config.json` dengan token & chat ID kamu:
```json
{
  "bot_token": "TOKEN_DARI_BOTFATHER",
  "chat_id": "CHAT_ID_KAMU"
}
```

> **Cara dapat Token:** Buka Telegram → cari `@BotFather` → `/newbot`  
> **Cara dapat Chat ID:** Buka Telegram → cari `@userinfobot` → `/start`

### 4. Jalankan Web App

```bash
# Terminal 1 – Web UI
python -m streamlit run app.py
```

Buka browser: [http://localhost:8501](http://localhost:8501)

Atau isi konfigurasi langsung dari sidebar Streamlit, lalu klik **💾 Simpan Konfigurasi**.

### 5. Jalankan Bot Scheduler (Terminal Terpisah)

```bash
# Terminal 2 – Bot Otomatis
python bot_scheduler.py
```

Bot akan aktif dan mengirim notifikasi sesuai jadwal harian secara otomatis! 🤖

---

## 🗂️ Struktur Proyek

```
rbb-bumn-jadwal-belajar/
├── app.py                  # Web UI Streamlit
├── bot_sender.py           # Modul pengiriman pesan Telegram
├── bot_scheduler.py        # Engine penjadwalan otomatis (APScheduler)
├── requirements.txt        # Dependencies Python
├── config.example.json     # Template konfigurasi (AMAN di-upload)
├── .gitignore              # config.json dikecualikan dari Git
└── README.md               # Dokumentasi ini
```

> ⚠️ `config.json` (berisi Bot Token & Chat ID) **TIDAK** ter-upload ke GitHub karena sudah masuk `.gitignore`.

---

## 🔧 Troubleshooting

| Error | Solusi |
|-------|--------|
| `Unauthorized` | Token Bot salah → salin ulang dari BotFather |
| `Chat not found` | Chat ID salah → cek ulang dari @userinfobot. Pastikan sudah `/start` bot kamu |
| `can't parse entities` | Karakter khusus tidak di-escape → sudah diatasi di versi terbaru |
| `ModuleNotFoundError` | Jalankan `pip install -r requirements.txt` |
| Bot tidak kirim notif | Pastikan terminal `bot_scheduler.py` masih terbuka |

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io)** – Web UI framework Python
- **[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)** – Telegram Bot API wrapper
- **[APScheduler](https://apscheduler.readthedocs.io)** – Background job scheduler
- **[pytz](https://pythonhosted.org/pytz/)** – Timezone handling (WIB/Asia/Jakarta)
- **[pandas](https://pandas.pydata.org)** – Data manipulation untuk tabel jadwal

---

## 📄 Lisensi

MIT License © 2026 – Restu Firmansyah

---

> 💪 **Semangat persiapan RBB BUMN-nya! Kamu pasti bisa!** 🔥
