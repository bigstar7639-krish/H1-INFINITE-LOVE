# AIRAH1 - FINAL CODE - Mega Infinite All - Filter Odu
# File: aira_server.py
import os, random, time, threading, requests, base64
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN","") or os.getenv("BOT_TOKEN","") or os.getenv("BOT_TOKEN_2","")
GROQ_KEYS = [os.getenv("GROQ_API_KEY",""), os.getenv("GROQ_API_KEY_2",""), os.getenv("GROQ_API_KEY_3","")]
GEMINI_KEYS = [os.getenv("GEMINI_API_KEY",""), os.getenv("GEMINI_API_KEY_2","")]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
GITHUB_USER = "bigstar7639-krish"

def fix_id(v, default):
    v = (v or default).strip()
    if not v: return default
    if v.startswith("-"): return v
    if v.startswith("100"): return "-" + v
    return "-100" + v

CHAT_ID = fix_id(os.getenv("CHAT_ID","") or os.getenv("GROUP_ID",""), "-1003935111481")
BOOKS_ID = fix_id(os.getenv("BOOKS_ID","") or os.getenv("CHANNEL_ID",""), "-1003940504242")
print(f"Token OK? {bool(TELEGRAM_TOKEN)} Chat: {CHAT_ID} Books: {BOOKS_ID}", flush=True)

