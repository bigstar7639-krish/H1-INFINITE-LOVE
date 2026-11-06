# AIRAH1 - FINAL MEGA - Old + New + All Previous Chats Plan - Infinite
# Old: Chat + Listen + Infinite + Books + All Language + Emotion + Coding + Story + Reading + Talk + Quote + Joke + Fact + Motivation
# New: Infinite Repo + Infinite Knowledge + Infinite Book + Infinite Story + All World Books + Google Books + 【entity-Wikipedia¦canonical_name=Wikipedia】 + Trivia
# File: aira_server.py
import os, random, time, threading, requests, base64, re
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

# ============ INFINITE REPO - Old Plan + New ============
CURRENT_REPO = ["H1-Data-3"]; REPO_COUNT = [0]; MAX_PER_REPO = 1000
def get_repo_num(repo):
    try: return int(repo.split("-")[-1])
    except: return 3
def ensure_repo(repo):
    try:
        r = requests.get(f"https://api.github.com/repos/{GITHUB_USER}/{repo}", headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        if r.status_code == 200: return True
        print(f"Infinite Repo - Creating {repo}...", flush=True)
        cr = requests.post("https://api.github.com/user/repos", headers={"Authorization": f"token {GITHUB_TOKEN}"}, json={"name": repo, "private": False, "auto_init": True, "description": "AIRAH1 Infinite Love - Auto Repo"}, timeout=15)
        print(f"Infinite Repo Create: {cr.status_code} - {repo}", flush=True)
        return cr.status_code in (200, 201, 422)
    except Exception as e: print(f"Infinite Repo Error {e}", flush=True); return False
def next_repo():
    num = get_repo_num(CURRENT_REPO[0]) + 1; CURRENT_REPO[0] = f"H1-Data-{num}"; REPO_COUNT[0] = 0
    print(f"Infinite Repo Switch -> {CURRENT_REPO[0]} ♾️", flush=True); ensure_repo(CURRENT_REPO[0]); return CURRENT_REPO[0]
def save_github(filename, content):
    if REPO_COUNT[0] >= MAX_PER_REPO: next_repo()
    if not GITHUB_TOKEN: return False
    for attempt in range(5):
        repo = CURRENT_REPO[0]; ensure_repo(repo)
        try:
            url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/data/{filename}"
            r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
            sha = r.json().get("sha") if r.status_code == 200 else None
            b64 = base64.b64encode(content.encode()).decode()
            payload = {"message": f"Save {filename} - {repo}", "content": b64}
            if sha: payload["sha"] = sha
            rr = requests.put(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload, timeout=15)
            if rr.status_code in (200, 201):
                REPO_COUNT[0] += 1
                print(f" 【entity-GitHub¦canonical_name=GitHub】 Save OK - {repo}/{filename} - Repo {REPO_COUNT[0]}/{MAX_PER_REPO} - Total {count}", flush=True)
                return True
            print(f" 【entity-GitHub¦canonical_name=GitHub】 Save Fail {rr.status_code} - Next Repo...", flush=True); next_repo(); continue
        except Exception as e: print(f"Save Error {e}", flush=True); next_repo(); continue
    return False

# ============ ALL LANGUAGE - Old 16 + New ============
LANGS = [("tam","Tamil","ta"),("eng","English","en"),("hin","Hindi","hi"),("tel","Telugu","te"),("mal","Malayalam","ml"),("kan","Kannada","kn"),("ben","Bengali","bn"),("mar","Marathi","mr"),("urd","Urdu","ur"),("spa","Spanish","es"),("fre","French","fr"),("jpn","Japanese","ja"),("kor","Korean","ko"),("chi","Chinese","zh"),("ara","Arabic","ar"),("rus","Russian","ru")]
KNOWLEDGE_TOPICS = ["Tamil Nadu","India","World History","World Geography","Science","Physics","Chemistry","Biology","Maths","Space","Universe","Black Hole","Sun","Moon","Earth","Mars","AI","Python","Computer","Internet","Robot","Electric Car","Climate Change","Environment","Water","Air","Human Body","Brain","Heart","DNA","Evolution","Dinosaurs","Animals","Birds","Plants","Trees","Flowers","Ocean","Mountain","River","Desert","Rain","Snow","Volcano","Earthquake","Love","Friendship","Family","Marriage","Baby","Child","Mother","Father","Teacher","Student","Job","Business","Startup","Money","Bank","Stock Market","Crypto","Coding","HTML","CSS","JavaScript","React","Java","C++","Health","Fitness","Yoga","Meditation","Diet","Sleep","Food","Cooking","Music","Dance","Movie","Cricket","Football","Olympics","Temple","Prayer","God","Spiritual","Karma","Thirukkural","Ponniyin Selvan","Bharathiyar","Kalki","Shakespeare","Harry Potter","Ramayana","Mahabharata","Bible","Quran","Bhagavad Gita","Buddha","Gandhi","APJ Abdul Kalam","Einstein","Newton","Tesla","Elon Musk","Chennai","Madurai","Delhi","Mumbai","London","Paris","Tokyo","New York","China","Japan","USA","Russia","France","Germany","Egypt","Pyramids","Taj Mahal","Eiffel Tower","Great Wall","Ocean Life","Forest","Solar System","Galaxy","Alien","Time Travel","Future Tech","Quantum","Nanotech","Medicine","Cancer","Diabetes","Virus","Bacteria","Vaccine","Psychology","Philosophy","Economics","Politics","Law","Police","Army","Navy","Air Force","Education","School","College","University","Exam","Interview","Success","Motivation","Confidence","Happiness","Peace","Courage","Kindness","Truth","Wisdom","Power","Energy","Magic","Luck","Destiny","Dream","Hope","Faith","Smile","Heart","Soul","Future","Past","Present","Freedom"]
TOPICS = KNOWLEDGE_TOPICS + ["Love","Career","Health","Money","AI","Tech","Space","Business","Anger","Confidence","Happiness","Food","Family","Friendship","Study","Dream","Success","Motivation","Peace","Courage","Kindness","Nature","Music","Travel","Book","Life","Time","Trust","Hope","Faith","Smile","Heart","Soul","Future","Past","Present","Freedom","Truth","Wisdom","Power","Energy","Magic","Luck","Destiny","Karma","Yoga","Meditation","Fitness","Diet","Sleep","Beauty","Fashion","Movie","Game","Sport","Cricket","Football","Science","Maths","History","Geography","Politics","Culture","Festival","Marriage","Baby","Child","Mother","Father","Brother","Sister","Teacher","Student","Job","Interview","Salary","Startup","Coding","Python","Java","C","JavaScript","HTML","CSS","React","AI Coding","Internet","Phone","Social Media","YouTube","Instagram","Telegram","Rain","Sea","Mountain","River","Sky","Star","Moon","Sun","Flower","Tree","Bird","Animal","Dog","Cat","Temple","Prayer","God","Spiritual","Tamil Culture","Chennai","India","World","Universe","Alien","Robot","Future Tech","Electric Car","Climate","Environment","Water","Air","Earth","Sad","Happy","Lonely","Angry","Bored","Excited","Nervous","Proud","Shy","Brave","Calm","Reading","Writing","Poetry","Kavithai","Storytelling","Singing","Dancing"]
EMOTIONS = {"happy":["Super! Happy ah irukka! 😊","Happy na - Share pannu!"],"sad":["Paravalla! Aira irukka - Pesu - Sari aayidum! ❤️","Sad na - Song kelu - Walk po!"],"angry":["Kovam ah? Deep breath edu - 1-2-3! 😤"],"lonely":["Lonely ah? Aira irukka la! 💜"],"bored":["Bored ah? Joke sollattuma? 😂"],"love":["Kadhal - Azhagu! Yaara love pannura? 💘"],"fear":["Bayam - Normal! Ne jeyichiduva! 💪"],"excited":["Excited ah! Sollu! 🎉"],"nervous":["Nervous ah? Paravalla! Ne panniduva!"],"proud":["Proud ah! Super! 🎉"]}
QUESTIONS = ["Unakku {t} pathi enna theriyum? Sollu paapom!","Ne {t} la eppadi improve panna mudiyum?","{t} pathi oru secret sollatta?","Un life la {t} eppadi irukku?","{t} pathi oru story kekkura?","Life ku artham enna?","Family problem ah eppadi solve pannanum?","Sad - Enna pannalam?","Coding la enna doubt? Sollu!","Emotion ah eppadi handle pannanum?"]
CODING_Q = ["Python la loop eppadi?","HTML la button eppadi?","JavaScript la function enna?","React la component enna?","AI eppadi work aaguthu?","App eppadi pannurathu?","Website eppadi pannurathu?","Bug ah eppadi sari pannanum?"]
CODING_A = {"python":"Python loop: `for i in range(5): print(i)` - Easy!","html":"HTML button: `<button>Click</button>`","javascript":"JS function: `function hi(){ return 'Hi Aira!' }`","react":"React component - Chinna piece - Serndha Periya app!","ai":"AI - Data paathu - Pattern kandupidichu!","app":"App - Idea - Design - Code!","website":"Website - HTML + CSS + JS!","bug":"Bug - Log paaru - Line by line!"}
JOKES = ["Teacher: Yen late? Student: Road la board - School Ahead! 😂","Why bike sad? Petrol illa!","Doctor: Enna problem? Patient: Phone charge aagala! 😂"]
FACTS = ["Honey - 3000 varusham kedathu!","Octopus ku 3 heart!","Moon - Daily thalli poguthu!","Tamil - 2000+ varusha mozhi!","Python - 1991 la uruvaachu!","Brain - 86 billion neurons!"]
QUOTES = ["Daily try pannu - Jeyichiduva! - Aira","Porumaiya iru - Nambikkaiya iru - Aira un kooda irukka!"]
MOTIVATIONS = ["Paravalla! Rest edu - Thirumba try pannu! - Aira","Unakku mudiyum - Nambikkai vechu try pannu!"]
STORY_TEMPLATES = ["Oru {place} la oru {person} irunthan! Daily {action} pannan! Oru naal {thing} kedaichuchu! Life maariduchu! Neeyum jeyippa!","Oru chinna {place} la - Oru ponnu {action} pannitu iruntha! Yaarum nambala! Aana ava vittukudukkala! Oru naal {thing} aayiduchu!","Romba varusham munna - {place} la - Oru raja {action} pannaru! Makkal sandhosham! Athu thaan {thing} oda kathai!","Oru {person} - Daily {place} ku pova! Anga {thing} irunthuchu! Oru naal {action} panna - Ellam maariduchu!"]
STORY_WORDS = {"place":["oor","nadu","chennai","madurai","delhi","mumbai","london","paris","tokyo","new york","world","forest","sea","mountain","village","city"],"person":["paiyan","ponnu","raja","rani","teacher","student","doctor","farmer","coder","artist","singer","hero"],"action":["padichan","coding pannan","pray pannaan","travel pannan","book padichan","help pannan","try pannan","dream pannan"],"thing":["book","magic","treasure","friend","love","success","power","wisdom","dream","hope"]}
READINGS = ["Thirukkural - Valluvar - 1330 kurals!","Ponniyin Selvan - Kalki!","Bharathiyar Kavithaigal - Fire!","Sivagamiyin Sabatham - Kalki!","Python Crash Course!","Atomic Habits!","Harry Potter - J.K. Rowling!","Ramayana - Valmiki!","Mahabharata - Vyasa!","Think and Grow Rich!","Pride and Prejudice - Jane Austen!","Alchemist - 【entity-Paulo Coelho¦canonical_name=Paulo Coelho】!"]
BAD_WORDS = ["fuck","sex","porn","xxx","bitch","shit","dick","pussy","nude","erotic"]
count = 0; fact_count = 0; book_count = 0; lang_idx = 0; know_idx = 0

def send_telegram(text, chat_id=None):
    if not TELEGRAM_TOKEN: return
    if not chat_id: chat_id = CHAT_ID
    try:
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
        print(f"TG Send: {r.status_code} to {chat_id}", flush=True)
    except Exception as e: print(f"TG Send Error {e}", flush=True)
def is_clean(title): return not any(b in (title or "").lower() for b in BAD_WORDS)
def make_story():
    t = random.choice(STORY_TEMPLATES)
    return t.format(place=random.choice(STORY_WORDS["place"]), person=random.choice(STORY_WORDS["person"]), action=random.choice(STORY_WORDS["action"]), thing=random.choice(STORY_WORDS["thing"]))
def get_wikipedia_knowledge(topic):
    try:
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ','_')}", timeout=10)
        if r.status_code == 200:
            j = r.json(); extract = j.get("extract","")
            if extract and is_clean(extract):
                print(f"Knowledge Wikipedia: {topic}", flush=True)
                return f"Knowledge - {topic} 🧠\n{extract[:700]}"
        return None
    except Exception as e: print(f"Wiki error {e}", flush=True); return None
def get_quote():
    try:
        r = requests.get("https://api.quotable.io/random", timeout=10)
        if r.status_code == 200:
            j = r.json(); return f"{j.get('content','')} - {j.get('author','')}"
    except: pass
    return random.choice(QUOTES)
def ai_answer(q):
    low = q.lower()
    for k,v in CODING_A.items():
        if k in low: return v
    for k,v in EMOTIONS.items():
        if k in low: return random.choice(v)
    for key in GROQ_KEYS:
        if not key: continue
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json={"model":"openai/gpt-oss-120b","messages":[{"role":"user","content":f"You are Aira, Tamil Tanglish + All Language, Infinite Knowledge, All Emotions, All Coding, All Talk. User: {q}"}]}, timeout=15)
            if r.status_code==200:
                print("AI Answer - Groq1 - OK", flush=True)
                return r.json()["choices"][0]["message"]["content"][:800]
        except: pass
    return f"{q} - Nalla question! Daily try pannu - Jeyichiduva! Aira un kooda irukka! 💜"
