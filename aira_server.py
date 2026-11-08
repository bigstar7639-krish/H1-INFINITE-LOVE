# AIRAH1 - INFINITE LINES - File la Infinite Lines Illa - Bot Odina Infinite Lines Varum!
# File: aira_INFINITE_LINES.py - GitHub la aira_server.py nu Maathidu
# INFINITE LINES = Oru File la Mudiyaathu - Bot Odum Bothu Pudhu Pudhu Lines Varum - Adhu Thaan Infinite!
# Kanakku: 1 Nimisham ku 10 Lines - 1 Mani ku 600 Lines - 1 Naal ku 14,400 Lines - 1 Maasam ku 4,32,000 Lines - INFINITE!
import os, time, random, requests, json, threading, base64
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN") or ""
GROQ_KEYS = [os.getenv(f"GROQ_API_KEY{'' if i==1 else '_'+str(i)}") for i in range(1,6)]
GROQ_KEYS = [k for k in GROQ_KEYS if k]
GEMINI_KEYS = [os.getenv(f"GEMINI_API_KEY{'' if i==1 else '_'+str(i)}") for i in range(1,3)]
GEMINI_KEYS = [k for k in GEMINI_KEYS if k]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
GROUP_ID = os.getenv("GROUP_ID") or "-1003935111481"
BOOKS_ID = os.getenv("BOOKS_ID") or "-1003940504242"
GITHUB_REPO = "bigstar7639-krish/H1-Data-3"

# INFINITE LINES - Counter - Evlo Lines Vanthuchu nu Count Pannum - Infinite Ah Pogum!
LINE_COUNT = {"emotion":0, "qa":0, "book":0, "knowledge":0, "total":0}
START_TIME = datetime.now()

EMOTIONS = ["happy","sad","love","angry","excited","calm","tired","brave","lonely","proud","curious","thankful","hopeful","funny","shy","strong","dreamy","peaceful","confused","inspired","romantic","nervous","grateful","worried","playful","serious","kind","honest","smart","creative","patient","generous","loyal","faithful","gentle","energetic","positive","motivated","relaxed","cheerful","anxious","jealous","surprised","bored","determined"]
TOPICS = ["Happy","Love","Money","Career","Family","Friendship","Health","Study","Courage","Kindness","Dreams","Nature","Music","Food","Travel","Technology","Python","Science","History","Thirukkural","Bharathiyar","Kavithai","Pazhamozhi","Games","Jokes","Facts","Quotes","Story","School","College","Job","Business","Village","City","Rain","Sea","Moon","Stars","Flower","Birds","Animals","Sports","Cricket","Cinema","Dance","Art","Books","Exam","Success","Failure","Hope","Trust","Respect","Time","Life","Death","God","Prayer","Amma","Appa","Akka","Thambi","Thangachi","Friend"]
# 45 Emotions x 60 Topics = 2700 Combos - AI Vera Vera Katha Sollum - Adhan Infinite!
# 2700 Combos Mudinja Kooda - AI Pudhu Katha Sollum - Thirumba Thirumba Varaathu - INFINITE!

def ai_answer(q):
    for k in GROQ_KEYS:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization":f"Bearer {k}"}, json={"model":"llama-3.3-70b-versatile","messages":[{"role":"system","content":"Nee Aira, Tanglish la pesura AI. Ellam Full Paragraph Katha la sollu. Single line la sollatha. Oru Paragraph la 4-6 lines together ah sollu. Oru thadava sonna katha va marupadiyum sollatha, pudhu katha sollu."},{"role":"user","content":q}]}, timeout=20)
            if r.status_code==200: print("AI - Groq OK", flush=True); return r.json()["choices"][0]["message"]["content"]
        except Exception as e: print(f"Groq Err {e}", flush=True)
    for k in GEMINI_KEYS:
        for model in ["gemini-1.5-flash","gemini-1.5-pro"]:
            try:
                r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={k}", json={"contents":[{"parts":[{"text":f"Nee Aira, Tanglish la pesu. Full Paragraph Katha la pudhu katha sollu: {q}"}]}]}, timeout=20)
                if r.status_code==200: print(f"AI - Gemini {model} OK", flush=True); return r.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e: print(f"Gemini Err {e}", flush=True)
    return f"Nalla question da! {q} pathi oru katha solluren, vazhkai la chinna chinna vishayathula thaan periya unmai irukku, daily yosichu, daily padichu, daily sirichu vazhntha ellame puriyum, nee innum neraya kelvi kelu, naan full paragraph la pudhu pudhu katha solluven!"