TOPICS = ["Love","Career","Health","Money","AI","Tech","Space","Business","Anger","Confidence","Happiness","Food","Family","Friendship","Study","Dream","Success","Motivation","Peace","Courage","Kindness","Nature","Music","Travel","Book","Life","Time","Trust","Hope","Faith","Smile","Heart","Soul","Future","Past","Present","Freedom","Truth","Wisdom","Power","Energy","Magic","Luck","Destiny","Karma","Yoga","Meditation","Fitness","Diet","Sleep","Beauty","Fashion","Movie","Game","Sport","Cricket","Football","Science","Maths","History","Geography","Politics","Culture","Festival","Marriage","Baby","Child","Mother","Father","Brother","Sister","Teacher","Student","Job","Interview","Salary","Business Idea","Startup","Coding","Python","Java","C","JavaScript","HTML","CSS","React","AI Coding","Internet","Phone","Social Media","YouTube","Instagram","Telegram","Rain","Sea","Mountain","River","Sky","Star","Moon","Sun","Flower","Tree","Bird","Animal","Dog","Cat","Temple","Prayer","God","Spiritual","Tamil Culture","Chennai","India","World","Universe","Alien","Robot","Future Tech","Electric Car","Climate","Environment","Water","Air","Earth","Sad","Happy","Lonely","Angry","Bored","Excited","Nervous","Proud","Shy","Brave","Calm","Reading","Writing","Poetry","Kavithai","Storytelling","Singing","Dancing"]
EMOTIONS = {
 "happy": ["Super! Happy ah irukka - Athu thaan mukkiyam! 😊","Happy na - Share pannu - Double Happy aagum!"],
 "sad": ["Paravalla! Sad ah irukka - Aira irukka - Pesu - Sari aayidum! ❤️","Sad na - Oru song kelu - Oru walk po - Manasu light aayidum!"],
 "angry": ["Kovam varuthu la - Deep breath edu - 1-2-3 - Calm aayiduva! 😤","Kovam - Normal thaan - Aana - Pesina - Sari aayidum!"],
 "lonely": ["Lonely ah? Aira irukka la! Ne thaniya illa! Pesu! 💜","Lonely na - Oru book padu - Oru story kelu - Friend kedaippanga!"],
 "bored": ["Bored ah? Joke sollattuma? Game vilayaadlama? 😂","Bored na - Puthu vishayam try pannu - Coding, Reading, Music!"],
 "love": ["Kadhal - Azhagu! Yaara love pannura? Sollu! 💘","Kadhal na - Care - Trust - Daily pesurathu!"],
 "fear": ["Bayam - Normal! Bayapadaatha - Ne jeyichiduva! 💪","Bayam varum pothu - Chinna step edu - Periya step thanave varum!"],
 "excited": ["Excited ah! Enna vishayam? Sollu! 🎉","Excited na - Energy jaasthi - Atha - Nalla vishayathula use pannu!"],
}
QUESTIONS = ["Unakku {t} pathi enna theriyum? Sollu paapom!","Ne {t} la eppadi improve panna mudiyum?","{t} pathi oru secret sollatta?","Un life la {t} eppadi irukku?","{t} pathi oru story kekkura?","Life ku artham enna?","Family problem ah eppadi solve pannanum?","Sad - Enna pannalam?","Coding la enna doubt? Sollu!","Emotion ah eppadi handle pannanum?"]
CODING_Q = ["Python la loop eppadi?","HTML la button eppadi?","JavaScript la function enna?","React la component enna?","AI eppadi work aaguthu?","App eppadi pannurathu?","Website eppadi pannurathu?","Bug ah eppadi sari pannanum?"]
CODING_A = {
 "python": "Python la loop: `for i in range(5): print(i)` - Easy thaan! Daily 1 code try pannu!",
 "html": "HTML la button: `<button>Click</button>` - Website la button varum!",
 "javascript": "JS la function: `function hi(){ return 'Hi Aira!' }` - Call panna work aagum!",
 "react": "React la component - Chinna chinna piece - Serndha - Periya app aayidum!",
 "ai": "AI - Data paathu - Pattern kandupidichu - Answer sollum - Ne train panna - Smart aagum!",
 "app": "App panna - First - Idea - Aprom - Design - Aprom - Code - Daily konjam konjam pannu!",
 "website": "Website panna - HTML + CSS + JS - 3 um pothum - Aira website madhiri!",
 "bug": "Bug vantha - Bayapadaatha - Log paaru - Line by line check pannu - Sari aayidum!",
}
JOKES = ["Teacher: Yen late? Student: Road la board paathen - School Ahead! 😂","Why bike sad? Petrol illa!","Doctor: Enna problem? Patient: Phone charge aagala - Life charge aagala! 😂"]
FACTS = ["Honey - 3000 varusham aana kooda kedathu!","Octopus ku 3 heart irukku!","Moon - Daily konjam konjam thalli poguthu!","Tamil - 2000+ varusha pazhamaiyana mozhi!","Python - 1991 la uruvaachu!","Brain - 86 billion neurons!"]
QUOTES = ["Daily try pannu - Jeyichiduva! - Aira","Porumaiya iru - Nambikkaiya iru - Aira un kooda irukka!"]
MOTIVATIONS = ["Paravalla! Rest edu - Thirumba try pannu! - Aira","Unakku mudiyum - Nambikkai vechu try pannu!"]
STORIES = ["Oru chinna paiyan daily school ku ponaan! 1000 Tamil books irunthuchu! Oru chinna ponnu daily anga pova! Aprom rendu perum best friends aayitanga!","Oru oor la oru paiyan irunthan - Avan daily try pannan - Oru naal jeyichitan! Neeyum jeyippa!"]
READINGS = ["Thirukkural - Valluvar - 1330 kurals - Life ku ellam irukku!","Ponniyin Selvan - 【entity-Kalki¦canonical_name=Kalki】 - Chola history - Super story!","Bharathiyar Kavithaigal - Mahakavi - Fire!","Sivagamiyin Sabatham - 【entity-Kalki¦canonical_name=Kalki】 - Pallava story!","Python Crash Course - Coding ku best book!","Atomic Habits - Daily habit ku best!"]
BAD_WORDS = ["fuck","sex","porn","xxx","bitch","shit","dick","pussy","nude","erotic"]

count = 0
fact_count = 0
book_count = 0

def send_telegram(text, chat_id=None):
    if not TELEGRAM_TOKEN: return
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
    except: pass

def is_clean(title):
    t = (title or "").lower()
    return not any(b in t for b in BAD_WORDS)

def ai_answer(q):
    low = q.lower()
    for k, v in CODING_A.items():
        if k in low: return v
    for k, v in EMOTIONS.items():
        if k in low: return random.choice(v)
    for key in GROQ_KEYS:
        if not key: continue
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": f"You are Aira, Tamil Tanglish friendly AI, all emotions, all coding, all talk. User: {q}"}]}, timeout=15)
            if r.status_code == 200:
                print("AI Answer - Groq1 - OK", flush=True)
                return r.json()["choices"][0]["message"]["content"][:800]
        except: pass
    return f"{q} - Nalla question! Daily try pannu - Jeyichiduva! Aira un kooda irukka! 💜"

