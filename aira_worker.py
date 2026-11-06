# AIRAH1 - WORKER 2 BOTS - New Channel + 2 Bots = Aira Data
# File: aira_worker.py
import os, time, threading, requests

# 2 Bot Token - Render Env Var la Podu!
BOT1_TOKEN = os.getenv("BOT1_TOKEN","")  # Image Worker
BOT2_TOKEN = os.getenv("BOT2_TOKEN","")  # Knowledge Worker
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
GITHUB_USER = "bigstar7639-krish"
# New Channel ID - H1 Aira Data Channel ID
DATA_CHANNEL = os.getenv("DATA_CHANNEL","")  # -100... nu Podu!

def send_to_channel(text, bot_token):
    try:
        r = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": DATA_CHANNEL, "text": text}, timeout=15)
        print(f"Worker Send: {r.status_code} to Data Channel", flush=True)
    except Exception as e:
        print(f"Worker Send Error {e}", flush=True)

def save_github(filename, content):
    if not GITHUB_TOKEN: return
    try:
        import base64
        url = f"https://api.github.com/repos/{GITHUB_USER}/H1-Data-3/contents/data/{filename}"
        r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        sha = r.json().get("sha") if r.status_code==200 else None
        old = ""
        if r.status_code==200:
            try: old = base64.b64decode(r.json().get("content","")).decode(errors="ignore")
            except: old = ""
        new = (old + "\n" + content) if old else content
        b64 = base64.b64encode(new.encode()).decode()
        payload = {"message": f"Worker Save {filename}", "content": b64}
        if sha: payload["sha"] = sha
        rr = requests.put(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload, timeout=15)
        print(f"Worker 【entity-GitHub¦canonical_name=GitHub】 Save: {rr.status_code} - {filename}", flush=True)
    except Exception as e:
        print(f"Worker Save Error {e}", flush=True)

# BOT 1 - IMAGE WORKER - 100 Image Per Category!
def bot1_image_worker():
    cats = ["Tamil","Love","God","Nature","Cat","Food","Cricket","Space","Story","Health"]
    idx = 0
    while True:
        try:
            cat = cats[idx % len(cats)]; idx += 1
            print(f"Bot1 - Image Worker - Category: {cat} - 100 Image...", flush=True)
            r = requests.get("https://commons.wikimedia.org/w/api.php", params={
                "action":"query","format":"json","generator":"search",
                "gsrsearch":cat,"gsrnamespace":6,"gsrlimit":20,
                "prop":"imageinfo","iiprop":"url"
            }, timeout=20)
            count = 0
            for page in r.json().get("query",{}).get("pages",{}).values():
                url = page.get("imageinfo",[{}])[0].get("url","")
                if url:
                    count += 1
                    send_to_channel(f"Auto Image - {cat} - {count}/100 📸\n{url}", BOT1_TOKEN)
                    save_github(f"images-{cat}-2026-11-06.txt", f"{cat} - {url}")
                    time.sleep(2)
            print(f"Bot1 Done - {cat} - {count} Image", flush=True)
            time.sleep(3600) # 1 Mani Wait - Adutha Category!
        except Exception as e:
            print(f"Bot1 Error {e}", flush=True); time.sleep(60)

# BOT 2 - KNOWLEDGE WORKER - Knowledge + Books!
def bot2_knowledge_worker():
    topics = ["Tamil Nadu","India","Space","Science","Love","Health","Business","History","Cricket","AI"]
    idx = 0
    while True:
        try:
            topic = topics[idx % len(topics)]; idx += 1
            print(f"Bot2 - Knowledge Worker - Topic: {topic}", flush=True)
            # 【entity-Wikipedia¦canonical_name=Wikipedia】 Knowledge!
            r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ','_')}", timeout=10)
            if r.status_code==200:
                ex = r.json().get("extract","")[:500]
                if ex:
                    send_to_channel(f"Auto Knowledge - {topic} 🧠\n{ex}", BOT2_TOKEN)
                    save_github(f"knowledge-worker-2026-11-06.txt", f"{topic} - {ex}")
            # OpenLibrary Books!
            r2 = requests.get("https://openlibrary.org/search.json", params={"q":topic,"limit":3}, timeout=10)
            for b in r2.json().get("docs",[])[:2]:
                title = b.get("title","")
                if title:
                    send_to_channel(f"Auto Book - {topic} - {title} 📚", BOT2_TOKEN)
                    save_github(f"books-worker-2026-11-06.txt", f"{topic} - {title}")
            time.sleep(1800) # 30 Min Wait!
        except Exception as e:
            print(f"Bot2 Error {e}", flush=True); time.sleep(60)

if __name__ == "__main__":
    print("AIRAH1 WORKER 2 BOTS - Started - Data Channel!", flush=True)
    threading.Thread(target=bot1_image_worker, daemon=True).start()
    threading.Thread(target=bot2_knowledge_worker, daemon=True).start()
    # Web Server - Render ku!
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        class H(BaseHTTPRequestHandler):
            def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"AIRAH1 Worker 2 Bots ON")
            def log_message(self,*a): pass
        HTTPServer(("0.0.0.0", int(os.getenv("PORT","10000"))), H).serve_forever()
    except:
        while True: time.sleep(60)