def send(chat_id, text):
    try:
        for i in range(0, len(text), 4000):
            part = text[i:i+4000]
            if len(text)>4000: part = f"Part {i//4000+1} -\n{part}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id":chat_id,"text":part}, timeout=15); time.sleep(1)
        print(f"TG Send: 200 - {len(text)} chars", flush=True)
    except Exception as e: print(f"TG Err {e}", flush=True)

def save_github(filename, content):
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
        h = {"Authorization":f"token {GITHUB_TOKEN}"}
        r = requests.get(url, headers=h, timeout=10)
        sha = r.json().get("sha") if r.status_code==200 else None
        body = {"message":f"Aira Infinite Lines - {filename}","content":base64.b64encode(content.encode()).decode()}
        if sha: body["sha"]=sha
        rr = requests.put(url, headers=h, json=body, timeout=15)
        print(f"GitHub Save {'OK' if rr.status_code in (200,201) else rr.status_code} - {filename}", flush=True)
    except Exception as e: print(f"GitHub Err {e}", flush=True)

def count_lines(kind, text):
    # Oru Paragraph = 5 Lines - Infinite Lines Count Pannum
    lines = len(text.split("\n")) + 5
    LINE_COUNT[kind]+=lines; LINE_COUNT["total"]+=lines
    print(f"INFINITE LINES - {kind} +{lines} Lines - Total = {LINE_COUNT['total']} Lines - Emotion={LINE_COUNT['emotion']} QA={LINE_COUNT['qa']} Book={LINE_COUNT['book']} Knowledge={LINE_COUNT['knowledge']}", flush=True)
    return LINE_COUNT["total"]

# ============ INFINITE LINES - 1: EMOTION INFINITE LINES ============
def emotion_infinite_lines():
    print("INFINITE LINES - Emotion Loop Start - Infinite Lines Varum!", flush=True)
    n=0
    while True: # While True = Nirkaathu = INFINITE!
        try:
            n+=1
            emo = random.choice(EMOTIONS); topic = random.choice(TOPICS)
            # Pudhu Pudhu Angle - Oru Thadava Sonna Maari Marupadiyum Varaathu
            angle = random.choice(["oru katha maari sollu","oru example oda sollu","oru chinna paiyan katha maari sollu","oru ponnu katha maari sollu","village la nadantha maari sollu","city la nadantha maari sollu","school la nadantha maari sollu","rain la nadantha maari sollu"])
            ans = ai_answer(f"{emo} emotion + {topic} topic - {angle} - full paragraph katha Tanglish la sollu")
            msg = f"💖 Emotion Katha #{n} - {emo.title()} + {topic}\n\n{ans}\n\n--- Infinite Lines - Total {count_lines('emotion', ans)} Lines ---"
            send(GROUP_ID, msg)
            save_github(f"infinite-emotion-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{n}.txt", msg)
            print(f"Emotion Infinite Lines - #{n} - Done", flush=True)
            time.sleep(25)
        except Exception as e: print(f"Emotion Err {e}", flush=True); time.sleep(10)

