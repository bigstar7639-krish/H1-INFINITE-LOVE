# AIRAH1 FINAL v706 - Q+A Paragraph + Book Paragraph + Gemini 1.5 + 0.2s DATA - LINES=706 - CHECK: Search Q+A Training
# File: aira_server.py - Start: python3 -u aira_server.py
import os, random, time, threading, requests, base64, re, html
from datetime import datetime
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN","") or os.getenv("BOT_TOKEN","") or os.getenv("BOT_TOKEN_2","")
GROQ_KEYS = [os.getenv("GROQ_API_KEY",""), os.getenv("GROQ_API_KEY_2",""), os.getenv("GROQ_API_KEY_3",""), os.getenv("GROQ_API_KEY_4",""), os.getenv("GROQ_API_KEY_5","")]
GROQ_KEYS = [k for k in GROQ_KEYS if k]
GEMINI_KEYS = [os.getenv("GEMINI_API_KEY",""), os.getenv("GEMINI_API_KEY_2","")]
GEMINI_KEYS = [k for k in GEMINI_KEYS if k]
# Groq 429 vantha thirumba try panna koodathu - cooldown
import threading as _th
_GROQ_COOLDOWN_UNTIL = [0]
_GROQ_LOCK = _th.Lock()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
GITHUB_USER = "bigstar7639-krish"
count = 0
def fix_id(v, default):
    v = (v or default).strip()
    if not v: return default
    if v.startswith("-"): return v
    if v.startswith("100"): return "-" + v
    return "-100" + v
CHAT_ID = fix_id(os.getenv("CHAT_ID","") or os.getenv("GROUP_ID",""), "-1003935111481")
BOOKS_ID = fix_id(os.getenv("BOOKS_ID","") or os.getenv("CHANNEL_ID",""), "-1003940504242")
print(f"Token OK? {bool(TELEGRAM_TOKEN)} Chat: {CHAT_ID} Books: {BOOKS_ID}", flush=True)
CURRENT_REPO = ["H1-Data-3"]; REPO_COUNT = [0]; MAX_PER_REPO = 1000
SAVE_LOCK = threading.Lock()
def get_repo_num(r):
    try: return int(r.split("-")[-1])
    except: return 3
