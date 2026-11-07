# AIRAH1 - FINAL - Worker - 100/100 + No Watermark + Japan + China + India + Infinite Source + Infinite Repo + do_HEAD
# File: aira_worker.py - Start: python3 -u aira_worker.py
# NO Pollinations! NO Google / Instagram / Facebook scraping! Only FREE legal sources - No Watermark!
import os, time, threading, requests, base64, random, html, re
from datetime import datetime

BOT1_TOKEN = os.getenv("BOT1_TOKEN","")
BOT2_TOKEN = os.getenv("BOT2_TOKEN","")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
GITHUB_USER = "bigstar7639-krish"

def fix_id(v, default):
    v = (v or default).strip()
    if not v: return default
    if v.startswith("-"): return v
    if v.startswith("100"): return "-" + v
    return "-100" + v

DATA_CHANNEL = fix_id(os.getenv("DATA_CHANNEL",""), "-1004366479419")
print(f"Worker Start - Bot1 OK? {bool(BOT1_TOKEN)} Bot2 OK? {bool(BOT2_TOKEN)} Channel: {DATA_CHANNEL}", flush=True)

CURRENT_REPO = ["H1-Data-3"]; REPO_COUNT = [0]; MAX_PER_REPO = 1000
SAVE_LOCK = threading.Lock()
def get_repo_num(r):
    try: return int(r.split("-")[-1])
    except: return 3
def ensure_repo(repo):
    try:
        r = requests.get(f"https://api.github.com/repos/{GITHUB_USER}/{repo}", headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "AIRAH1"}, timeout=10)
        if r.status_code == 200: return True
        cr = requests.post("https://api.github.com/user/repos", headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "AIRAH1"}, json={"name": repo, "private": False, "auto_init": True, "description": "AIRAH1 Infinite"}, timeout=15)
        print(f"Infinite Repo Create: {cr.status_code} - {repo}", flush=True)
        return cr.status_code in (200,201,422)
    except Exception as e: print(f"Repo Error {e}", flush=True); return False
def next_repo():
    n = get_repo_num(CURRENT_REPO[0])+1; CURRENT_REPO[0]=f"H1-Data-{n}"; REPO_COUNT[0]=0
    print(f"Infinite Repo Switch -> {CURRENT_REPO[0]}", flush=True); ensure_repo(CURRENT_REPO[0]); return CURRENT_REPO[0]
def save_github(filename, content):
    if REPO_COUNT[0] >= MAX_PER_REPO: next_repo()
    if not GITHUB_TOKEN: return False
    with SAVE_LOCK:
        for attempt in range(3):
            repo = CURRENT_REPO[0]; ensure_repo(repo)
            try:
                url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/data/{filename}"
                r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
                sha = r.json().get("sha") if r.status_code==200 else None
                old = ""
                if r.status_code==200:
                    try: old = base64.b64decode(r.json().get("content","")).decode(errors="ignore")
                    except: old = ""
                new = (old + "\n" + content) if old else content
                lines = new.split("\n")
                if len(lines) > 2000: new = "\n".join(lines[-2000:])
                b64 = base64.b64encode(new.encode()).decode()
                payload = {"message": f"Worker Save {filename}", "content": b64}
                if sha: payload["sha"] = sha
                rr = requests.put(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload, timeout=15)
                if rr.status_code in (200,201):
                    REPO_COUNT[0]+=1
                    print(f"Worker GitHub Save OK - {repo}/{filename} - Repo {REPO_COUNT[0]}/{MAX_PER_REPO}", flush=True)
                    return True
                if rr.status_code in (409,422):
                    print(f"Worker Save Retry {rr.status_code} - Try {attempt+1}/3", flush=True); time.sleep(1); continue
                if rr.status_code in (403,413): next_repo(); continue
                time.sleep(1); continue
            except Exception as e: print(f"Worker Save Error {e}", flush=True); time.sleep(1); continue
        return False

