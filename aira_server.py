import threading, os, requests, time, random
from http.server import BaseHTTPRequestHandler, HTTPServer

# Port Fix - Render ku!
def start_web():
    port = int(os.environ.get("PORT", 10000))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Aira Server ON!")
        def log_message(self, *a):
            pass
    HTTPServer(("0.0.0.0", port), H).serve_forever()
threading.Thread(target=start_web, daemon=True).start()
print("Web Port ON!")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
GROUP_ID = "-1003935111481"
CHANNEL_ID = "-1003940504242"

# Books Lines - New Question ku!
BOOK_LINES = [
    "Agara mudhala ezhuthellam aadhi bhagavan mudhatre ulagu",
    "Katrathu kai mann alavu kallathathu ulagalavu",
    "Anbudaiya...",
    "Thirukkural la love pathi enna?",
    "Bharathiyar la courage pathi enna?",
    "Bore adikuthu, enna pannalam?",
    "Tamil la oru story sollu",
    "Sad ah irukku, enna pannalam?",
    "Hi, epdi irukka?",
    "Vanakkam!",
    "Kadhal na enna?",
    "Friendship na enna?",
    "Life la jeyikka enna pannanum?",
    "Thirukkural la oru kural sollu",
    "Bharathiyar paadal sollu",
]

# Auto Question - 10 Sec Loop - Aira Bot Kelvi Kekkum!
def auto_question():
    print("10 Sec Auto Q Start!")
    used = set()
    while True:
        # New Question - Use pannatha line!
        avail = [l for l in BOOK_LINES if l not in used]
        if not avail:
            used.clear()
            avail = BOOK_LINES
        line = random.choice(avail)
        used.add(line)
        q = f"{line} na enna artham? Sollu paapom!"
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            r = requests.post(url, data={"chat_id": GROUP_ID, "text": q}, timeout=10)
            print(f"Q: {q} - {r.status_code}")
        except Exception as e:
            print(f"Q Error - {e}")
        time.sleep(10)

threading.Thread(target=auto_question, daemon=True).start()

# Auto Download - Books Download Pannum!
def auto_download():
    print("Auto Download Start!")
    done = set()
    while True:
        try:
            r = requests.get("https://archive.org/advancedsearch.php?q=language:(tamil)&fl[]=identifier,title&rows=20&output=json", timeout=30)
            books = r.json()['response']['docs']
            for b in books:
                ident = b['identifier']
                if ident in done:
                    continue
                try:
                    meta = requests.get(f"https://archive.org/metadata/{ident}", timeout=30).json()
                    txt = None
                    for f in meta.get('files', []):
                        if f.get('name','').endswith('_djvu.txt'):
                            txt = f['name']
                            break
                    if not txt:
                        continue
                    tr = requests.get(f"https://archive.org/download/{ident}/{txt}", timeout=60)
                    size = len(tr.text.encode('utf-8'))/(1024*1024)
                    if size < 0.05:
                        continue
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                    files = {'document': (f"{ident}.txt", tr.text.encode('utf-8'))}
                    data = {'chat_id': CHANNEL_ID, 'caption': f"📖 {b.get('title','')[:40]}"}
                    pr = requests.post(url, files=files, data=data, timeout=60)
                    if pr.status_code == 200:
                        done.add(ident)
                        print(f"Download OK {ident} - {size:.2f} MB")
                except:
                    continue
                time.sleep(2)
        except:
            print("Download Wait...")
            time.sleep(10)
        time.sleep(60)

threading.Thread(target=auto_download, daemon=True).start()

print("Aira Full Auto Server ON! 10 Sec Q + Auto Download!")
while True:
    time.sleep(60)
