import json
import urllib.parse
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. MASUKKAN TOKEN KAMU DI SINI
TOKEN = '8738189565:AAGv96kfO4mzryarE_jGN_jzvSe3YRNuYQs'

# 2. MASUKKAN LINK GITHUB PAGES KAMU DI SINI (Hasil dari Settings > Pages tadi)
LINK_GITHUB_PAGES = "https://fadianurazizahbs-hub.github.io/nura-manhwa-bot/"

def ambil_data_manhwa_list():
    url = "https://www.zinmanga.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': 'https://www.zinmanga.net/' # Menipu web biar dikira kita buka dari web asli
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='page-item-detail')
        
        daftar = []
        for item in items[:5]:
            try:
                tag_judul = item.find(['h3', 'h4'])
                if not tag_judul: continue
                
                tag_a = tag_judul.find('a')
                if not tag_a: continue
                
                judul = tag_a.text.strip()
                link = tag_a['href']
                
                # --- PERBAIKAN GAMBAR DI SINI ---
                tag_img = item.find('img')
                img_url = ""
                if tag_img:
                    # Cek berbagai kemungkinan tempat link gambar disembunyikan
                    img_url = (tag_img.get('data-src') or 
                               tag_img.get('data-lazy-src') or 
                               tag_img.get('src') or "")
                    
                    # Kalau link-nya cuma diawali //, tambahin https:
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                # -------------------------------

                daftar.append({
                    "judul": judul, 
                    "link": link, 
                    "img": img_url,
                    "genre": "Update"
                })
            except:
                continue
                
        return daftar
    except Exception as e:
        print(f"Error: {e}")
        return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Klik /update untuk melihat daftar manhwa di aplikasi.")

async def kirim_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bentar ya, lagi ngambil data dari ZinManga...")
    
    # Ambil data terbaru
    data_manhwa = ambil_data_manhwa_list()
    
    if not data_manhwa:
        await update.message.reply_text("Maaf, gagal mengambil data. Coba lagi nanti.")
        return

    # Proses data agar bisa dikirim lewat link (Encoding)
    data_json = json.dumps(data_manhwa)
    data_encoded = urllib.parse.quote(data_json)
    
    # Gabungkan Link GitHub Pages dengan data manhwa
    full_app_url = f"https://fadianurazizahbs-hub.github.io/nura-manhwa-bot?data={data_encoded}"
    
    # Buat tombol khusus untuk membuka Mini App
    keyboard = [
        [InlineKeyboardButton("Buka di Aplikasi 📱", web_app=WebAppInfo(url=full_app_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Data sudah siap! Klik tombol di bawah ini untuk melihat update manhwa dalam tampilan aplikasi.",
        reply_markup=reply_markup
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("update", kirim_update))
    
    print("Bot sudah jalan... Coba ketik /update di Telegram!")
    app.run_polling()