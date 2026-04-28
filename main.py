import requests
from bs4 import BeautifulSoup

# Gunakan URL ZinManga karena HTML tadi dari sana
URL = "https://www.zinmanga.net/" 

def cari_manhwa():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    print(f"Sedang mengakses {URL}...")
    response = requests.get(URL, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # KITA PAKAI CLASS YANG KAMU TEMUKAN TADI!
        items = soup.find_all('div', class_='slider__item')
        
        print(f"Berhasil menemukan {len(items)} manhwa!\n")
        
        for item in items:
            # Ambil Judul (ada di dalam h4 > a)
            tag_h4 = item.find('h4')
            if tag_h4:
                tag_a = tag_h4.find('a')
                judul = tag_a.text.strip()
                link = tag_a['href']
                
                # Ambil Chapter terbaru (opsional)
                chapter_tag = item.find('span', class_='chapter')
                chapter = chapter_tag.text.strip() if chapter_tag else "N/A"
                
                print(f"📖 Judul  : {judul}")
                print(f"🔗 Link   : {link}")
                print(f"🆙 Update : {chapter}")
                print("-" * 30)
    else:
        print(f"Waduh, gagal masuk. Status code: {response.status_code}")

if __name__ == "__main__":
    cari_manhwa()