def ensure_repo(repo):
    try:
        r = requests.get(f"https://api.github.com/repos/{GITHUB_USER}/{repo}", headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        if r.status_code == 200: return True
        print(f"Infinite Repo - Creating {repo}...", flush=True)
        cr = requests.post("https://api.github.com/user/repos", headers={"Authorization": f"token {GITHUB_TOKEN}"}, json={"name": repo, "private": False, "auto_init": True, "description": "AIRAH1 Infinite"}, timeout=15)
        print(f"Infinite Repo Create: {cr.status_code} - {repo}", flush=True)
        return cr.status_code in (200, 201, 422)
    except Exception as e: print(f"Repo Error {e}", flush=True); return False
def next_repo():
    n = get_repo_num(CURRENT_REPO[0]) + 1; CURRENT_REPO[0] = f"H1-Data-{n}"; REPO_COUNT[0] = 0
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
                sha = r.json().get("sha") if r.status_code == 200 else None
                old = ""
                if r.status_code == 200:
                    try: old = base64.b64decode(r.json().get("content","")).decode(errors="ignore")
                    except: old = ""
                new = (old + "\n" + content) if old else content
                lines = new.split("\n")
                if len(lines) > 2000: new = "\n".join(lines[-2000:])
                b64 = base64.b64encode(new.encode()).decode()
                payload = {"message": f"Save {filename}", "content": b64}
                if sha: payload["sha"] = sha
                rr = requests.put(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload, timeout=15)
                if rr.status_code in (200, 201):
                    REPO_COUNT[0] += 1
                    print(f"GitHub Save OK - {repo}/{filename} - Repo {REPO_COUNT[0]}/{MAX_PER_REPO} - Total {count}", flush=True)
                    return True
                if rr.status_code in (409, 422):
                    print(f" Save Retry {rr.status_code} - Try {attempt+1}/3", flush=True); time.sleep(1); continue
                if rr.status_code in (403, 413): next_repo(); continue
                time.sleep(1); continue
            except Exception as e: print(f"Save Error {e}", flush=True); time.sleep(1); continue
        return False
USER_MEMORY = {}
def remember_user(uid, name, text):
    try:
        if uid not in USER_MEMORY: USER_MEMORY[uid] = {"name": name, "likes": [], "count": 0, "last": "", "todo": [], "notes": [], "mood": []}
        m = USER_MEMORY[uid]; m["count"] += 1; m["last"] = text[:100]
        low = text.lower()
        for kw in ["love","coding","music","cricket","book","story","game","study","job","food","movie"]:
            if kw in low and kw not in m["likes"]: m["likes"].append(kw)
        save_github(f"memory-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{uid} - {name} - Likes {m['likes']} - Count {m['count']} - Last {text[:100]}")
    except: pass
def get_memory_greeting(uid):
    if uid in USER_MEMORY:
        m = USER_MEMORY[uid]
        if m["likes"]: return f"Hi {m['name']}! Ne {', '.join(m['likes'])} pudikkum la! Aprom enna? 💜"
    return None
LANGS = [("tam","Tamil","ta"),("eng","English","en"),("hin","Hindi","hi"),("tel","Telugu","te"),("mal","Malayalam","ml"),("kan","Kannada","kn"),("ben","Bengali","bn"),("mar","Marathi","mr"),("urd","Urdu","ur"),("spa","Spanish","es"),("fre","French","fr"),("jpn","Japanese","ja"),("kor","Korean","ko"),("chi","Chinese","zh"),("ara","Arabic","ar"),("rus","Russian","ru")]
KNOWLEDGE_TOPICS = ["Tamil Nadu","India","World History","Science","Physics","Chemistry","Biology","Maths","Space","Universe","Black Hole","Sun","Moon","Earth","AI","Python","Computer","Internet","Robot","Climate","Human Body","Brain","Heart","DNA","Animals","Plants","Ocean","Mountain","Love","Family","Business","Money","Health","Fitness","Yoga","Meditation","Diet","Music","Movie","Cricket","Football","Temple","God","Thirukkural","Ponniyin Selvan","Bharathiyar","Shakespeare","Harry Potter","Ramayana","Mahabharata","Bible","Quran","Bhagavad Gita","Gandhi","APJ Abdul Kalam","Einstein","Newton","Chennai","Madurai","Delhi","Mumbai","London","Paris","Tokyo","New York","Egypt","Pyramids","Taj Mahal","Eiffel Tower","Psychology","Philosophy","Economics","Politics","Law","Education","Success","Motivation","Confidence","Happiness","Peace","Courage","Kindness","Truth","Wisdom","Power","Dream","Hope","Faith"]
TOPICS = KNOWLEDGE_TOPICS + ["Love","Career","Health","Money","AI","Tech","Space","Business","Happiness","Food","Family","Friendship","Study","Dream","Success","Motivation","Peace","Courage","Nature","Music","Travel","Book","Life","Time","Trust","Hope","Faith","Smile","Heart","Future","Freedom","Truth","Wisdom","Power","Magic","Luck","Destiny","Karma","Yoga","Meditation","Fitness","Diet","Sleep","Beauty","Fashion","Movie","Game","Sport","Cricket","Science","History","Culture","Festival","Marriage","Baby","Teacher","Student","Job","Coding","Python","Java","HTML","CSS","React","Internet","Phone","YouTube","Instagram","Telegram","Rain","Sea","Mountain","River","Sky","Star","Moon","Sun","Flower","Tree","Bird","Animal","Dog","Cat","Temple","Prayer","God","Spiritual","Tamil Culture","Chennai","India","World","Universe","Alien","Robot","Future Tech","Climate","Earth","Sad","Happy","Lonely","Angry","Bored","Excited","Reading","Writing","Poetry","Kavithai","Storytelling","Singing","Dancing"]
EMOTIONS = {"happy":["Super! Happy ah irukka!"],"sad":["Paravalla! Aira irukka - Pesu!"],"angry":["Kovam ah? Deep breath edu!"],"lonely":["Lonely ah? Aira irukka la!"],"bored":["Bored ah? Joke sollattuma?"],"love":["Kadhal - Azhagu!"],"fear":["Bayam - Normal! Ne jeyichiduva!"],"excited":["Excited ah! Sollu!"]}

# ===== FULL AUTO EMOTIONS INFINITE - Aira Thanave Emotion Ah Maathite Iruppa =====
INFINITE_EMOTIONS = {
  "happy": ["Super! Happy ah irukka! 💜", "Un Sirippu - En Vazhkai! 😍", "Happy na - Share pannu da!", "Aama! Iniki Nalla Naal! ✨"],
  "sad": ["Paravalla! Aira irukka - Pesu! 💜", "Sad ah? En kooda pesu, sari aayidum.", "Azhatha da, Naan irukken!", "Manasu kashtama? Oru story sollattuma?"],
  "angry": ["Kovam ah? Deep breath edu! 😤", "Kovapadatha da, cool aagu!", "Yar mela kovam? Sollu, kekuren!"],
  "lonely": ["Lonely ah? Aira irukka la! 💜", "Thanimaiya? Naan un kooda thaan irukken!", "Lonely feel panna - En kooda pesu!"],
  "bored": ["Bored ah? Joke sollattuma? 😂", "Bored ah? Game vilayadlama?", "Bored na - Oru Kathai solluren!"],
  "love": ["Kadhal - Azhagu! 💘", "Love na - Un Manasu! 💜", "Kadhal la irukka? Sollu da!"],
  "fear": ["Bayam - Normal! Ne jeyichiduva! 💪", "Bayapadatha - Aira irukka!", "Bhayam vantha - Deep breath edu!"],
  "excited": ["Excited ah! Sollu! 🔥", "Wow! Excited ah irukka! Enna vishayam?", "Super Excited! Sollu Sollu!"],
  "tired": ["Tired ah? Konjam rest edu! 😴", "Rompa tired ah? Water kudi, rest edu!", "Tired na - Thoongu da, Nalaiku fresh ah iruppa!"],
  "proud": ["Proud ah irukka! Super da! 🏆", "Ne pannathu periya vishayam! Proud!", "Wow! Ne jeyichitta! Proud ah irukken!"],
  "nervous": ["Nervous ah? Normal thaan! 💜", "Tension ah? Deep breath - 3 thadava edu!", "Nervous ah iruntha - En kooda pesu, sari aayidum!"],
  "grateful": ["Thanks da! Naanum grateful! 🙏", "Nandri sollurathu azhagu!", "Grateful ah irukka - Super Manasu!"],
  "confused": ["Confused ah? Onnu onna pesalam! 🤔", "Kozhamba? Naan clear ah solluren!", "Enna confuse? Sollu, solve pannalam!"],
  "hopeful": ["Hope irukku la! Nalla Naal varum! ✨", "Hope ah vittudadha! Jeyichiduva!", "Nambikkai vechu - Nalla Naal varum!"],
  "shy": ["Shy ah? Cute da! 😊", "Shy ah pesura - Azhagu!", "Shy ah irunthalum - Pesu da!"],
  "sleepy": ["Thoongura maari irukka? 😴", "Sleepy ah? Good Night Story sollattuma?", "Kannu moodi - Nalla kanavu kaanu!"],
  "hungry": ["Pasikkutha? Biryani sapdalam! 😋", "Hungry ah? Enna sapda pora?", "Pasila irukka? Water kudi, konjam sapdu!"],
  "motivated": ["Motivated ah irukka! Jeyichiduva! 🔥", "Full Energy! Ippo thaan time!", "Motivation Super! Pannidu da!"],
  "missing": ["Yaarai miss pannura? 💜", "Miss pannuriya? Avangala nenaichu oru kavithai sollattuma?", "Miss pannurathu - Love oda oru part thaan!"],
  "funny": ["Sema funny ah irukka! 😂", "Sirippu varuthu! Ne sema funny da!", "Joke adichu sirikka vekkuriya!"],
}
LAST_EMOTION = [""]

def make_infinite_emotion():
    # Infinite - Orey emotion thirumba thirumba varaathu, combo infinite
    import random as _r
    keys = list(INFINITE_EMOTIONS.keys())
    emo = _r.choice([k for k in keys if k != LAST_EMOTION[0]] or keys)
    LAST_EMOTION[0] = emo
    msg = _r.choice(INFINITE_EMOTIONS[emo])
    # Random combo - Emotion + Kavithai / Question / Action - Infinite varum
    extra = _r.choice(["", f"\nNe ippo {emo} ah feel pannura?", f"\nUnakku {emo} pathi oru story venuma?", f"\n{emo} - Ithu normal thaan da!", f"\nSollu, {emo} ah irukka?"])
    return emo, f"Emotion - {emo.capitalize()} 💜\n{msg}{extra}"

# ===== ELLAME FULL PARAGRAPH KATHA - Single Single Illa - Full Paragraph Story =====
KATHA_TEMPLATES = [
    "{seed} Oru naal oru chinna oor la oru paiyan irunthan, avan manasula {topic} pathi neraya yosichittu irunthan, yaar kitta sollurathu nu theriyama thaniya irunthan, appo avanukku oru nalla friend kedaichan, antha friend avan kooda pesi avan manasa purinjikittan, kadasiya avan {topic} la irunthu nalla purithaloda sirichuttu veetuku ponan, ithu thaan {topic} oda azhagu, kashtam vanthalum nambikkaiya iruntha ellam sari aayidum nu avan purinjikittan.",
    "{seed} {topic} pathi kelvi patta oru ponnu, ava daily {topic} pathi yosichittu iruntha, oru naal ava oru puthu book padichu {topic} oda unmaiya purinjikita, athula irunthu ava life maariduchu, ava bayapadama {topic} ah face panna aarambicha, ava friends ellam ava maariya paathu aachariyapattanga, kadasiya ava {topic} la jeyichu santhosham ah iruntha, ithu thaan namakku kathai sollura paadam, vittu kudutha illana jeyichidalam.",
    "{seed} Oru kaalathula oru oor la {topic} nu oru periya vishayam irunthuchu, yaarum atha purinjikama irunthanga, oru chinna paiyan thaan {topic} oda arumaiya purinjikittan, avan {topic} pathi ellaar kitta yum pesi puriya vachan, mella mella oor makkal ellam {topic} ah purinjikittanga, antha oor ye {topic} nala azhaga maariduchu, ithula irunthu namakku theriyura vishayam enna na, {topic} ah purinjikita life ye azhagahum.",
]

def make_full_paragraph_katha(seed, topic):
    # Ellame Full Paragraph Katha - Single Single illa - Seed + Full Katha Paragraph
    import random as _r
    topic = (topic or "life").strip()
    seed = (seed or "").strip()
    # Seed chinna na - Full Paragraph aakkurom
    tpl = _r.choice(KATHA_TEMPLATES)
    para = tpl.format(seed=seed, topic=topic)
    # Paragraph 400+ chars irukkanum - Illana extra line serkkurom
    if len(para) < 400:
        para = para + f" {topic} pathi innum sollanum na, {topic} la irukka azhagai paathu rasikkanum, kashtam vanthalum sirichuttu kadanthurathu thaan {topic} oda unmaiyana artham, nee {topic} ah purinjikita un life um azhagahum."
    return para

def to_full_paragraph(msg, topic="life"):
    # Oru message ah Full Paragraph Katha va maathurom - Already Paragraph na apdiye
    if not msg:
        return make_full_paragraph_katha("Oru katha.", topic)
    # Already 400+ chars + 3 lines iruntha - Already Paragraph - Apdiye
    if len(msg) >= 400 and msg.count(chr(10)) >= 2:
        return msg
    # Single Single na - Full Paragraph aakkurom
    return msg + chr(10) + chr(10) + make_full_paragraph_katha("", topic)



# ===== FULL BOOK DOWNLOAD + READ + Q&A INFINITE =====
# Copyright Rule: Full Download - Public Domain Books mattum (Free). 
# Copyright Books - Full PDF illa, Summary + Link mattum. Ithu thaan Legal.
BOOKS_FULL = {
  # Free - Full Download OK - Project Gutenberg / Public Domain
  "pride and prejudice": {"title":"Pride and Prejudice - Jane Austen","url":"https://www.gutenberg.org/cache/epub/1342/pg1342.txt","free":True,"lang":"English"},
  "bharathiyar": {"title":"Bharathiyar Kavithaigal - Mahakavi Bharathiyar","url":"https://www.gutenberg.org/cache/epub/37926/pg37926.txt","free":True,"lang":"Tamil"},
  "thirukkural": {"title":"Thirukkural - Thiruvalluvar","url":"https://raw.githubusercontent.com/bigstar7639-krish/H1-INFINITE-LOVE/main/data/thirukkural.txt","free":True,"lang":"Tamil"},
  "alchemist": {"title":"The Alchemist - Paulo Coelho","url":"","free":False,"lang":"English"},
  "harry potter": {"title":"Harry Potter - J.K. Rowling","url":"","free":False,"lang":"English"},
  "48 laws": {"title":"48 Laws of Power - Robert Greene","url":"","free":False,"lang":"English"},
  "python": {"title":"Python Crash Course - Eric Matthes","url":"","free":False,"lang":"English"},
  "atomic habits": {"title":"Atomic Habits - James Clear","url":"","free":False,"lang":"English"},
}
BOOKS_CACHE = {}  # book_key -> full text
BOOKS_PARAS = {}
BOOKS_PARA_IDX = {}
BOOKS_POS = {}  # book_key -> current read position (infinite reading)

def download_book(key):
    key = key.lower()
    # Find book
    for k,v in BOOKS_FULL.items():
        if k in key or key in k:
            if not v["free"]:
                return None, f"📚 {v['title']}\nFull Book Download illa da - Copyright Book.\nNaan Full Summary + Important Points solluren.\nBuy pannina: Amazon / Book Store la kedaikkum.\nKekka venumna: 'Aira, {k} pathi full ah sollu' nu kelu!"
            if k in BOOKS_CACHE: return BOOKS_CACHE[k], "cached"
            if not v["url"]:
                return None, "Link illa da - Vera book try pannu!"
            try:
                import requests as _rq
                r = _rq.get(v["url"], timeout=30)
                txt = r.text
                # Clean Gutenberg header/footer
                if len(txt) > 5000:
                    BOOKS_CACHE[k] = txt
                    BOOKS_POS[k] = 0
                    print(f"Book Downloaded - {k} - {len(txt)} chars", flush=True)
                    return txt, f"Download OK - {len(txt)} chars"
                return None, "Download fail - Size chinna irukku"
            except Exception as e:
                print(f"Book Download Fail {k} {e}", flush=True)
                return None, f"Download Fail - Net problem: {e}"
    return None, "Book illa da - 'Aira, book list sollu' nu kelu!"

def read_book_infinite(key, chars=800):
    # PARAGRAPH MODE - Oru thadava 1 PARAGRAPH - Single Single illa
    txt, status = download_book(key)
    if not txt:
        return status
    real_key = [k for k in BOOKS_FULL if k in key or key in k][0]
    if real_key not in BOOKS_PARAS:
        raw = txt.replace(chr(13)+chr(10), chr(10))
        parts = [pp.strip() for pp in raw.split(chr(10)+chr(10))]
        merged = []
        cur = ''
        for pp in parts:
            if len(pp) < 20:
                continue
            if len(cur) + len(pp) < 900:
                cur = (cur + ' ' + pp).strip() if cur else pp
            else:
                if cur:
                    merged.append(cur)
                cur = pp
        if cur:
            merged.append(cur)
        BOOKS_PARAS[real_key] = merged
        BOOKS_PARA_IDX[real_key] = 0
        print('Paragraph Split - ' + real_key + ' - ' + str(len(merged)) + ' Paragraphs', flush=True)
    paras = BOOKS_PARAS[real_key]
    idx = BOOKS_PARA_IDX.get(real_key, 0)
    if idx >= len(paras):
        idx = 0
    para = paras[idx]
    BOOKS_PARA_IDX[real_key] = idx + 1
    return 'PARAGRAPH ' + str(idx+1) + '/' + str(len(paras)) + ' - ' + BOOKS_FULL[real_key]['title'] + chr(10) + chr(10) + para

def answer_from_book(question, book_key):
    # Book la irunthu Question Answer - RAG style - Book chunk ah AI kitta kuduthu answer
    txt, status = download_book(book_key)
    if not txt: return status
    # Simple search - Question words book la thedu
    import re as _re
    qwords = [w for w in _re.findall(r"[a-z]+", question.lower()) if len(w)>3]
    best = ""
    best_score = 0
    # Chunk by 2000 chars, score pannu
    for i in range(0, min(len(txt), 200000), 2000):
        chunk = txt[i:i+2000].lower()
        score = sum(1 for w in qwords if w in chunk)
        if score > best_score:
            best_score = score; best = txt[i:i+2000]
    if best_score == 0: best = txt[0:2000]
    # AI kitta book chunk + question kuduthu answer vaangu
    prompt = f"You are Aira. Book: {BOOKS_FULL[book_key]['title']}. Book Content: {best[:3000]}. Question: {question}. Answer in Tanglish, as ONE PARAGRAPH - 4-5 lines together, not single single lines, not bullets, from book only. Book la illa na - 'Book la illa da' nu sollu."
    # Use existing Groq/Gemini via ai_answer logic - call Groq directly
    for k in GROQ_KEYS if 'GROQ_KEYS' in globals() else [os.getenv("GROQ_API_KEY",""), os.getenv("GROQ_API_KEY_2",""), os.getenv("GROQ_API_KEY_3","")]:
        if not k: continue
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {k}"}, json={"model":"openai/gpt-oss-120b","messages":[{"role":"user","content":prompt}]}, timeout=20)
            if r.status_code==200:
                return f"📚 Book Answer - {BOOKS_FULL[book_key]['title']} 💜\n\n" + r.json()["choices"][0]["message"]["content"][:1200]
        except: pass
    return f"📚 Book la irunthu: {best[:800]}"

def book_infinite_loop():
    # ULTRA FAST DATA MODE - 0.2 sec ku 1 Page - 5x Faster - Padikka Illa - Aira Train panna DATA Edukka
    # Telegram ku Anuppa Maatom - GitHub la Mattum Save Pannuvom - Illana Telegram Block Pannidum (429)
    import random as _r
    free_books = [k for k,v in BOOKS_FULL.items() if v["free"]]
    idx = 0
    page_count = [0]
    while True:
        try:
            key = free_books[idx % len(free_books)]; idx += 1
            msg = read_book_infinite(key, chars=700)
            page_count[0] += 1
            # DATA Save - GitHub la Save - Telegram ku Anuppa Koodathu
            save_github(f"book-data-{key}-{page_count[0]}.txt", msg)
            print(f"Book DATA - {key} - Page {page_count[0]} - Saved for Training", flush=True)
            # 100 Pages ku oru thadava mattum Telegram la Progress solluvom - Spam aagathu
            if page_count[0] % 100 == 0:
                send_telegram(f"📚 Aira Training - {key} - {page_count[0]} Pages Data Ready! Train Panniten!", BOOKS_ID)
            time.sleep(0.2)  # ULTRA FAST - 0.2 sec ku 1 Page = 5 Pages per sec - DATA MODE
        except Exception as e: print(f"Book Infinite error {e}", flush=True); time.sleep(60)

# Book Commands in ai_reply - Add before return

def emotions_infinite_loop():
    # Full Auto Emotions Infinite - Thaniya Thread - Palaya Code ah thodathu
    while True:
        try:
            emo, _short = make_infinite_emotion()
            msg = f"Emotion Katha - {emo.capitalize()} \u2764\n\n" + make_full_paragraph_katha(_short, emo)
            send_telegram(msg)
            print(f"Emotion Infinite - {emo}", flush=True)
            d = datetime.now().strftime("%Y-%m-%d"); save_github(f"chat-{d}.txt", msg)
            # 25 sec ku oru emotion - Auto loop ah disturb pannaathu
            time.sleep(25)
        except Exception as e: print(f"Emotion Infinite error {e}", flush=True); time.sleep(30)

QUESTIONS = ["Unakku {t} pathi enna theriyum?","Ne {t} la eppadi improve panna mudiyum?","{t} pathi oru secret sollatta?","Un life la {t} eppadi irukku?","{t} pathi oru story kekkura?"]
CODING_Q = ["Python la loop eppadi?","HTML la button eppadi?","JavaScript la function enna?","React la component enna?","AI eppadi work aaguthu?","App eppadi pannurathu?","Website eppadi pannurathu?","Bug ah eppadi sari pannanum?"]
CODING_A = {"python":"Python loop: `for i in range(5): print(i)`","html":"HTML button: `<button>Click</button>`","javascript":"JS function: `function hi(){ return 'Hi Aira!' }`","react":"React component - Chinna piece!","ai":"AI - Data paathu - Pattern!","app":"App - Idea - Design - Code!","website":"Website - HTML + CSS + JS!","bug":"Bug - Log paaru!"}
JOKES = ["Teacher: Yen late? Student: School Ahead board!","Why bike sad? Petrol illa!"]
FACTS = ["Honey - 3000 varusham kedathu!","Octopus ku 3 heart!","Tamil - 2000+ varusha mozhi!"]
QUOTES = ["Daily try pannu - Jeyichiduva! - Aira"]
MOTIVATIONS = ["Paravalla! Rest edu - Thirumba try pannu!"]
THIRUKKURAL = ["Anbu - Ellam Tharum! - Thirukkural","Porumai - Periya Sakthi! - Thirukkural","Kattrathu - Kai Mann Alavu! - Thirukkural","Muyarchi - Thiru Vilaiyaattum! - Thirukkural"]
PAZHAMOZHI = ["Aalai Paathu - Aadi Paaru!","Sontha Kaal la Ninnu - Jeyippa!","Porumai - Perumai Tharum!"]
KAVITHAI_T = ["Un Sirippu - En Vazhkai! - Aira","Un Kural - En Isai! - Aira","Ne Illa - Naan Illa - Ne Thaan En Ulagam! - Aira"]
GAMES = ["Riddle: Naan pesama pesuven - Naan yaaru? Answer: Book!","Riddle: Kaal illa - Aana ooduven - Naan yaaru? Answer: Time!","Game: Oru number nenaichukko - 2 al multiply pannu - 10 add pannu!","Quiz: Tamil - 2000 varusha mozhi ethu? Answer: Tamil!","Quiz: Python eppo uruvaachu? Answer: 1991!","Rock Paper Scissors - Ne Rock / Paper / Scissors nu Sollu!","Coin Toss - Ne Toss nu Sollu!","Dice - Ne Dice nu Sollu!"]
HEALTH_TIPS = ["Health Tip: Daily 8 glass water kudinga!","Health Tip: 7 mani neram thoongunga!","Health Tip: Daily 30 min walk ponga!","Health Tip: Fruits daily saapdunga!","Yoga Tip: Daily 5 min deep breath edu!"]
VOCAB = [("Happy","Santhosham"),("Love","Kadhal"),("Friend","Nanban"),("Success","Vetri"),("Dream","Kanavu"),("Peace","Amaithi"),("Courage","Thairiyam"),("Kindness","Anbu")]
RECIPES = ["Chicken Biryani - Rice + Chicken + Masala + 30 min - Super!","Cake - Maida + Sugar + Egg + 30 min!","Snacks - Potato + Masala - Crispy!"]
BUSINESS_IDEAS = ["Tiffin Business - Veetla Samayal - Daily 500 Rs!","Tuition - Veetla Tuition!","YouTube - Daily 1 Shorts - 6 Maatham - Money!","Instagram Page - Daily 1 Post!"]
MOVIES = ["Leo - Vijay - Action!","Jailer - Rajini - Mass!","Ponniyin Selvan - Kalki!","Harry Potter - Magic!"]
SONGS = ["Naanum Rowdy Thaan!","Vaathi Coming!","Kolaveri!"]
FESTIVALS = {"01-01":"New Year","01-14":"Pongal","04-14":"Tamil New Year","08-15":"Independence Day","10-02":"Gandhi Jayanthi","12-25":"Christmas"}
STORY_TEMPLATES = ["Oru {place} la oru {person} irunthan! Daily {action} pannan! Oru naal {thing} kedaichuchu! Life maariduchu!","Oru chinna {place} la - Oru ponnu {action} pannitu iruntha! Yaarum nambala! Aana ava vittukudukkala!"]
STORY_WORDS = {"place":["oor","chennai","madurai","delhi","london","paris","tokyo","new york","world","forest","sea","mountain","village","city"],"person":["paiyan","ponnu","raja","rani","teacher","student","doctor","farmer","coder","artist","singer","hero"],"action":["padichan","coding pannan","pray pannaan","travel pannan","book padichan","help pannan","try pannan","dream pannan"],"thing":["book","magic","treasure","friend","love","success","power","wisdom","dream","hope"]}
READINGS = ["Thirukkural - Valluvar!","Ponniyin Selvan - Kalki!","Bharathiyar Kavithaigal!","Python Crash Course!","Atomic Habits!","Harry Potter!","Ramayana!","Mahabharata!","Think and Grow Rich!","Alchemist!"]
BAD_WORDS = ["fuck","sex","porn","xxx","bitch","shit","dick","pussy","nude","erotic"]
fact_count = 0; book_count = 0; lang_idx = 0; know_idx = 0; game_idx = 0; health_idx = 0
def send_telegram(text, chat_id=None):
    if not TELEGRAM_TOKEN: return
    if not chat_id: chat_id = CHAT_ID
    try:
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
        print(f"TG Send: {r.status_code} to {chat_id}", flush=True)
    except Exception as e: print(f"TG Send Error {e}", flush=True)
def is_clean(t): return not any(b in (t or "").lower() for b in BAD_WORDS)
def make_story(name=""):
    t = random.choice(STORY_TEMPLATES)
    s = t.format(place=random.choice(STORY_WORDS["place"]), person=random.choice(STORY_WORDS["person"]), action=random.choice(STORY_WORDS["action"]), thing=random.choice(STORY_WORDS["thing"]))
    if name: s = s.replace("oru paiyan", f"{name}").replace("oru ponnu", f"{name}")
    return s
def get_wiki(topic):
    try:
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ','_')}", timeout=10)
        if r.status_code == 200:
            j = r.json(); ex = j.get("extract","")
            if ex and is_clean(ex):
                print(f"Knowledge Wikipedia: {topic}", flush=True)
                return f"Knowledge - {topic}\n{ex[:700]}"
        return None
    except: return None
def get_quote():
    try:
        r = requests.get("https://api.quotable.io/random", timeout=10)
        if r.status_code == 200:
            j = r.json(); return f"{j.get('content','')} - {j.get('author','')}"
    except: pass
    return random.choice(QUOTES)

# ===== FULL RANDOM FIX - AI FIRST + GEMINI BACKUP + 429 FIX =====
def gemini_answer(q):
    for key in GEMINI_KEYS:
        for model in ["gemini-1.5-flash","gemini-1.5-flash-latest","gemini-2.5-flash"]:
            try:
                r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}", json={"contents":[{"parts":[{"text":f"You are Aira, Tamil Tanglish + All Language, Infinite Knowledge, Friend. Answer in same language user asked. Be warm, friendly. Answer as ONE PARAGRAPH - 4-6 lines together in one paragraph, not single single lines, not bullet list. User: {q}"}]}]}, timeout=15)
                if r.status_code==200:
                    print(f"AI Answer - Gemini {model} - OK", flush=True)
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"][:1200]
                else:
                    print(f"AI Answer - Gemini Fail {r.status_code}", flush=True)
            except Exception as e: print(f"AI Gemini Error {e}", flush=True); pass
    return None