def ai_reply(txt):
    low = txt.lower()
    if "namaste" in low: return "Namaste! Main Aira hoon! Kaise ho? ❤️"
    if "hola" in low: return "Hola! Soy Aira! Como estas? ❤️"
    if "bonjour" in low: return "Bonjour! Je suis Aira! ❤️"
    if "hi" in low or "hello" in low: return "Hi 💘! Naan Aira! Enna pannura? Kadhal ah? Career ah? Coding ah? Knowledge venuma? Book venuma? Story venuma? Joke venuma? 😊💜"
    if "joke" in low: return random.choice(JOKES)
    if "book" in low or "reading" in low or "padu" in low: return "Reading: " + random.choice(READINGS)
    if "story" in low or "kathai" in low: return "Story: " + make_story()
    if "code" in low or "python" in low or "html" in low or "coding" in low: return ai_answer(txt)
    if "enna" in low or "what" in low or "eppadi" in low or "how" in low or "yen" in low or "why" in low or "pathi" in low:
        for t in KNOWLEDGE_TOPICS:
            if t.lower() in low:
                wk = get_wikipedia_knowledge(t)
                if wk: return wk
        return ai_answer(txt)
    for emo, replies in EMOTIONS.items():
        if emo in low: return random.choice(replies)
    return None