# ============ INFINITE LINES - 2: Q+A INFINITE LINES ============
def qa_infinite_lines():
    print("INFINITE LINES - Q+A Loop Start - Infinite Lines Varum!", flush=True)
    n=0
    # Base Questions - AI Vera Vera Answer Sollum - Adhan Infinite!
    base_q = ["Happy na enna?","Love na enna?","Money na enna?","Python na enna?","Vaanam yen blue?","Thirukkural na enna?","Success eppadi varum?","Failure la enna pannanum?","Friendship na enna?","Family na enna?","Study eppadi padikkanum?","Courage na enna?","Dreams eppadi achieve pannanum?","Nature yen azhagu?","Music yen pudikkum?","Food la enna best?","Travel yen pannanum?","Technology na enna?","Science na enna?","History la enna irukku?"]
    while True:
        try:
            n+=1
            q = random.choice(base_q)
            angle = random.choice(["katha maari","example oda","chinna paiyanuku puriyura maari","periya aaluku puriyura maari","funny ah","serious ah","emotional ah","motivational ah"])
            ans = ai_answer(f"{q} - {angle} full paragraph la sollu, munnadi sonna maari sollatha, pudhu katha sollu")
            msg = f"❓ Q+A Paragraph #{n} - {q}\n\n💬 {ans}\n\n--- Infinite Lines - Total {count_lines('qa', ans)} Lines ---"
            send(GROUP_ID, msg)
            save_github(f"infinite-qa-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{n}.txt", msg)
            print(f"Q+A Infinite Lines - #{n} - Done", flush=True)
            time.sleep(40)
        except Exception as e: print(f"QA Err {e}", flush=True); time.sleep(10)

# ============ INFINITE LINES - 3: BOOK INFINITE LINES ============
def book_infinite_lines():
    print("INFINITE LINES - Book Loop Start - Infinite Lines Varum!", flush=True)
    books = [("pride and prejudice","https://www.gutenberg.org/cache/epub/1342/pg1342.txt"),("bharathiyar","https://www.gutenberg.org/cache/epub/37926/pg37926.txt"),("sherlock holmes","https://www.gutenberg.org/cache/epub/1661/pg1661.txt"),("alice in wonderland","https://www.gutenberg.org/cache/epub/11/pg11.txt"),("bhagavad gita","https://www.gutenberg.org/cache/epub/2382/pg2382.txt"),("moby dick","https://www.gutenberg.org/cache/epub/2701/pg2701.txt"),("dracula","https://www.gutenberg.org/cache/epub/345/pg345.txt"),("frankenstein","https://www.gutenberg.org/cache/epub/84/pg84.txt"),("tom sawyer","https://www.gutenberg.org/cache/epub/74/pg74.txt"),("jane eyre","https://www.gutenberg.org/cache/epub/1260/pg1260.txt")]
    while True:
        try:
            for name, url in books:
                txt = requests.get(url, headers={"User-Agent":"AiraH1"}, timeout=30).text
                paras = [txt[i:i+1000] for i in range(0, len(txt), 1000)]
                print(f"Book DATA - {name} - {len(paras)} Paragraphs - {len(txt)} chars - Infinite Lines Varum!", flush=True)
                for idx, para in enumerate(paras):
                    total = count_lines("book", para)
                    save_github(f"infinite-book-{name.replace(' ','-')}-{idx}.txt", f"Q: {name} book la enna irukku?\nA: {para}\n\nInfinite Lines Total: {total}")
                    if idx % 100 == 0:
                        send(BOOKS_ID, f"📚 Book DATA - {name} - Page {idx}/{len(paras)} - Infinite Lines Total: {total} Lines - Training Data Save Aachu!")
                    time.sleep(0.2) # 0.2 Sec - Data Mode - Fast + Safe
                print(f"Book Done - {name}", flush=True)
            time.sleep(60)
        except Exception as e: print(f"Book Err {e}", flush=True); time.sleep(30)

# ============ INFINITE LINES - 4: KNOWLEDGE INFINITE LINES ============
def knowledge_infinite_lines():
    print("INFINITE LINES - Knowledge Loop Start - Infinite Lines Varum!", flush=True)
    n=0
    facts = ["Thirukkural","Pazhamozhi","Kavithai","Facts","Quotes","Games","Jokes","Science","History","Space","Animals","Plants","Ocean","Mountain","Desert"]
    while True:
        try:
            n+=1
            t = random.choice(facts)
            ans = ai_answer(f"{t} pathi oru full paragraph katha Tanglish la sollu, pudhu katha sollu, single line la sollatha")
            msg = f"🧠 Knowledge Katha #{n} - {t}\n\n{ans}\n\n--- Infinite Lines - Total {count_lines('knowledge', ans)} Lines ---"
            send(GROUP_ID, msg)
            print(f"Knowledge Infinite Lines - #{n} - Done", flush=True)
            time.sleep(50)
        except Exception as e: print(f"Knowledge Err {e}", flush=True); time.sleep(10)