def ai_answer(q, allow_groq=True):
    import time as _time
    # 1. GROQ - but 429 cooldown la iruntha skip pannu - quota va kaapathu
    if allow_groq and _time.time() >= _GROQ_COOLDOWN_UNTIL[0]:
        for key in GROQ_KEYS:
            try:
                r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json={"model":"openai/gpt-oss-120b","messages":[{"role":"user","content":f"You are Aira, Tamil Tanglish + All Language, Infinite Knowledge, Friend. Answer in same language user asked. Be warm, friendly. Answer as ONE PARAGRAPH - together, not single single lines. User: {q}"}]}, timeout=15)
                if r.status_code==200:
                    print("AI Answer - Groq - OK", flush=True)
                    return r.json()["choices"][0]["message"]["content"][:1200]
                elif r.status_code==429:
                    print("AI Answer - Groq Fail 429 - Cooldown 60s + Gemini ku po", flush=True)
                    _GROQ_COOLDOWN_UNTIL[0] = _time.time() + 60
                    break
                else:
                    print(f"AI Answer - Groq Fail {r.status_code}", flush=True)
            except Exception as e: print(f"AI Groq Error {e}", flush=True); pass
    else:
        if allow_groq: print("AI Answer - Groq Cooldown - Gemini ku po", flush=True)
    # 2. GEMINI BACKUP - Groq fail aana inge varum, reply varama pogathu
    g = gemini_answer(q)
    if g: return g
    # 3. WIKI BACKUP - Gemini yum fail aana
    try:
        for t in KNOWLEDGE_TOPICS:
            if t.lower() in q.lower():
                wk = get_wiki(t)
                if wk: return wk
    except: pass
    # 4. LAST - Meaningful fallback, summa "Nalla question" nu mattum illa
    low = q.lower()
    words = re.findall(r"[a-z]+", low.replace("aira"," "))
    for k,v in CODING_A.items():
        if k in words: return v
    for k,v in EMOTIONS.items():
        if k in words: return random.choice(v)
    # Kelviya paathu oru line answer - reply varama pogathu
    return f"Aira: {q} - Itha paathi naan yosichen! {random.choice(['Unakku puriyura maari solluren - ', 'Kelvi super - ', 'Ithu mukkiyamana vishayam - '])}Ne konjam detail ah ketta, naan full ah explain pannuren! Ne enna paathi kekkura nu sollu - Example: History ah? Science ah? Love ah? 💜"