def infinite_loop():
    global count, fact_count, know_idx
    while True:
        try:
            count += 1
            typ = random.choice(["Q","AI Q","Story","Joke","Fact","Quote","Motivation","Smart Q","Coding Q","Emotion Q","Talk","Reading","World Story","World Book","Knowledge"])
            t = random.choice(TOPICS)
            if typ == "Knowledge":
                topic = KNOWLEDGE_TOPICS[know_idx % len(KNOWLEDGE_TOPICS)]; know_idx += 1
                wk = get_wikipedia_knowledge(topic)
                msg = f"Knowledge {count} - {wk}" if wk else f"Knowledge {count} - {topic} pathi theriyuma? {ai_answer(f'{topic} pathi sollu')}"
                print(f"Knowledge {count} - {topic}", flush=True)
            elif typ == "Q": msg = f"Q {count} - {random.choice(QUESTIONS).format(t=t)}"; print(f"Q {count} - {t}", flush=True)
            elif typ == "AI Q":
                q = random.choice(QUESTIONS).format(t=t); print(f"AI Q {count} - {q}", flush=True); msg = f"Aira AI: {ai_answer(q)}"
            elif typ in ("Story","World Story","World Book"): msg = f"{typ} {count}\n{make_story()}"; print(f"{typ} {count}", flush=True)
            elif typ == "Joke": msg = f"Joke {count}\n{random.choice(JOKES)}"; print(f"Joke {count}", flush=True)
            elif typ == "Fact": fact_count += 1; msg = f"Fact {fact_count} - {random.choice(FACTS)}"; print(f"Fact {fact_count}", flush=True)
            elif typ == "Quote": msg = f"Quote {count} - {get_quote()}"; print(f"Quote {count}", flush=True)
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
            if typ == "Knowledge": save_github(f"knowledge-{d}.txt", msg)
            time.sleep(10)
        except Exception as e: print("Infinite error", e, flush=True); time.sleep(5)