# --- 100+ CATEGORIES - Tamil + Japan + China + India + Global ---
BASE_CATS = ["Tamil","Love","God","Nature","Cat","Dog","Food","Cricket","Space","Story","Health","Music","Movie","Temple","Flower","Sea","Mountain","River","Sky","Star","Moon","Sun","Bird","Animal","Baby","Teacher","Student","Business","Money","Yoga","Meditation","Fitness","Diet","Sleep","Beauty","Fashion","Game","Sport","Football","Science","History","Culture","Festival","Marriage","Family","Friendship","Study","Dream","Success","Motivation","Peace","Courage","Kindness","Truth","Wisdom","Power","Magic","Luck","Destiny","Karma","Rain","Village","City","Chennai","Madurai","Delhi","Mumbai","London","Paris","Tokyo","New York","Egypt","Pyramids","Taj Mahal","Eiffel Tower","Psychology","Philosophy","Economics","Politics","Law","Education","Happiness","Smile","Heart","Future","Freedom","Hope","Faith",
# Japan
"Japan","Tokyo","Sakura","Kimono","Anime","Japanese Food","Sushi","Kyoto","Osaka","Japanese Temple","Japanese Girl","Samurai","Ninja",
# China
"China","Beijing","Great Wall","Panda","Chinese Food","Chinese Temple","Shanghai","Chinese Culture","Dragon","Chinese Girl",
# India
"India","Tamil Nadu","Kerala","Saree","Biryani","Diwali","Pongal","Indian Temple","Indian Food","Indian Girl","Kolkata","Bangalore","Hyderabad",
# Extra
"Beach","Forest","Desert","Snow","Fire","Earth","Water","Coffee","Tea","Cake","Pizza","Burger","Chocolate","Fruit","Vegetable","Summer","Winter","Monsoon","Morning","Night","Home","Garden","Park","Elephant","Tiger","Lion","Horse","Bike","Car","Train","Flight","Phone","Computer","Book","Kavithai","Thirukkural","Pazhamozhi","Joke","Reading","Writing","Poetry","Singing","Dancing"]

# Category -> Search term mapping for Japan / China / India sources
# Openverse + Wikimedia + Unsplash ellam itha use pannum - No Watermark!
SEARCH_MAP = {
    "Japan": "Japan Tokyo", "Tokyo": "Tokyo Japan", "Sakura": "Sakura cherry blossom Japan", "Kimono": "Kimono Japanese woman", "Anime": "Anime illustration", "Japanese Food": "Japanese food sushi", "Sushi": "Sushi Japanese food", "Kyoto": "Kyoto Japan temple", "Osaka": "Osaka Japan", "Japanese Temple": "Japanese temple", "Japanese Girl": "Japanese girl portrait", "Samurai": "Samurai Japan", "Ninja": "Ninja Japan",
    "China": "China Beijing", "Beijing": "Beijing China", "Great Wall": "Great Wall of China", "Panda": "Giant panda", "Chinese Food": "Chinese food", "Chinese Temple": "Chinese temple", "Shanghai": "Shanghai China", "Chinese Culture": "Chinese culture", "Dragon": "Chinese dragon", "Chinese Girl": "Chinese girl portrait",
    "India": "India", "Tamil Nadu": "Tamil Nadu temple", "Kerala": "Kerala India", "Saree": "Saree Indian woman", "Biryani": "Biryani Indian food", "Diwali": "Diwali festival India", "Pongal": "Pongal festival Tamil", "Indian Temple": "Indian temple", "Indian Food": "Indian food", "Indian Girl": "Indian girl portrait", "Chennai": "Chennai Tamil Nadu", "Madurai": "Madurai temple",
    "Science": "science laboratory microscope", "Space": "space stars galaxy rocket", "Nature": "beautiful nature forest mountain", "Health": "yoga healthy fitness meditation", "Food": "delicious food", "Cricket": "cricket stadium match", "Temple": "hindu temple", "God": "hindu god temple divine",
}

def search_term(cat):
    return SEARCH_MAP.get(cat, cat)

def send_to_channel(text, bot_token, bot_name="Worker"):
    if not bot_token or not DATA_CHANNEL: return False
    for attempt in range(2):
        try:
            r = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": DATA_CHANNEL, "text": text[:4000]}, timeout=15)
            print(f"Worker Send: {r.status_code} to Data Channel - {bot_name}", flush=True)
            if r.status_code==200: return True
            if r.status_code==400:
                print(f"Worker Send 400 - {bot_name} - {r.text[:200]}", flush=True)
                time.sleep(2); continue
            time.sleep(1)
        except Exception as e: print(f"Worker Send Error {e}", flush=True); time.sleep(2)
    return False