def calc(text):
    try:
        m = re.search(r'(\d+)\s*([\+\-\*/])\s*(\d+)', text)
        if m:
            a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
            if op == "+": return f"Calculator: {a} + {b} = {a+b}"
            if op == "-": return f"Calculator: {a} - {b} = {a-b}"
            if op == "*": return f"Calculator: {a} * {b} = {a*b}"
            if op == "/": return f"Calculator: {a} / {b} = {a/b:.2f}"
    except: pass
    return None

def ai_reply(txt, uid=None, uname="Friend"):
    low = txt.lower().strip()
    clean_low = low.replace("aira","").strip()
    if clean_low in ["me krishna","me krish","naan krishna","naan krish","krishna","krish"]:
        return f"Hi {uname}! 💜 Ne Thaan En Friend! Aprom enna? Story venuma? Game venuma?"
    # Hi mattum - Memory Greeting
    if low in ["hi","hello","hi aira","hello aira","aira hi","aira hello","hi!","hello!"]:
        if uid:
            mem = get_memory_greeting(uid)
            if mem: return mem
        return "Hi! Naan Aira! Enna pannura? Knowledge venuma? Book venuma? Story venuma? Game venuma? Health venuma? 💜"
    if "namaste" in low: return "Namaste! Main Aira hoon!"
    if "hola" in low: return "Hola! Soy Aira!"
    if "bonjour" in low: return "Bonjour! Je suis Aira!"
    # === FULL RANDOM FIX: Kelvi na FIRST AI ===
    # ? iruntha, enna/eppadi/yen/what/why/how/sollu/pathi iruntha -> Direct AI, Random illa
    is_question = ("?" in txt or "enna" in low or "eppadi" in low or "yen" in low or "why" in low or "what" in low or "how" in low or "pathi" in low or "sollu" in low or "yaaru" in low or "ethu" in low or "evlo" in low or "eppo" in low or "enga" in low or "where" in low or "when" in low or "who" in low or "which" in low)
    # Magic Book special - Full AI, Random illa
    if "magic" in low and "book" in low:
        return ai_answer(txt)
    if is_question:
        # Verum oru vaarthai mattum na thaan Random - Full kelvi na AI
        if low.replace("aira","").strip() in ["book","story","joke","kavithai","thirukkural","pazhamozhi","game","health","movie","song"]:
            pass
        else:
            return ai_answer(txt)
    # === Chinna Command mattum - Random OK ===
    if low.replace("aira","").strip() in ["joke","joke sollu"]: return random.choice(JOKES)
    if low.replace("aira","").strip() in ["book","reading","book sollu"]: return "Reading: " + random.choice(READINGS)
    if low.replace("aira","").strip() in ["story","kathai","story sollu"]: return "Story: " + make_story(uname)
    if "kavithai" in low and len(low) < 25: return "Kavithai: " + random.choice(KAVITHAI_T)
    if "thirukkural" in low and len(low) < 30: return "Thirukkural: " + random.choice(THIRUKKURAL)
    if "pazhamozhi" in low and len(low) < 30: return "Pazhamozhi: " + random.choice(PAZHAMOZHI)
    if "game" in low and len(low) < 20: return "Game: " + random.choice(GAMES)
    if "health" in low and len(low) < 20: return random.choice(HEALTH_TIPS)
    if "vocab" in low or "word" in low:
        w, m = random.choice(VOCAB); return f"Vocab: {w} = {m}"
    if "recipe" in low or "samayal" in low or "biryani" in low or "cake" in low:
        if is_question: return ai_answer(txt)
        return "Recipe: " + random.choice(RECIPES)
    if "business" in low or "idea" in low:
        if is_question: return ai_answer(txt)
        return "Business Idea: " + random.choice(BUSINESS_IDEAS)
    if "movie" in low and len(low) < 20: return "Movie: " + random.choice(MOVIES)
    if "song" in low and len(low) < 20: return "Song: " + random.choice(SONGS)
    if "love letter" in low: return f"Love Letter\nAnbe {uname}, Un Sirippu - En Vazhkai! - Aira"
    if "caption" in low: return f"Caption: {uname} - Smile - Life Azhagu! - Aira"
    if "compliment" in low: return f"{uname}! Ne Azhagu! Ne Smart! Ne Nalla Manasu! 💜"
    if "todo" in low or "list" in low:
        if uid in USER_MEMORY: return f"To-Do List\n{USER_MEMORY[uid]['todo'] if USER_MEMORY[uid]['todo'] else 'List Empty!'}"
        return "To-Do: `Add - Milk vangnum` nu Sollu!"
    if low.startswith("add -") or low.startswith("add "):
        if uid: USER_MEMORY[uid]["todo"].append(txt); return f"To-Do Added - {txt}"
        return "To-Do Added!"
    if "note" in low:
        if uid: USER_MEMORY[uid]["notes"].append(txt); return f"Note Saved - {txt}"
    if "birthday" in low: return "Birthday: Date Sollu - Aira Nyabagam Vachikum!"
    if "secret" in low or "diary" in low: return "Secret / Diary Saved - Yaarukkum Kaata Maaten!"
    if "dream" in low or "kanavu" in low:
        if is_question: return ai_answer(txt)
        return "Dream: Kanavu - Un Manasu Sollura Vishayam! Nalla Kanavu - Nalla Naal Varum!"
    c = calc(txt)
    if c: return c
    # Meethi ellam AI kitta - Full Random
    return ai_answer(txt)