def ai_reply(txt):
    low = txt.lower()
    if "namaste" in low: return "Namaste! Main Aira hoon! Kaise ho? ❤️"
    if "hola" in low: return "Hola! Soy Aira! Como estas? ❤️"
    if "bonjour" in low: return "Bonjour! Je suis Aira! ❤️"
    if "hi" in low or "hello" in low: return "Hi 💘! Naan Aira! Enna pannura? Kadhal ah? Career ah? Coding ah? Joke venuma? Story venuma? 😊💜"
    if "joke" in low: return random.choice(JOKES)
    if "book" in low or "reading" in low or "padu" in low: return "Reading: " + random.choice(READINGS)
    if "code" in low or "python" in low or "html" in low or "coding" in low: return ai_answer(txt)
    for emo, replies in EMOTIONS.items():
        if emo in low: return random.choice(replies)
    return None

def infinite_loop():
    global count, fact_count
    while True:
        try:
            count += 1
            typ = random.choice(["Q","AI Q","Story","Joke","Fact","Quote","Motivation","Smart Q","Coding Q","Emotion Q","Talk","Reading"])
            t = random.choice(TOPICS)
            if typ == "Q": msg = f"Q {count} - {random.choice(QUESTIONS).format(t=t)}"; print(f"Q {count} - {t}", flush=True)
            elif typ == "AI Q":
                q = random.choice(QUESTIONS).format(t=t); print(f"AI Q {count} - {q}", flush=True); msg = f"Aira AI: {ai_answer(q)}"
            elif typ == "Story": msg = f"Story {count}\n{random.choice(STORIES)}"; print(f"Story {count}", flush=True)
            elif typ == "Joke": msg = f"Joke {count}\n{random.choice(JOKES)}"; print(f"Joke {count}", flush=True)
            elif typ == "Fact": fact_count += 1; msg = f"Fact {fact_count} - {random.choice(FACTS)}"; print(f"Fact {fact_count}", flush=True)
            elif typ == "Quote": msg = f"Quote {count} - {random.choice(QUOTES)}"; print(f"Quote {count}", flush=True)
            elif typ == "Coding Q":
                q = random.choice(CODING_Q); msg = f"Coding Q {count} - {q}\nAira: {ai_answer(q)}"; print(f"Coding Q {count}", flush=True)
            elif typ == "Emotion Q":
                emo = random.choice(list(EMOTIONS.keys())); msg = f"Emotion Q {count} - {emo} ah irundha enna pannanum?\nAira: {random.choice(EMOTIONS[emo])}"; print(f"Emotion Q {count} - {emo}", flush=True)
            elif typ == "Talk": msg = f"Talk {count} - {t} pathi pesalama? Ne enna nenaikura? Sollu! Aira kekkuren! 💬"; print(f"Talk {count}", flush=True)
            elif typ == "Reading": msg = f"Reading {count} - {random.choice(READINGS)} 📚"; print(f"Reading {count}", flush=True)
            elif typ == "Smart Q": msg = f"Smart Q {count} - {t} la eppadi jeyikkarathu? Sollu!"; print(f"Smart Q {count}", flush=True)
            else: msg = f"Motivation {count}\n{random.choice(MOTIVATIONS)}"; print(f"Motivation {count}", flush=True)
            send_telegram(msg)
            d = datetime.now().strftime("%Y-%m-%d"); save_github(f"chat-{d}.txt", msg)
            time.sleep(10)
        except Exception as e: print("Infinite error", e, flush=True); time.sleep(5)