# --- FREE SOURCES - No Watermark - No Key - No Login ---
# 1. Openverse - 800M free photos - No watermark - Best for Japan/China/India!
# 2. Wikimedia - 100M free photos - No watermark
# 3. Unsplash Source - Free - No watermark
def fetch_openverse(query, page=1):
    try:
        r = requests.get("https://api.openverse.org/v1/images/", params={"q": query, "page": page, "page_size": 20}, headers={"User-Agent": "AIRAH1-Bot/1.0"}, timeout=20)
        if r.status_code == 200:
            out = []
            for it in r.json().get("results", []):
                u = it.get("foreign_landing_url") or it.get("url")
                if u: out.append(u)
            return out
    except Exception as e: print(f"Openverse Error {e}", flush=True)
    return []

def fetch_wikimedia(query):
    try:
        r = requests.get("https://commons.wikimedia.org/w/api.php", params={"action":"query","format":"json","list":"search","srsearch":query,"srnamespace":6,"srlimit":20}, headers={"User-Agent": "AIRAH1-Bot/1.0 (Tamil Books)"}, timeout=20)
        if "application/json" not in r.headers.get("content-type",""): return []
        out = []
        for item in r.json().get("query",{}).get("search",[])[:20]:
            t = item.get("title","")
            if t: out.append(f"https://commons.wikimedia.org/wiki/{t.replace(' ','_')}")
        return out
    except Exception as e: print(f"Wikimedia Error {e}", flush=True); return []

def bot1_image_worker():
    idx = 0
    while True:
        try:
            cat = BASE_CATS[idx % len(BASE_CATS)]; idx += 1
            q = search_term(cat)
            print(f"Bot1 - Category: {cat} - Search: {q} - 100 Image Start! - Repo {CURRENT_REPO[0]}", flush=True)
            # Collect pool - Openverse + Wikimedia - Infinite source
            pool = []
            # Openverse - 3 pages = 60 images
            for p in [1,2,3]:
                pool += fetch_openverse(q, page=p)
                time.sleep(1)
            # Wikimedia - 20 images
            pool += fetch_wikimedia(q)
            # Unsplash - backup - 20 slots (same base URL with different query, Telegram will preview)
            # Deduplicate, keep order
            seen = set(); uniq = []
            for u in pool:
                if u not in seen: seen.add(u); uniq.append(u)
            pool = uniq
            print(f"Bot1 - {cat} - Pool {len(pool)} - Start 100 loop", flush=True)
            # FIX: Oru category ku 100/100 varaikkum angaye iru! 7/100 illa!
            for n in range(1, 101):
                try:
                    if pool:
                        url = pool[(n-1) % len(pool)]
                        src = "Openverse" if "openverse" in url.lower() or "flickr" in url.lower() or "wordpress" in url.lower() or "http" in url else "Wikimedia"
                        if "commons.wikimedia" in url: src = "Wikimedia"
                        elif "unsplash" in url: src = "Unsplash"
                        else: src = "Openverse"
                    else:
                        # Fallback - Unsplash Source - No watermark
                        url = f"https://source.unsplash.com/800x600/?{q.replace(' ','%20')}"
                        src = "Unsplash"
                    # Every 10th - Unsplash extra variety
                    if n % 10 == 0:
                        url = f"https://source.unsplash.com/800x600/?{q.replace(' ','%20')}"
                        src = "Unsplash"
                    send_to_channel(f"Auto Image - {cat} - {n}/100 📸\nSource: {src} - No Watermark - Made by Aira H1 ❤️\n{url}", BOT1_TOKEN, "Bot1-Image")
                    save_github(f"images-{cat}-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{cat} - {src} - {url}")
                    print(f"Bot1 - {cat} - {n}/100 Done!", flush=True)
                    time.sleep(2)  # Slow - 2 sec ku 1 image - Spam illa
                except Exception as e: print(f"Bot1 100 Error {e}", flush=True); time.sleep(2)
            print(f"Bot1 Done - {cat} - 100/100 - Next Category!", flush=True)
            time.sleep(10)
        except Exception as e: print(f"Bot1 Error {e}", flush=True); time.sleep(30)