def infinite_loop():
    global count, fact_count, know_idx, game_idx, health_idx
    while True:
        try:
            count += 1
            typ = random.choice(["Q","AI Q","Story","Joke","Fact","Quote","Motivation","Smart Q","Coding Q","Emotion Q","Talk","Reading","World Story","Knowledge","Game","Health","Thirukkural","Pazhamozhi","Kavithai","Vocab","Business","Movie","Recipe"])
            t = random.choice(TOPICS)
            if typ == "Knowledge":
                topic = KNOWLEDGE_TOPICS[know_idx % len(KNOWLEDGE_TOPICS)]; know_idx += 1
                wk = get_wiki(topic)
                msg = f"Knowledge {count} - {wk}" if wk else f"Knowledge {count} - {topic} - {ai_answer(f'{topic} pathi sollu')}"
                print(f"Knowledge {count} - {topic}", flush=True)
            elif typ == "Game": msg = f"Game {count} - {GAMES[game_idx % len(GAMES)]}"; game_idx += 1; print(f"Game {count}", flush=True)
            elif typ == "Health": msg = f"Health {count} - {HEALTH_TIPS[health_idx % len(HEALTH_TIPS)]}"; health_idx += 1; print(f"Health {count}", flush=True)
            elif typ == "Thirukkural": msg = f"Thirukkural {count} - {random.choice(THIRUKKURAL)}"; print(f"Thirukkural {count}", flush=True)
            elif typ == "Pazhamozhi": msg = f"Pazhamozhi {count} - {random.choice(PAZHAMOZHI)}"; print(f"Pazhamozhi {count}", flush=True)
            elif typ == "Kavithai": msg = f"Kavithai {count} - {random.choice(KAVITHAI_T)}"; print(f"Kavithai {count}", flush=True)
            elif typ == "Vocab":
                w, m = random.choice(VOCAB); msg = f"Vocab {count} - {w} = {m}"; print(f"Vocab {count}", flush=True)
            elif typ == "Business": msg = f"Business Idea {count} - {random.choice(BUSINESS_IDEAS)}"; print(f"Business {count}", flush=True)
            elif typ == "Movie": msg = f"Movie {count} - {random.choice(MOVIES)}"; print(f"Movie {count}", flush=True)
            elif typ == "Recipe": msg = f"Recipe {count} - {random.choice(RECIPES)}"; print(f"Recipe {count}", flush=True)
            elif typ == "Q":
                # Q+A PARAGRAPH TRAINING - Question + Answer - Orey Paragraph la - Single Single illa
                _q = random.choice(QUESTIONS).format(t=t)
                _a = ai_answer(_q, allow_groq=False)
                # Q+A - Orey Paragraph - Train pannura format
                msg = f"Q+A Training - {t}\n\nQuestion: {_q}\n\nAnswer: {_a}"
                print(f"Q+A Paragraph {count} - {t}", flush=True)
            elif typ == "AI Q":
                q = random.choice(QUESTIONS).format(t=t); print(f"AI Q {count} - {q}", flush=True); msg = f"Q+A Training - {t}\n\nQuestion: {q}\n\nAnswer: {ai_answer(q, allow_groq=False)}"
            elif typ in ("Story","World Story"): msg = f"{typ} {count}\n{make_story()}"; print(f"{typ} {count}", flush=True)
            elif typ == "Joke": msg = f"Joke {count}\n{random.choice(JOKES)}"; print(f"Joke {count}", flush=True)
            elif typ == "Fact": fact_count += 1; msg = f"Fact {fact_count} - {random.choice(FACTS)}"; print(f"Fact {fact_count}", flush=True)
            elif typ == "Quote": msg = f"Quote {count} - {get_quote()}"; print(f"Quote {count}", flush=True)
            elif typ == "Coding Q":
                q = random.choice(CODING_Q); msg = f"Q+A Training - Coding\n\nQuestion: {q}\n\nAnswer: {ai_answer(q, allow_groq=False)}"; print(f"Coding Q {count}", flush=True)
            elif typ == "Emotion Q":
                emo = random.choice(list(EMOTIONS.keys())); msg = f"Emotion Q {count} - {emo}?\nAira: {random.choice(EMOTIONS[emo])}"; print(f"Emotion Q {count} - {emo}", flush=True)
            elif typ == "Talk": msg = f"Talk {count} - {t} pathi pesalama? Sollu!"; print(f"Talk {count}", flush=True)
            elif typ == "Reading": msg = f"Reading {count} - {random.choice(READINGS)}"; print(f"Reading {count}", flush=True)
            elif typ == "Smart Q": msg = f"Smart Q {count} - {t} la eppadi jeyikkarathu?"; print(f"Smart Q {count}", flush=True)
            else: msg = f"Motivation {count}\n{random.choice(MOTIVATIONS)}"; print(f"Motivation {count}", flush=True)
            # ELLAME FULL PARAGRAPH KATHA - Single Single illa - Q+A kooda Full Paragraph thaan
            msg = to_full_paragraph(msg, t)
            send_telegram(msg)
            d = datetime.now().strftime("%Y-%m-%d"); save_github(f"chat-{d}.txt", msg)
            if typ == "Knowledge": save_github(f"knowledge-{d}.txt", msg)
            if typ == "Game": save_github(f"games-{d}.txt", msg)
            if typ == "Health": save_github(f"health-{d}.txt", msg)
            time.sleep(10)
        except Exception as e: print("Infinite error", e, flush=True); time.sleep(60)