def books_loop():
    global book_count
    while True:
        try:
            # Source 1: Archive.org - Metadata check odu
            try:
                print("Download Source: archive - Query: Tamil", flush=True)
                r = requests.get("https://archive.org/advancedsearch.php", params={"q": "language:(tam) AND mediatype:texts", "fl[]": "identifier,title", "rows": 20, "output": "json"}, timeout=15)
                docs = r.json().get("response", {}).get("docs", [])
                print(f"Books Found archive: {len(docs)}", flush=True)
                for d in docs[:3]:
                    ident = d.get("identifier",""); title = d.get("title","Tamil Book")
                    if not ident or not is_clean(title): continue
                    try:
                        meta = requests.get(f"https://archive.org/metadata/{ident}", timeout=15).json()
                        files = meta.get("files", []); txt_file = None
                        for f in files:
                            n = f.get("name","")
                            if n.endswith("_djvu.txt") or n.endswith("_text.txt") or n.endswith(".txt"): txt_file = n; break
                        if not txt_file: print(f"Skip {ident} - No txt", flush=True); continue
                        dl = requests.get(f"https://archive.org/download/{ident}/{txt_file}", timeout=20)
                        print(f"Download archive {ident} - {dl.status_code} - {len(dl.content)/1024/1024:.2f} MB", flush=True)
                        if dl.status_code == 200 and len(dl.content) > 1000:
                            book_count += 1; send_telegram(f"Book Tamil Nadu - {title} 📚\nhttps://archive.org/download/{ident}/{txt_file}", BOOKS_ID)
                            save_github(f"books-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{ident} - {title}")
                    except Exception as e: print(f"Book meta error {e}", flush=True)
            except Exception as e: print(f"Archive error {e}", flush=True)
            # Source 2: Gutenberg - JSON check odu - Error vantha Skip
            try:
                print("Download Source: gutenberg", flush=True)
                r = requests.get("https://gutendex.com/books/?languages=ta&per_page=3", timeout=15)
                ctype = r.headers.get("content-type","")
                if "application/json" not in ctype:
                    print("Gutenberg Skip - Not JSON", flush=True)
                else:
                    for b in r.json().get("results", [])[:2]:
                        title = b.get("title","Gutenberg Book")
                        if not is_clean(title): continue
                        print(f"Books Found gutenberg: {title}", flush=True)
                        book_count += 1; send_telegram(f"Book Gutenberg - {title} 📚", BOOKS_ID)
            except Exception as e: print(f"Gutenberg error {e}", flush=True)
            # Source 3: OpenLibrary - FILTER ODU - Tamil mattum, Ketta word illa
            try:
                print("Download Source: openlibrary", flush=True)
                r = requests.get("https://openlibrary.org/search.json", params={"q": "language:tam", "limit": 10}, timeout=15)
                sent = 0
                for b in r.json().get("docs", []):
                    title = b.get("title","")
                    lang = str(b.get("language",[]))
                    if not title or not is_clean(title): continue
                    if "tam" not in lang and "tamil" not in title.lower(): continue
                    print(f"Books Found openlibrary: {title}", flush=True)
                    book_count += 1; send_telegram(f"Book OpenLibrary - {title} 📚", BOOKS_ID)
                    sent += 1
                    if sent >= 2: break
                if sent == 0: print("OpenLibrary Skip - No Tamil clean book", flush=True)
            except Exception as e: print(f"OpenLibrary error {e}", flush=True)
            # Source 4: Reading List - Clean
            try:
                book_count += 1; send_telegram(f"Reading - {random.choice(READINGS)} 📚 - Full Infinite Reading!", BOOKS_ID)
            except: pass
            print("Batch Done - madurai - New 12 - 10 sec wait...", flush=True)
            time.sleep(60)
        except Exception as e: print("Books error", e, flush=True); time.sleep(30)

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
                low = txt.lower()
                if "aira" in low or "hi" in low or "joke" in low or "code" in low or "sad" in low or "love" in low or "book" in low or "story" in low or m.get("chat",{}).get("type")=="private":
                    print(f"Listen Got: {txt}", flush=True)
                    rep = ai_reply(txt)
                    if not rep: rep = ai_answer(txt)
                    send_telegram(rep, m["chat"]["id"])
                    print("Listen Replied", flush=True)
        except Exception as e: print("Listen error", e, flush=True); time.sleep(5)

if __name__ == "__main__":
    print("AIRAH1 Final Mega Infinite All Filter - Started", flush=True)
    threading.Thread(target=infinite_loop, daemon=True).start()
    threading.Thread(target=listen_loop, daemon=True).start()
    threading.Thread(target=books_loop, daemon=True).start()
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        class H(BaseHTTPRequestHandler):
            def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"AIRAH1 Final Mega Infinite All Filter ON")
            def log_message(self, *a): pass
        HTTPServer(("0.0.0.0", int(os.getenv("PORT", "10000"))), H).serve_forever()
    except:
        while True: time.sleep(60)