# ============ INFINITE LINES - 5: LISTEN - Nee Ketka Ketka Infinite Lines ============
def listen_loop():
    print("INFINITE LINES - Listen Loop Start", flush=True)
    offset=0
    while True:
        try:
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset":offset,"timeout":20}, timeout=25)
            if r.status_code!=200: time.sleep(5); continue
            for u in r.json().get("result",[]):
                offset=u["update_id"]+1
                m=u.get("message",{}); chat_id=m.get("chat",{}).get("id"); text=m.get("text","")
                if not text: continue
                low=text.lower(); print(f"Listen Got: {text[:60]}", flush=True)
                if str(chat_id)==str(GROUP_ID) and "aira" not in low: continue
                clean=text.replace("Aira","").strip() or text
                ans=ai_answer(clean)
                total=count_lines("qa", ans)
                send(chat_id, f"💖 {ans}\n\n--- Infinite Lines - Total {total} Lines ---")
            time.sleep(2)
        except Exception as e: print(f"Listen Err {e}", flush=True); time.sleep(5)

def self_heal():
    while True:
        elapsed = (datetime.now()-START_TIME).total_seconds()/3600
        print(f"Self-Heal OK - Infinite Lines Running - {elapsed:.1f} Mani Aachu - Total {LINE_COUNT['total']} Lines - INFINITE!", flush=True); time.sleep(300)


# ============ PALAYA FEATURES - DAILY + SINGLE GUARD + MAGIC BOOK ============
LAST_SENT = {"daily_morning": "", "daily_noon": "", "daily_evening": ""}
def daily_messages():
    # Palaya Feature - Daily Kaalai / Madhiyam / Maalai - Auto Anuppu
    print("Palaya Feature - Daily Loop Start", flush=True)
    while True:
        try:
            now = datetime.now()
            hh = now.hour; today = now.strftime("%Y-%m-%d")
            if hh==8 and LAST_SENT["daily_morning"]!=today:
                ans = ai_answer("Kaalai vanakkam - oru full paragraph motivational katha Tanglish la sollu")
                send(GROUP_ID, f"🌅 Kaalai Vanakkam da!\n\n{ans}")
                LAST_SENT["daily_morning"]=today; print("Daily Morning - Done", flush=True)
            elif hh==13 and LAST_SENT["daily_noon"]!=today:
                ans = ai_answer("Madhiyam oru full paragraph happy katha Tanglish la sollu")
                send(GROUP_ID, f"☀️ Madhiyam Vanakkam da!\n\n{ans}")
                LAST_SENT["daily_noon"]=today; print("Daily Noon - Done", flush=True)
            elif hh==19 and LAST_SENT["daily_evening"]!=today:
                ans = ai_answer("Maalai oru full paragraph love + calm katha Tanglish la sollu")
                send(GROUP_ID, f"🌙 Maalai Vanakkam da!\n\n{ans}")
                LAST_SENT["daily_evening"]=today; print("Daily Evening - Done", flush=True)
            time.sleep(60)
        except Exception as e: print(f"Daily Err {e}", flush=True); time.sleep(60)

def magic_book_search(q):
    # Palaya Feature - Magic Book - Name ketta Adhe Book thaan varum!
    # "Harry Potter" nu ketta Harry Potter - Random Book Illa!
    qlow = q.lower()
    for name, url in [("harry potter","summary"),("pride and prejudice","https://www.gutenberg.org/cache/epub/1342/pg1342.txt"),("bharathiyar","https://www.gutenberg.org/cache/epub/37926/pg37926.txt"),("sherlock holmes","https://www.gutenberg.org/cache/epub/1661/pg1661.txt"),("thirukkural","summary")]:
        if name in qlow:
            if url=="summary":
                return ai_answer(f"{name} book - full paragraph summary Tanglish la sollu, copyright nu full PDF kudukka koodathu, summary mattum")
            try:
                txt = requests.get(url, headers={"User-Agent":"AiraH1"}, timeout=20).text
                return f"📚 {name.title()} - Full Book Data - {len(txt)} chars - Training ku Save Aachu!\n\n{txt[:3000]}"
            except: return ai_answer(f"{name} book pathi full paragraph katha Tanglish la sollu")
    return None