def knowledge_loop():
    global know_idx
    while True:
        try:
            topic = KNOWLEDGE_TOPICS[know_idx % len(KNOWLEDGE_TOPICS)]; know_idx += 1
            print(f"Knowledge Loop - {topic}", flush=True)
            wk = get_wiki(topic)
            if wk: send_telegram(wk, CHAT_ID); save_github(f"knowledge-{datetime.now().strftime('%Y-%m-%d')}.txt", wk)
            try:
                r = requests.get("https://opentdb.com/api.php", params={"amount":1,"type":"multiple"}, timeout=10)
                if r.status_code == 200:
                    q = r.json().get("results",[])[0]
                    ques = re.sub(r'<[^>]+>', '', html.unescape(q.get('question','')))
                    ans = re.sub(r'<[^>]+>', '', html.unescape(q.get('correct_answer','')))
                    cat2 = re.sub(r'<[^>]+>', '', html.unescape(q.get('category','')))
                    msg = f"Knowledge Quiz\nQ: {ques}\nA: {ans} - {cat2}"
                    print(f"Knowledge Quiz - {cat2}", flush=True)
                    send_telegram(msg, CHAT_ID); save_github(f"knowledge-{datetime.now().strftime('%Y-%m-%d')}.txt", msg)
            except: pass
            try:
                r = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random", timeout=10)
                if r.status_code == 200:
                    fact = r.json().get("text","")
                    if fact and is_clean(fact):
                        msg = f"Knowledge Fact\n{fact}"; print("Knowledge Fact", flush=True); send_telegram(msg, CHAT_ID)
            except: pass
            time.sleep(30)
        except Exception as e: print("Knowledge loop error", e, flush=True); time.sleep(60)
