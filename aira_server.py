import threading, os, requests, time
from http.server import BaseHTTPRequestHandler, HTTPServer

# Port Fix - Render ku Port venum!
def start_web():
    port = int(os.environ.get("PORT", 10000))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Aira Server ON! Books Downloading...")
        def log_message(self, *a):
            pass
    HTTPServer(("0.0.0.0", port), H).serve_forever()
threading.Thread(target=start_web, daemon=True).start()
print("Web Port ON!")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "-1003940504242")
print("Render Server Start!")
done = set()
while True:
    try:
        r = requests.get("https://archive.org/advancedsearch.php?q=language:(tamil)&fl[]=identifier,title&rows=50&output=json", timeout=30)
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
                    print(f"OK {ident} - {size:.2f} MB")
            except:
                continue
            time.sleep(2)
    except:
        print("Wait 10 sec...")
        time.sleep(10)
