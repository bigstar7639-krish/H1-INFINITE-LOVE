# AIRAH1 - FINAL FIXED - Infinite Smart Chat
# File: aira_server.py
import os, random, time, threading, requests, base64
from datetime import datetime

# FIX - Rendum Peru Support - Env Peru Enna Irundhalum Work Aagum!
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN","") or os.getenv("BOT_TOKEN","") or os.getenv("BOT_TOKEN_2","")
GROQ_KEYS = [os.getenv("GROQ_API_KEY",""), os.getenv("GROQ_API_KEY_2",""), os.getenv("GROQ_API_KEY_3","")]
GEMINI_KEYS = [os.getenv("GEMINI_API_KEY",""), os.getenv("GEMINI_API_KEY_2","")]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
GITHUB_USER = "bigstar7639-krish"
CHAT_ID = os.getenv("CHAT_ID","") or os.getenv("GROUP_ID","-1003935111481")
BOOKS_ID = os.getenv("BOOKS_ID","") or os.getenv("CHANNEL_ID","-1003940504242")
print(f"Token OK? {bool(TELEGRAM_TOKEN)} Chat: {CHAT_ID} Books: {BOOKS_ID}", flush=True)

TOPICS = ["Love","Career","Health","Money","AI","Tech","Space","Business","Anger","Confidence","Happiness","Food","Family","Friendship","Study","Dream","Success","Motivation","Peace","Courage","Kindness","Nature","Music","Travel","Book","Life","Time","Trust","Hope","Faith","Smile","Heart","Soul","Future","Past","Present","Freedom","Truth","Wisdom","Power","Energy","Magic","Luck","Destiny","Karma","Yoga","Meditation","Fitness","Diet","Sleep","Beauty","Fashion","Movie","Game","Sport","Cricket","Football","Science","Maths","History","Geography","Politics","Culture","Festival","Marriage","Baby","Child","Mother","Father","Brother","Sister","Teacher","Student","Job","Interview","Salary","Business Idea","Startup","Coding","Python","Internet","Phone","Social Media","YouTube","Instagram","Telegram","Rain","Sea","Mountain","River","Sky","Star","Moon","Sun","Flower","Tree","Bird","Animal","Dog","Cat","Temple","Prayer","God","Spiritual","Tamil Culture","Chennai","India","World","Universe","Alien","Robot","Future Tech","Electric Car","Climate","Environment","Water","Air","Earth","Sad","Happy","Life"]

QUESTIONS = ["Unakku {t} pathi enna theriyum? Sollu paapom!","Ne {t} la eppadi improve panna mudiyum?","{t} pathi oru secret sollatta?","Un life la {t} eppadi irukku? Happy ah?","{t} pathi oru story kekkura?","Life ku artham enna?","Family problem ah eppadi solve pannanum?","Sad - Enna pannalam?"]
ANSWERS = ["{t} - Life la romba mukkiyam! Daily try pannu - Jeyichiduva! Aira un kooda irukka!","Unakku {t} pathi doubt iruntha - Kekkam - Aira sollitharen!"]
JOKES = ["Teacher: Yen late? Student: Road la board paathen - School Ahead! 😂","Why bike sad? Petrol illa!","Doctor: Enna problem? Patient: Phone charge aagala - Life charge aagala! 😂"]
FACTS = ["Honey - 3000 varusham aana kooda kedathu!","Octopus ku 3 heart irukku!","Moon - Daily konjam konjam thalli poguthu!","Tamil - 2000+ varusha pazhamaiyana mozhi!"]
QUOTES = ["Daily try pannu - Jeyichiduva! - Aira","Porumaiya iru - Nambikkaiya iru - Aira un kooda irukka!"]
MOTIVATIONS = ["Paravalla! Rest edu - Thirumba try pannu! - Aira","Unakku mudiyum - Nambikkai vechu try pannu!"]
STORIES = ["Oru chinna paiyan daily school ku ponaan! 1000 Tamil books irunthuchu! Oru chinna ponnu daily anga pova! Aprom rendu perum best friends aayitanga!","Oru oor la oru paiyan irunthan - Avan daily try pannan - Oru naal jeyichitan! Neeyum jeyippa!"]

count = 0
fact_count = 0
book_count = 0

def send_telegram(text, chat_id=None):
    if not TELEGRAM_TOKEN:
        print("ERROR: No Token!", flush=True); return
    if not chat_id: chat_id = CHAT_ID
    try:
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
        print(f"TG Send: {r.status_code} to {chat_id}", flush=True)
    except Exception as e: print(f"TG Send Error {e}", flush=True)

def save_github(filename, content):
    if not GITHUB_TOKEN: return
    try:
        url = f"https://api.github.com/repos/{GITHUB_USER}/H1-Data-3/contents/data/{filename}"
        r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        sha = r.json().get("sha") if r.status_code == 200 else None
        b64 = base64.b64encode(content.encode()).decode()
        payload = {"message": f"Save {filename}", "content": b64}
        if sha: payload["sha"] = sha
        rr = requests.put(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload, timeout=10)
        if rr.status_code in (200, 201): print(f"【entity-GitHub¦canonical_name=GitHub】 Save OK - H1-Data-3/{filename} - Count {count}", flush=True)
    except Exception as e: print("【entity-GitHub¦canonical_name=GitHub】 error", e, flush=True)