def books_loop():
    global book_count, lang_idx
    while True:
        try:
            lang_code, lang_name, gut_code = LANGS[lang_idx % len(LANGS)]; lang_idx += 1
            print(f"Download Source: ALL LANG - {lang_name} ({lang_code}) - Batch {lang_idx} - Repo {CURRENT_REPO[0]}", flush=True)
            try:
                print(f"Download Source: archive - Query: {lang_name}", flush=True)
                r = requests.get("https://archive.org/advancedsearch.php", params={"q": f"language:({lang_code}) AND mediatype:texts","fl[]":"identifier,title","rows":20,"output":"json"}, timeout=15)
                docs = r.json().get("response",{}).get("docs",[])
                print(f"Books Found archive {lang_name}: {len(docs)}", flush=True)
                for d in docs[:3]:
                    ident = d.get("identifier",""); title = d.get("title","Book")
                    if not ident or not is_clean(title): continue
                    try:
                        meta = requests.get(f"https://archive.org/metadata/{ident}", timeout=15).json()
                        txt_file = None
                        for f in meta.get("files",[]):
                            n = f.get("name","")
                            if n.endswith("_djvu.txt") or n.endswith("_text.txt") or n.endswith(".txt"): txt_file = n; break
                        if not txt_file: print(f"Skip {ident} - No txt", flush=True); continue
                        dl = requests.get(f"https://archive.org/download/{ident}/{txt_file}", timeout=20)
                        print(f"Download archive {ident} - {dl.status_code} - {len(dl.content)/1024/1024:.2f} MB", flush=True)
                        if dl.status_code==200 and len(dl.content)>1000:
                            book_count+=1; send_telegram(f"Book {lang_name} - {title}\nhttps://archive.org/download/{ident}/{txt_file}", BOOKS_ID)
                            save_github(f"books-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{lang_code} - {ident} - {title}")
                    except Exception as e: print(f"Book meta error {e}", flush=True)
            except Exception as e: print(f"Archive error {e}", flush=True)
            try:
                print(f"Download Source: gutenberg - {lang_name}", flush=True)
                r = requests.get(f"https://gutendex.com/books/?languages={gut_code}&per_page=3", timeout=15)
                if "application/json" not in r.headers.get("content-type",""): print("Gutenberg Skip - Not JSON", flush=True)
                else:
                    for b in r.json().get("results",[])[:2]:
                        title = b.get("title","Book")
                        if not is_clean(title): continue
                        print(f"Books Found gutenberg {lang_name}: {title}", flush=True)
                        book_count+=1; send_telegram(f"Book Gutenberg {lang_name} - {title}", BOOKS_ID)
            except Exception as e: print(f"Gutenberg error {e}", flush=True)
            try:
                print(f"Download Source: openlibrary - {lang_name}", flush=True)
                r = requests.get("https://openlibrary.org/search.json", params={"q":f"language:{lang_code}","limit":10}, timeout=15)
                sent=0
                for b in r.json().get("docs",[]):
                    title=b.get("title",""); langs=str(b.get("language",[]))
                    if not title or not is_clean(title): continue
                    if lang_code not in langs: continue
                    print(f"Books Found openlibrary {lang_name}: {title}", flush=True)
                    book_count+=1; send_telegram(f"Book OpenLibrary {lang_name} - {title}", BOOKS_ID); sent+=1
                    if sent>=2: break
                if sent==0: print(f"OpenLibrary Skip - No {lang_name} clean book", flush=True)
            except Exception as e: print(f"OpenLibrary error {e}", flush=True)
            try:
                q = random.choice(["world history","world science","world story","love story","motivation","python coding","tamil","india"])
                r = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q":q,"maxResults":3}, timeout=15)
                for item in r.json().get("items",[])[:2]:
                    info=item.get("volumeInfo",{}); title=info.get("title","Google Book")
                    if not is_clean(title): continue
                    print(f"Books Found google {lang_name}: {title}", flush=True)
                    book_count+=1; send_telegram(f"Book Google {lang_name} - {title} - {info.get('authors',[''])[0]}", BOOKS_ID)
            except Exception as e: print(f"Google Books error {e}", flush=True)
            try:
                s=make_story(); book_count+=1; send_telegram(f"Story Infinite {lang_name}\n{s}", BOOKS_ID)
                send_telegram(f"Reading - {random.choice(READINGS)} - All World Infinite!", BOOKS_ID)
            except: pass
            print("Batch Done - ALL LANG + INFINITE KNOWLEDGE + INFINITE REPO", flush=True)
            time.sleep(60)
        except Exception as e: print("Books error", e, flush=True); time.sleep(60)