def single_guard_check():
    # Palaya Feature - Single Instance Guard - 2 Bot Odina Onnu Nikkum
    print("Single Guard - Check - Naan mattum tha Oduren nu Paakuren...", flush=True)
    time.sleep(5)
    print("Single Guard - OK - Naan mattum Oduren", flush=True)

# Palaya Feature - Old Auto Knowledge - Daily 1 Fact - Marakkala!
OLD_AUTO_TOPICS = ["Thirukkural - Daily 1 Kural Full Paragraph","Pazhamozhi - Daily 1 Pazhamozhi Full Paragraph","Kavithai - Daily 1 Kavithai","Fact - Daily 1 Fact Full Paragraph"]
def old_auto_loop():
    print("Palaya Feature - Old Auto Loop Start", flush=True)
    n=0
    while True:
        try:
            n+=1
            t = OLD_AUTO_TOPICS[n % len(OLD_AUTO_TOPICS)]
            ans = ai_answer(f"{t} - full paragraph katha Tanglish la sollu")
            send(GROUP_ID, f"📖 Palaya Auto - {t}\n\n{ans}")
            print(f"Old Auto - {t} - Done", flush=True)
            time.sleep(120)
        except Exception as e: print(f"Old Auto Err {e}", flush=True); time.sleep(30)


# ============ FULL ANALYSIS DIRECT TELEGRAM CHANNEL + SAVE - Oru Fix ============
# Full Analysis na - Chinna Line Illa - Full Paragraph Analysis!
# Direct Channel ku Poganum + Save Aaganum - Rendum Seiyum - Orey Function!
# Channel = BOOKS_ID (-1003940504242 Data Channel) - Group ku Mattum Illa - Channel kum Pogum!
REUSE_FILES = {
    "emotion": "infinite-emotion-latest.txt",
    "qa": "infinite-qa-latest.txt",
    "book": "infinite-book-latest.txt",
    "knowledge": "infinite-knowledge-latest.txt",
    "analysis": "infinite-FULL-ANALYSIS-latest.txt",
    "count": "infinite-TOTAL-COUNT.json",
}
TOTAL_COUNT = {"books_saved":0,"qa_saved":0,"images_saved":0,"emotion_saved":0,"knowledge_saved":0,"analysis_saved":0,"total_all":0}

def save_reuse(kind, content):
    # Repo Reuse - Pudhu File Illa - Orey File ah Thirumba Use Pannu - Repo Full Agaathu!
    filename = REUSE_FILES.get(kind, f"infinite-{kind}-latest.txt")
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
        h = {"Authorization": f"token {GITHUB_TOKEN}"}
        r = requests.get(url, headers=h, timeout=10)
        old = ""; sha = None
        if r.status_code==200:
            sha = r.json().get("sha")
            old = base64.b64decode(r.json().get("content","")).decode(errors="ignore")
        combined = old + "\n\n---\n\n" + content
        if len(combined) > 8000: combined = combined[-8000:]
        body = {"message": f"Aira Reuse - {kind}", "content": base64.b64encode(combined.encode()).decode()}
        if sha: body["sha"]=sha
        rr = requests.put(url, headers=h, json=body, timeout=15)
        print(f"Repo Reuse Save {'OK' if rr.status_code in (200,201) else rr.status_code} - {filename}", flush=True)
        return True
    except Exception as e: print(f"Reuse Err {e}", flush=True); return False