def ai_answer(q):
    for key in GROQ_KEYS:
        if not key: continue
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": f"You are Aira, Tamil Tanglish friendly AI. User: {q}"}]}, timeout=15)
            if r.status_code == 200:
                print("AI Answer - Groq1 - openai/gpt-oss-120b - OK", flush=True)
                return r.json()["choices"][0]["message"]["content"][:800]
        except: pass
    return random.choice(ANSWERS).format(t=q)

def ai_reply(txt):
    low = txt.lower()
    if "namaste" in low: return "Namaste! Main Aira hoon! Kaise ho? ❤️"
    if "hola" in low: return "Hola! Soy Aira! Como estas? ❤️"
    if "bonjour" in low: return "Bonjour! Je suis Aira! ❤️"
    if "hi" in low or "hello" in low: return "Hi 💘! Naan Aira! Enna pannura? Kadhal ah? Career ah? Joke venuma? Story venuma? 😊💜"
    if "joke" in low: return random.choice(JOKES)
    if "book" in low: return "Book - Channel la varum! 📚"
    return None

def infinite_loop():
    global count, fact_count
    while True:
        try:
            count += 1
            typ = random.choice(["Q","AI Q","Story","Joke","Fact","Quote","Motivation","Smart Q"])
            t = random.choice(TOPICS)
            if typ == "Q":
                msg = f"Q {count} - {random.choice(QUESTIONS).format(t=t)}"
                print(f"Q {count} - {t}", flush=True)
            elif typ == "AI Q":
                q = random.choice(QUESTIONS).format(t=t)
                print(f"AI Q {count} - {q}", flush=True)
                msg = f"Aira AI: {ai_answer(q)}"
            elif typ == "Story":
                msg = f"Story {count}\n{random.choice(STORIES)}"
                print(f"Story {count}", flush=True)
            elif typ == "Joke":
                msg = f"Joke {count}\n{random.choice(JOKES)}"
                print(f"Joke {count}", flush=True)
            elif typ == "Fact":
                fact_count += 1; msg = f"Fact {fact_count} - {random.choice(FACTS)}"
                print(f"Fact {fact_count}", flush=True)
            elif typ == "Quote":
                msg = f"Quote {count} - {random.choice(QUOTES)}"
                print(f"Quote {count}", flush=True)
            elif typ == "Smart Q":
                msg = f"Smart Q {count} - {t} la eppadi jeyikkarathu? Sollu!"
                print(f"Smart Q {count} - {t}", flush=True)
            else:
                msg = f"Motivation {count}\n{random.choice(MOTIVATIONS)}"
                print(f"Motivation {count}", flush=True)
            send_telegram(msg)
            d = datetime.now().strftime("%Y-%m-%d")
            save_github(f"chat-{d}.txt", msg)
            time.sleep(10)
        except Exception as e:
            print("Infinite error", e, flush=True); time.sleep(5)

def books_loop():
    global book_count
    while True:
        try:
            print("Download Source: archive - Query: Tamil - Page 19", flush=True)
            r = requests.get("https://archive.org/advancedsearch.php", params={"q": "language:(tam) AND mediatype:texts", "fl[]": "identifier,title", "rows": 20, "output": "json"}, timeout=15)
            docs = r.json().get("response", {}).get("docs", [])
            print(f"Books Found archive: {len(docs)}", flush=True)
            for d in docs[:5]:
                ident = d.get("identifier", "")
                if not ident: continue
                dl = requests.get(f"https://archive.org/download/{ident}/{ident}_djvu.txt", timeout=15)
                print(f"Download archive {ident} - {dl.status_code} - {len(dl.content)/1024/1024:.2f} MB", flush=True)
                if dl.status_code == 200:
                    book_count += 1
                    send_telegram(f"Book Tamil Nadu - {d.get('title','Tamil Book')} 📚\nhttps://archive.org/download/{ident}", BOOKS_ID)
                    dd = datetime.now().strftime("%Y-%m-%d")
                    save_github(f"books-{dd}.txt", f"{ident} - {d.get('title')}")
            print("Batch Done - madurai - New 12 - 10 sec wait...", flush=True)
            time.sleep(60)
        except Exception as e:
            print("Books error", e, flush=True); time.sleep(30)

def listen_loop():
    offset = 0
    while True:
        try:
            if not TELEGRAM_TOKEN: time.sleep(5); continue
            r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates", params={"offset": offset, "timeout": 20}, timeout=30)
            for u in r.json().get("result", []):
                offset = u["update_id"] + 1
                m = u.get("message", {}); txt = m.get("text", "")
                if not txt: continue
                if m.get("from", {}).get("is_bot"): continue
                if "aira" in txt.lower() or "hi" in txt.lower() or "joke" in txt.lower():
                    print(f"Listen Got: {txt}", flush=True)
                    rep = ai_reply(txt)
                    if not rep: rep = ai_answer(txt)
                    send_telegram(rep, m["chat"]["id"])
                    print("Listen Replied", flush=True)
        except Exception as e: print("Listen error", e, flush=True); time.sleep(5)

if __name__ == "__main__":
    print("AIRAH1 Fixed Infinite - Started", flush=True)
    threading.Thread(target=infinite_loop, daemon=True).start()
    threading.Thread(target=listen_loop, daemon=True).start()
    threading.Thread(target=books_loop, daemon=True).start()
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        class H(BaseHTTPRequestHandler):
            def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"AIRAH1 Fixed Infinite ON")
            def log_message(self, *a): pass
        HTTPServer(("0.0.0.0", int(os.getenv("PORT", "10000"))), H).serve_forever()
    except:
        while True: time.sleep(60)