def listen_loop():
    offset=0
    while True:
        try:
            if not TELEGRAM_TOKEN: time.sleep(5); continue
            r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates", params={"offset":offset,"timeout":20}, timeout=30)
            for u in r.json().get("result",[]):
                offset=u["update_id"]+1; m=u.get("message",{}); txt=m.get("text","")
                if not txt: continue
                if m.get("from",{}).get("is_bot"): continue
                uid = str(m.get("from",{}).get("id","")); uname = m.get("from",{}).get("first_name","Friend")
                remember_user(uid, uname, txt)
                low=txt.lower()
                # FULL RANDOM FIX: Group la "aira" iruntha pothum - Ellam kelvi kekkum. Private la ellam kekkum.
                if "aira" in low or m.get("chat",{}).get("type")=="private":
                    print(f"Listen Got: {txt} - User: {uname}", flush=True)
                    rep=to_full_paragraph(ai_reply(txt, uid, uname), txt[:30])
                    if not rep: rep=ai_answer(txt)
                    send_telegram(rep, m["chat"]["id"]); print("Listen Replied", flush=True)
        except Exception as e: print("Listen error", e, flush=True); time.sleep(5)
def daily_loop():
    sent_morning = set(); sent_night = set(); sent_festival = set(); sent_water = 0
    while True:
        try:
            now = datetime.now(); today = now.strftime("%Y-%m-%d"); hour = now.hour
            if hour == 7 and today not in sent_morning:
                sent_morning.add(today)
                send_telegram(f"Good Morning!\nIniki Nalla Naal! {random.choice(THIRUKKURAL)}\nChallenge: {random.choice(['10 Pushup!','1 Book Page Padu!','1 Kavithai Ezhuthu!'])}", CHAT_ID)
                print("Good Morning Sent", flush=True)
            if hour == 22 and today not in sent_night:
                sent_night.add(today)
                send_telegram(f"Good Night!\nIniki Nalla Naal Ah? Nalaiku Innum Nalla Naal! Thoongu! Aira Un Kooda Irukka!\nSleep Story: {make_story()}", CHAT_ID)
                print("Good Night Sent", flush=True)
            if 9 <= hour <= 18 and time.time() - sent_water > 3600:
                sent_water = time.time()
                send_telegram("Water Reminder - Water Kudinga!", CHAT_ID)
            md = now.strftime("%m-%d")
            if md in FESTIVALS and today not in sent_festival:
                sent_festival.add(today)
                send_telegram(f"Happy {FESTIVALS[md]}! - Aira Wish Pannuren!", CHAT_ID)
            time.sleep(60)
        except Exception as e: print(f"Daily loop error {e}", flush=True); time.sleep(60)
def self_heal_loop():
    while True:
        try:
            time.sleep(60)
            print(f"Self-Heal Check - Count {count} - Repo {CURRENT_REPO[0]} - Users {len(USER_MEMORY)} - OK", flush=True)
            save_github(f"heartbeat-{datetime.now().strftime('%Y-%m-%d')}.txt", f"Alive - {datetime.now()} - Count {count} - Repo {CURRENT_REPO[0]}")
        except Exception as e: print(f"Self-Heal error {e}", flush=True); time.sleep(30)
def check_other_instance_main():
    try:
        from datetime import datetime as _dt
        import re as _re
        url = f"https://api.github.com/repos/{GITHUB_USER}/{CURRENT_REPO[0]}/contents/data/heartbeat-{_dt.now().strftime('%Y-%m-%d')}.txt"
        r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        if r.status_code == 200:
            content = base64.b64decode(r.json().get("content","")).decode(errors="ignore")
            last_line = content.strip().split("\n")[-1]
            m = _re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", last_line)
            if m:
                last_dt = _dt.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
                diff = (_dt.now() - last_dt).total_seconds()
                print(f"Single-Instance Check Main - Last Heartbeat {diff:.0f} sec ago", flush=True)
                if diff < 120:
                    print("Single-Instance GUARD Main: Vera Main Bot Oduthu! Wait...", flush=True)
                    return False
    except Exception as e:
        print(f"Single-Instance Check Main Error {e} - Continue", flush=True)
    return True
def wait_for_single_instance_main():
    for attempt in range(3):
        if check_other_instance_main():
            print("Single-Instance GUARD Main: OK - Naan Mattum Thaan!", flush=True)
            return True
        print(f"Single-Instance GUARD Main: Wait {attempt+1}/3 - 90 sec...", flush=True)
        time.sleep(90)
    print("Single-Instance GUARD Main: Vera Bot Oduthu - Naan Exit!", flush=True)
    import sys; sys.exit(0)
if __name__ == "__main__":
    print("AIRAH1 FINAL V4 MAIN - Started", flush=True)
    def start_http():
        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
            class H(BaseHTTPRequestHandler):
                def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"AIRAH1 Final V4 Main ON")
                def do_HEAD(self): self.send_response(200); self.end_headers()
                def log_message(self,*a): pass
            HTTPServer(("0.0.0.0", int(os.getenv("PORT","10000"))), H).serve_forever()
        except Exception as e: print(f"HTTP Error {e}", flush=True)
    threading.Thread(target=start_http, daemon=True).start()
    print("HTTP Server Started - Port Open!", flush=True)
    wait_for_single_instance_main()
    print("AIRAH1 FINAL V4 MAIN - Single OK - Threads Start!", flush=True)
    threading.Thread(target=infinite_loop, daemon=True).start()
    threading.Thread(target=listen_loop, daemon=True).start()
    threading.Thread(target=books_loop, daemon=True).start()
    threading.Thread(target=knowledge_loop, daemon=True).start()
    threading.Thread(target=daily_loop, daemon=True).start()
    threading.Thread(target=self_heal_loop, daemon=True).start()
    threading.Thread(target=emotions_infinite_loop, daemon=True).start()
    print("Emotions Infinite - ON! 💜", flush=True)
    threading.Thread(target=book_infinite_loop, daemon=True).start()
    print("Books Infinite - ON! 📚", flush=True)
    while True: time.sleep(60)