def bot2_knowledge_worker():
    idx = 0
    while True:
        try:
            topic = BASE_CATS[idx % len(BASE_CATS)]; idx += 1
            print(f"Bot2 - Topic: {topic} - Batch {idx}", flush=True)
            try:
                r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ','_')}", headers={"User-Agent": "AIRAH1-Bot/1.0"}, timeout=10)
                if r.status_code==200:
                    ex = r.json().get("extract","")[:600]
                    if ex:
                        send_to_channel(f"Auto Knowledge - {topic} 🧠\n{ex}", BOT2_TOKEN, "Bot2-Wiki")
                        save_github(f"knowledge-worker-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{topic} - {ex}")
            except Exception as e: print(f"Wiki Error {e}", flush=True)
            try:
                r = requests.get("https://openlibrary.org/search.json", params={"q":topic,"limit":5}, timeout=10)
                for b in r.json().get("docs",[])[:3]:
                    title = b.get("title","")
                    if title:
                        send_to_channel(f"Auto Book - {topic} - {title} 📚", BOT2_TOKEN, "Bot2-Book")
                        save_github(f"books-worker-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{topic} - {title}")
            except Exception as e: print(f"OpenLibrary Error {e}", flush=True)
            try:
                r = requests.get("https://archive.org/advancedsearch.php", params={"q":f"title:({topic}) AND mediatype:texts","fl[]":"identifier,title","rows":5,"output":"json"}, timeout=15)
                for d in r.json().get("response",{}).get("docs",[])[:2]:
                    ident = d.get("identifier",""); title = d.get("title","Book")
                    if ident:
                        send_to_channel(f"Auto Book Archive - {topic} - {title} 📚\nhttps://archive.org/details/{ident}", BOT2_TOKEN, "Bot2-Archive")
                        save_github(f"books-archive-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{topic} - {ident} - {title}")
            except Exception as e: print(f"Archive Error {e}", flush=True)
            try:
                r = requests.get("https://opentdb.com/api.php", params={"amount":1,"type":"multiple"}, timeout=10)
                if r.status_code==200:
                    qd = r.json().get("results",[])[0]
                    # FIX: &quot; pogum - html.unescape + tags remove
                    ques = re.sub(r'<[^>]+>', '', html.unescape(qd.get('question','')))
                    ans = re.sub(r'<[^>]+>', '', html.unescape(qd.get('correct_answer','')))
                    cat2 = re.sub(r'<[^>]+>', '', html.unescape(qd.get('category','')))
                    msg = f"Auto Quiz - {topic} 🧠\nQ: {ques}\nA: {ans} - {cat2}"
                    send_to_channel(msg, BOT2_TOKEN, "Bot2-Quiz")
                    save_github(f"quiz-worker-{datetime.now().strftime('%Y-%m-%d')}.txt", msg)
            except Exception as e: print(f"Quiz Error {e}", flush=True)
            print(f"Bot2 Done - {topic} - Infinite Next!", flush=True)
            time.sleep(30)
        except Exception as e: print(f"Bot2 Error {e}", flush=True); time.sleep(30)

def self_heal():
    while True:
        try:
            time.sleep(60)
            print(f"Self-Heal - Worker - Repo {CURRENT_REPO[0]} - OK", flush=True)
            save_github(f"heartbeat-worker-{datetime.now().strftime('%Y-%m-%d')}.txt", f"Worker Alive - {datetime.now()} - Repo {CURRENT_REPO[0]}")
        except Exception as e: print(f"Self-Heal Error {e}", flush=True); time.sleep(30)

if __name__ == "__main__":
    print("AIRAH1 WORKER FINAL INFINITE - Started - Data Channel!", flush=True)
    threading.Thread(target=bot1_image_worker, daemon=True).start()
    threading.Thread(target=bot2_knowledge_worker, daemon=True).start()
    threading.Thread(target=self_heal, daemon=True).start()
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200); self.end_headers(); self.wfile.write(b"AIRAH1 Worker Final Infinite ON")
            def do_HEAD(self):
                self.send_response(200); self.end_headers()
            def log_message(self,*a): pass
        HTTPServer(("0.0.0.0", int(os.getenv("PORT","10000"))), H).serve_forever()
    except:
        while True: time.sleep(60)