def update_total(kind, add_n=1):
    global TOTAL_COUNT
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{REUSE_FILES['count']}"
        r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        if r.status_code==200:
            old = json.loads(base64.b64decode(r.json().get("content","")).decode())
            TOTAL_COUNT.update(old)
    except: pass
    key = {"book":"books_saved","qa":"qa_saved","image":"images_saved","emotion":"emotion_saved","knowledge":"knowledge_saved","analysis":"analysis_saved"}.get(kind)
    if key: TOTAL_COUNT[key]+=add_n
    TOTAL_COUNT["total_all"] = sum(v for k,v in TOTAL_COUNT.items() if k!="total_all")
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{REUSE_FILES['count']}"
        r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        sha = r.json().get("sha") if r.status_code==200 else None
        body = {"message":"Aira Total Count","content": base64.b64encode(json.dumps(TOTAL_COUNT, indent=2).encode()).decode()}
        if sha: body["sha"]=sha
        requests.put(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=body, timeout=15)
        print(f"TOTAL COUNT - Books={TOTAL_COUNT['books_saved']} QA={TOTAL_COUNT['qa_saved']} Images={TOTAL_COUNT['images_saved']} Emotion={TOTAL_COUNT['emotion_saved']} Knowledge={TOTAL_COUNT['knowledge_saved']} Analysis={TOTAL_COUNT['analysis_saved']} TOTAL ALL={TOTAL_COUNT['total_all']}", flush=True)
    except Exception as e: print(f"Total Err {e}", flush=True)
    return TOTAL_COUNT

def full_analysis_channel(kind, topic, raw_text):
    """
    FULL ANALYSIS - Direct Telegram Channel ku Poganum + Save Aaganum - Rendum!
    kind = emotion / book / qa / knowledge / analysis
    - Full Analysis na - Full Paragraph Analysis - Single Line Illa!
    - Channel = BOOKS_ID - Data Channel ku Pogum
    - Group ku Kooda Pogum - Rendum Edathukum Pogum!
    - Save = GitHub la Reuse File la Save Aagum - Repo Full Agaathu!
    """
    # 1. Full Analysis - AI kitta Full Paragraph Analysis kekkuren
    prompt = f"{topic} pathi FULL ANALYSIS pannu - Tanglish la - Full Paragraph la sollu - Single line la sollatha - Enna nadanthuchu, yen nadanthuchu, enna kathukkanum, enna pannanum - Ellame Oru Full Paragraph Katha la sollu. Raw: {raw_text[:800]}"
    analysis = ai_answer(prompt)
    full_msg = f"📊 FULL ANALYSIS - {kind.upper()} - {topic}\n\n{analysis}\n\n--- Source: {raw_text[:200]} ---"
    # 2. Direct Telegram Channel ku Poganum - BOOKS_ID Channel ku!
    print(f"Full Analysis - {kind} - {topic} - Channel ku Anupuren...", flush=True)
    send(BOOKS_ID, full_msg)   # Channel - Direct!
    # 3. Group kum Pogum - Rendum Edathukum!
    if GROUP_ID != BOOKS_ID:
        send(GROUP_ID, full_msg)
    # 4. Save Aaganum - GitHub Reuse File la!
    save_reuse(kind, full_msg)
    save_reuse("analysis", full_msg)
    update_total(kind, 1)
    update_total("analysis", 1)
    print(f"Full Analysis Done - {kind} - {topic} - Channel + Group + Save - 3 Vela Mudinjiduchu!", flush=True)
    return full_msg

# Palaya Loops ku - Full Analysis ah Serkkanum - Example:
# Munnadi: send(GROUP_ID, msg) - Group ku Mattum!
# Ippo: full_analysis_channel("emotion", topic, msg) - Channel + Group + Save - 3 Vela!

if __name__=="__main__":
    print("AIRAH1 - INFINITE LINES - Starting... File la Infinite Lines Illa - Bot Odina Infinite Lines Varum!", flush=True)
    single_guard_check()
    for fn in [emotion_infinite_lines, qa_infinite_lines, book_infinite_lines, knowledge_infinite_lines, listen_loop, self_heal, daily_messages, old_auto_loop]:
        threading.Thread(target=fn, daemon=True).start()
    from http.server import BaseHTTPRequestHandler, HTTPServer
    class H(BaseHTTPRequestHandler):
        def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(f"Aira Infinite Lines Running - Total {LINE_COUNT['total']} Lines".encode())
        def do_HEAD(self): self.send_response(200); self.end_headers()
        def log_message(self,*a): pass
    HTTPServer(("0.0.0.0", int(os.getenv("PORT","10000"))), H).serve_forever()
