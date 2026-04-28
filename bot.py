import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# GANTI DENGAN TOKEN KAMU
TOKEN = '8738189565:AAGv96kfO4mzryarE_jGN_jzvSe3YRNuYQs'

def ambil_data_manhwa():
    url = "https://www.zinmanga.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
      
        # Sesuai dengan inspect element yang kamu temukan
        items = soup.find_all('div', class_='slider__item')
        
        hasil = []
        for item in items[:5]:
            tag_h4 = item.find('h4')
            if tag_h4:
                tag_a = tag_h4.find('a')
                judul = tag_a.text.strip()
                
                # BAGIAN PENTING: Menggabungkan link agar bisa diklik
                link_pendek = tag_a['href']
                if link_pendek.startswith('/'):
                    link_lengkap = "https://www.zinmanga.net" + link_pendek
                else:
                    link_lengkap = link_pendek
                
                # Format pesan pake HTML (Bold judul + Link biru)
                item_teks = f"📖 <b>{judul}</b>\n🔗 <a href='{link_lengkap}'>Klik untuk Baca</a>"
                hasil.append(item_teks)
        
        if not hasil:
            return "Waduh, belum ada update manhwa nih."
            
        return "\n\n".join(hasil)
        
    except Exception as e:
        return f"Error pas ambil data: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Ketik /update buat liat manhwa terbaru.")

async def kirim_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bentar ya, lagi ngintip ZinManga...")
    pesan_manhwa = ambil_data_manhwa()
    
    # parse_mode='HTML' wajib ada biar linknya bisa diklik
    await update.message.reply_text(pesan_manhwa, parse_mode='HTML')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("update", kirim_update))
    
    print("Bot sudah jalan... Coba chat bot kamu di Telegram!")
    app.run_polling()