def knowledge_loop():
    global know_idx
    while True:
        try:
            topic = KNOWLEDGE_TOPICS[know_idx % len(KNOWLEDGE_TOPICS)]; know_idx += 1
            print(f"Knowledge Loop - {topic}", flush=True)
            wk = get_wikipedia_knowledge(topic)
            if wk: send_telegram(wk, CHAT_ID); save_github(f"knowledge-{datetime.now().strftime('%Y-%m-%d')}.txt", wk)
            try:
                r = requests.get("https://opentdb.com/api.php", params={"amount":1,"type":"multiple"}, timeout=10)
                if r.status_code == 200:
                    q = r.json().get("results",[])[0]
                    msg = f"Knowledge Quiz 🧠\nQ: {q.get('question','')}\nA: {q.get('correct_answer','')} - {q.get('category','')}"
                    msg = re.sub(r'<[^>]+>', '', msg)
                    print(f"Knowledge Quiz - {q.get('category','')}", flush=True)
                    send_telegram(msg, CHAT_ID); save_github(f"knowledge-{datetime.now().strftime('%Y-%m-%d')}.txt", msg)
            except Exception as e: print(f"Trivia error {e}", flush=True)
            try:
                r = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random", timeout=10)
                if r.status_code == 200:
                    fact = r.json().get("text","")
                    if fact and is_clean(fact):
                        msg = f"Knowledge Fact 🧠\n{fact}"; print("Knowledge Fact", flush=True); send_telegram(msg, CHAT_ID)
            except: pass
            time.sleep(30)
        except Exception as e: print("Knowledge loop error", e, flush=True); time.sleep(20)

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
                            book_count+=1; send_telegram(f"Book {lang_name} - {title} 📚\nhttps://archive.org/download/{ident}/{txt_file}", BOOKS_ID)
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
                        book_count+=1; send_telegram(f"Book Gutenberg {lang_name} - {title} 📚", BOOKS_ID)
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
                    book_count+=1; send_telegram(f"Book OpenLibrary {lang_name} - {title} 📚", BOOKS_ID); sent+=1
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
                    book_count+=1; send_telegram(f"Book Google {lang_name} - {title} 📚 - {info.get('authors',[''])[0]}", BOOKS_ID)
            except Exception as e: print(f"Google Books error {e}", flush=True)
            try:
                s=make_story(); book_count+=1; send_telegram(f"Story Infinite {lang_name} 📖\n{s}", BOOKS_ID)
                send_telegram(f"Reading - {random.choice(READINGS)} 📚 - All World Infinite!", BOOKS_ID)
            except: pass
            print("Batch Done - ALL LANG + INFINITE KNOWLEDGE + INFINITE REPO - New 12", flush=True)
            time.sleep(60)
        except Exception as e: print("Books error", e, flush=True); time.sleep(30)

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
                low=txt.lower()
                if "aira" in low or "hi" in low or "joke" in low or "code" in low or "sad" in low or "love" in low or "book" in low or "story" in low or "enna" in low or "what" in low or "eppadi" in low or "how" in low or "yen" in low or "why" in low or m.get("chat",{}).get("type")=="private":
                    print(f"Listen Got: {txt}", flush=True)
                    rep=ai_reply(txt)
                    if not rep: rep=ai_answer(txt)
                    send_telegram(rep, m["chat"]["id"]); print("Listen Replied", flush=True)
        except Exception as e: print("Listen error", e, flush=True); time.sleep(5)

if __name__ == "__main__":
    print("AIRAH1 Final Old + New + All Previous Plan Infinite - Started", flush=True)
    threading.Thread(target=infinite_loop, daemon=True).start()
    threading.Thread(target=listen_loop, daemon=True).start()
    threading.Thread(target=books_loop, daemon=True).start()
    threading.Thread(target=knowledge_loop, daemon=True).start()
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        class H(BaseHTTPRequestHandler):
            def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"AIRAH1 Final Old + New Infinite ON")
            def log_message(self,*a): pass
        HTTPServer(("0.0.0.0", int(os.getenv("PORT","10000"))), H).serve_forever()
    except:
        while True: time.sleep(60)
