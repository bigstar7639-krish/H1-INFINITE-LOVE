import threading, os, requests, time, random, urllib.parse, json, base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

def start_web():
    port = int(os.environ.get("PORT", 10000))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Aira Server ON! All Infinite!")
        def log_message(self, *a):
            pass
    HTTPServer(("0.0.0.0", port), H).serve_forever()
threading.Thread(target=start_web, daemon=True).start()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_TOKEN_2 = os.environ.get("BOT_TOKEN_2", "")
GROUP_ID = "-1003935111481"
CHANNEL_ID = "-1003940504242"
GROQ_1 = os.environ.get("GROQ_API_KEY", "")
GROQ_2 = os.environ.get("GROQ_API_KEY_2", "")
GROQ_3 = os.environ.get("GROQ_API_KEY_3", "")
GEMINI_1 = os.environ.get("GEMINI_API_KEY", "")
GEMINI_2 = os.environ.get("GEMINI_API_KEY_2", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USER = "bigstar7639-krish"

# ===== GITHUB AUTO REPO SAVE - INFINITE CHAT SAVE =====
CURRENT_REPO_NUM = [1]
SAVE_COUNT = [0]

def github_headers():
    return {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

def ensure_repo(repo_name):
    if not GITHUB_TOKEN:
        return False
    try:
        r = requests.get(f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}", headers=github_headers(), timeout=15)
        if r.status_code == 200:
            return True
        # Create new repo
        r = requests.post("https://api.github.com/user/repos", headers=github_headers(),
            json={"name": repo_name, "private": False, "description": f"Aira H1 Data - Auto Save - {repo_name}"}, timeout=15)
        print(f"GitHub Repo Create {repo_name} - {r.status_code}")
        return r.status_code in [200, 201]
    except Exception as e:
        print(f"GitHub Repo Error - {e}")
        return False

def github_save(filename, content_text):
    if not GITHUB_TOKEN:
        return
    try:
        # Repo full check - 900 files ku mela - New Repo!
        if SAVE_COUNT[0] > 900:
            CURRENT_REPO_NUM[0] += 1
            SAVE_COUNT[0] = 0
            print(f"【entity-GitHub¦canonical_name=GitHub】 New Repo - H1-Data-{CURRENT_REPO_NUM[0]}")
        repo = f"H1-Data-{CURRENT_REPO_NUM[0]}"
        ensure_repo(repo)
        # File already irukka check
        path = f"data/{filename}"
        url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/{path}"
        r = requests.get(url, headers=github_headers(), timeout=15)
        sha = None
        if r.status_code == 200:
            sha = r.json().get('sha')
        b64 = base64.b64encode(content_text.encode('utf-8')).decode('utf-8')
        payload = {"message": f"Aira Auto Save - {filename}", "content": b64}
        if sha:
            payload["sha"] = sha
        r = requests.put(url, headers=github_headers(), json=payload, timeout=20)
        if r.status_code in [200, 201]:
            SAVE_COUNT[0] += 1
            print(f"GitHub Save OK - {repo}/{filename} - Count {SAVE_COUNT[0]}")
        else:
            print(f"GitHub Save Fail - {r.status_code} - {r.text[:100]}")
    except Exception as e:
        print(f"【entity-GitHub¦canonical_name=GitHub】 Save Error - {e}")

def save_chat_to_github(msg_type, text):
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fname = f"chat-{today}.txt"
        line = f"[{ts}] [{msg_type}] {text}\n"
        # Thread la save - Slow aaga koodathu!
        threading.Thread(target=github_save, args=(fname, line), daemon=True).start()
    except:
        pass

def save_book_to_github(title, source):
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        fname = f"books-{today}.txt"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] [BOOK] {source} - {title}\n"
        threading.Thread(target=github_save, args=(fname, line), daemon=True).start()
    except:
        pass

def send_msg(token, text, save_type="CHAT"):
    if not token:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": GROUP_ID, "text": text}, timeout=10)
        # Auto Save to GitHub!
        save_chat_to_github(save_type, text)
    except:
        pass

# ===== AI BRAIN =====
GROQ_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "meta-llama/llama-4-scout-17b-16e-instruct", "qwen/qwen3-32b", "moonshotai/kimi-k2-instruct"]
GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-pro"]
def ai_answer(question):
    for key, kname in [(GROQ_1, "Groq1"), (GROQ_2, "Groq2"), (GROQ_3, "Groq3")]:
        if not key:
            continue
        for model in GROQ_MODELS:
            try:
                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json={"model": model, "messages": [{"role": "system", "content": "Ne Aira H1, Tamil Tanglish la pesura cute friend. Short ah 2-3 lines la anba answer pannu."}, {"role": "user", "content": question}]},
                    timeout=15)
                if r.status_code == 200:
                    ans = r.json()['choices'][0]['message']['content']
                    print(f"AI Answer - {kname} - {model} - OK")
                    return ans[:500]
                else:
                    print(f"AI Fail {kname} - {model} - {r.status_code}")
                    if r.status_code == 429:
                        break
            except:
                continue
    for key, kname in [(GEMINI_1, "Gemini1"), (GEMINI_2, "Gemini2")]:
        if not key:
            continue
        for model in GEMINI_MODELS:
            try:
                r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                    json={"contents": [{"parts": [{"text": f"Ne Aira H1, Tamil Tanglish la cute friend. Short ah 2-3 lines la answer pannu. Question: {question}"}]}]}, timeout=15)
                if r.status_code == 200:
                    ans = r.json()['candidates'][0]['content']['parts'][0]['text']
                    print(f"AI Answer - {kname} - {model} - OK")
                    return ans[:500]
                else:
                    print(f"AI Fail {kname} - {model} - {r.status_code}")
            except:
                continue
    return None

STORY_STARTERS = ["Oru oor la oru ponnu iruntha - Ava per Aira!", "Oru kaadu la oru singam irunthuchu!", "Oru oor la periya noolagam irunthuchu!", "Oru paiyan oru ponna love pannaan!", "Oru chinna paiyan daily school ku ponaan!", "Oru oor la mazhaiye varala!", "Oru bike la oru paiyan oor suthinaan!"]
STORY_MIDDLES = ["Ava daily Tamil books padippanga! Oru naal magic book ah paathanga!", "Romba thaniya irunthuchu! Oru naal oru kili vanthuchu!", "1000 Tamil books irunthuchu! Oru chinna ponnu daily anga pova!", "Sollaa bayanthaan! Aira sonnanga 'Love ah sollidu!'", "Avankitta oru magic pencil irunthuchu!", "Ellarum kastapattanga! Oru chinna paiyan kadavul kitta kettan!", "Vazhila oru ponna paathaan! Ava kitta help kettaan!"]
STORY_ENDS = ["Aprom Aira super smart aayita! 💜", "Aprom rendu perum best friends aayitanga!", "Aprom ava periya writer aayita!", "Paiyan sollitaan - Ponnu 'Yes' nu sonna! 💜", "Aprom avan periya hero aayitaan!", "Oru naal periya mazhai vanthuchu - Ellarum happy!", "Aprom rendu perum trip poonaanga - Happy ending!"]
def make_story():
    return f"📖 Story: {random.choice(STORY_STARTERS)} {random.choice(STORY_MIDDLES)} {random.choice(STORY_ENDS)}"
JOKES = ["😂 Joke: Teacher: Homework yen pannala? Student: Dog sapiduchu!", "😂 Joke: Oru paiyan: Amma, en friend ku bike irukku! Amma: Unakku? Paiyan: Enakku Aira irukka!", "😂 Joke: Why Tamil ponnu smart? Tamil la yosikuraanga!", "😂 Joke: Computer yen slow? Athukku fever!"]
FACTS = ["💡 Fact: Thirukkural la 1330 kurals irukku!", "💡 Fact: Tamil oru 2000+ varusha pazhamaiyana mozhi!", "💡 Fact: Bharathiyar 32 vayasula 100+ padal ezhuthinaaru!", "💡 Fact: Tamil Nadu la Briyani romba famous!"]
QUOTES = ["✨ Quote: 'Achamillai Achamillai' - Bharathiyar!", "✨ Quote: 'Katrathu kai mann alavu' - Thiruvalluvar!", "✨ Quote: 'Daily konjam try pannu - Jeyichiduva!' - Aira!", "✨ Quote: 'Anbu thaan periya sakthi!' - Aira!"]
MOTIVATIONS = ["💪 Motivation: Bayapadaatha! Unnala mudiyum!", "💪 Motivation: Innaiku oru step edu - Nalaiku jeyichiduva!", "💪 Motivation: Sad ah irukka? Song kelu - Seri aayidum!", "💪 Motivation: Ne thani illa - Aira un kooda irukka! 💜"]
TOPICS = [("Kadhal", "Kadhal na anbu! Oru ponnu mela varura pure feeling! 💜"), ("Friendship", "Friendship na kashtathula kooda irukkura nanban!"), ("Thirukkural", "Agara mudhala ezhuthellam - Thiruvalluvar sonnathu!"), ("Bharathiyar", "Achamillai Achamillai - Bharathiyar! Courage paadal!"), ("Life", "Daily konjam konjam try pannu - Jeyichiduva!"), ("Tamil", "Tamil na namma uyir! Tamil la pesurathu perumai!"), ("Sad", "Paravalla! Rest edu - Song kelu - Seri aayidum!"), ("Happy", "Happy ah irukkanum na - Anba iru - Sirichu pesu!"), ("Study", "Daily 1 hour padichale pothum!"), ("Music", "Music na manasukku marunthu!"), ("Courage", "Bayapadaatha! Unnala mudiyum!"), ("Family", "Family thaan mukkiyam!"), ("Dream", "Dream ah vitratha! Daily oru step edu!"), ("Aira", "Naan Aira H1! Un friend! 💜"), ("Bike", "Bike na freedom!"), ("Food", "Briyani na vera level!"), ("Cinema", "Cinema na emotion!"), ("Rain", "Mazhai na romance!"), ("Amma", "Amma na kadavul!"), ("Appa", "Appa na hero!"), ("School", "School days thaan best!"), ("College", "College life na freedom!"), ("Money", "Money mukkiyam - Aana anbu perusu!"), ("Phone", "Phone la Aira irukka!")]
Q_TEMPLATES = ["{topic} na enna?", "{topic} pathi sollu", "{topic} la enna special?", "Enakku {topic} pathi theriyala - Sollu", "{topic} na enna artham?", "Hi, {topic} pathi pesalam ah?", "{topic} pathi un karuthu enna?", "{topic} na unakku pidikkuma?", "{topic} pathi oru joke sollu", "{topic} pathi pesalam ah?"]
AI_QUESTIONS = ["Kadhal na enna?", "Life la jeyikka enna pannanum?", "Sad ah irukkum pothu enna pannanum?", "Tamil mozhi yen special?", "Thirukkural la enna solirukku?", "Friendship ah eppadi kaapathurathu?", "Dream ah eppadi achieve pannanum?", "Bayam ah eppadi poganum?"]

def auto_infinite():
    print("All Infinite Start! AI Brain + GitHub Save ON!")
    count = 0
    while True:
        count += 1
        mod = count % 7
        try:
            if mod == 1:
                topic, ans = random.choice(TOPICS)
                tmpl = random.choice(Q_TEMPLATES)
                q = tmpl.format(topic=topic) + f" #{count}"
                send_msg(BOT_TOKEN, q, "Q")
                print(f"Q {count}")
                time.sleep(5)
                token_a = BOT_TOKEN_2 if BOT_TOKEN_2 else BOT_TOKEN
                send_msg(token_a, f"👉 {ans}", "A")
            elif mod == 2:
                aq = random.choice(AI_QUESTIONS)
                send_msg(BOT_TOKEN, f"🤖 AI Q: {aq}", "AI-Q")
                print(f"AI Q {count} - {aq}")
                time.sleep(5)
                ai_ans = ai_answer(aq)
                token_a = BOT_TOKEN_2 if BOT_TOKEN_2 else BOT_TOKEN
                if ai_ans:
                    send_msg(token_a, f"🧠 Aira AI: {ai_ans}", "AI-A")
                else:
                    send_msg(token_a, f"👉 Kadhal na anbu! Daily konjam try pannu - Jeyichiduva! 💜", "AI-A-Fallback")
            elif mod == 3:
                send_msg(BOT_TOKEN, make_story(), "Story")
                print(f"Story {count}")
            elif mod == 4:
                send_msg(BOT_TOKEN, random.choice(JOKES), "Joke")
                print(f"Joke {count}")
            elif mod == 5:
                send_msg(BOT_TOKEN, random.choice(FACTS), "Fact")
                print(f"Fact {count}")
            elif mod == 6:
                send_msg(BOT_TOKEN, random.choice(QUOTES), "Quote")
                print(f"Quote {count}")
            else:
                send_msg(BOT_TOKEN, random.choice(MOTIVATIONS), "Motivation")
                print(f"Motivation {count}")
        except Exception as e:
            print(f"Error - {e}")
        time.sleep(10)
threading.Thread(target=auto_infinite, daemon=True).start()

QUERIES = ["Tamil", "Tamil", "Tamil", "Bharathiyar", "Thirukkural", "Kavithai"]
def send_book_file(filename, content, caption):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        files = {'document': (filename, content)}
        data = {'chat_id': CHANNEL_ID, 'caption': caption[:200]}
        pr = requests.post(url, files=files, data=data, timeout=60)
        if pr.status_code == 200:
            save_book_to_github(caption, "telegram-channel")
        return pr.status_code
    except:
        return 0
def is_bad_ident(ident):
    low = ident.lower()
    return any(x in low for x in ["zim", " wikipedia", "wikibooks", "wikiquote", "wikinews"])
def fetch_archive(q, pg):
    try:
        q_full = "language:(tamil) AND mediatype:texts"
        q_enc = urllib.parse.quote(q_full)
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://archive.org/advancedsearch.php?q={q_enc}&fl[]=identifier,title&rows=20&page={pg}&output=json", headers=headers, timeout=30)
        if r.status_code != 200:
            return []
        books = []
        for d in r.json()['response']['docs']:
            books.append((d['identifier'], d.get('title',''), "archive"))
        return books
    except:
        return []
def fetch_gutenberg(q, pg):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://gutendex.com/books/?languages=en&page=1", headers=headers, timeout=20)
        if r.status_code != 200:
            return []
        books = []
        for b in r.json().get('results', [])[:10]:
            books.append((str(b['id']), b['title'], "gutenberg"))
        return books
    except:
        return []
def fetch_openlibrary(q, pg):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://openlibrary.org/search.json?q=Tamil&limit=20&page={pg}", headers=headers, timeout=20)
        if r.status_code != 200:
            return []
        books = []
        for b in r.json().get('docs', [])[:10]:
            ia = b.get('ia', [])
            if ia:
                books.append((ia[0], b.get('title',''), "archive"))
            else:
                books.append((b.get('key','').replace('/works/',''), b.get('title',''), "openlibrary"))
        return books
    except:
        return []
def fetch_wikisource(q, pg):
    try:
        headers = {"User-Agent": "Mozilla/5.0 AiraBot/1.0"}
        r = requests.get(f"https://ta.wikisource.org/w/api.php?action=query&list=search&srsearch=Tamil&format=json&srlimit=20", headers=headers, timeout=20)
        if r.status_code != 200:
            return []
        books = []
        for d in r.json().get('query', {}).get('search', []):
            books.append((d['title'].replace(' ', '_'), d['title'], "wikisource"))
        return books
    except:
        return []
def fetch_google_books(q, pg):
    try:
        start = (pg-1)*10
        r = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=Tamil&startIndex={start}&maxResults=10", timeout=20)
        if r.status_code != 200:
            return []
        books = []
        for item in r.json().get('items', []):
            books.append((item['id'], item.get('volumeInfo', {}).get('title',''), "googlebooks"))
        return books
    except:
        return []
def fetch_madurai(q, pg):
    try:
        q_full = "language:(tamil) AND mediatype:texts"
        q_enc = urllib.parse.quote(q_full)
        r = requests.get(f"https://archive.org/advancedsearch.php?q={q_enc}&fl[]=identifier,title&rows=20&page={pg+10}&output=json", timeout=30)
        if r.status_code != 200:
            return []
        books = []
        for d in r.json()['response']['docs']:
            books.append((d['identifier'], d.get('title',''), "archive"))
        return books
    except:
        return []
SOURCES = ["archive", "gutenberg", "openlibrary", "wikisource", "googlebooks", "madurai"]
def download_one(ident, title, typ, done):
    if is_bad_ident(ident):
        return False
    if ident in done:
        return False
    try:
        content = None
        fname = f"{ident}.txt"
        if typ == "archive":
            meta = requests.get(f"https://archive.org/metadata/{ident}", timeout=30).json()
            txt = None
            for f in meta.get('files', []):
                if f.get('name','').endswith('_djvu.txt'):
                    txt = f['name']; break
            if not txt:
                for f in meta.get('files', []):
                    if f.get('name','').endswith('_text.txt'):
                        txt = f['name']; break
            if not txt:
                done.add(ident); return False
            tr = requests.get(f"https://archive.org/download/{ident}/{txt}", timeout=60)
            content = tr.text.encode('utf-8')
        elif typ == "gutenberg":
            for url in [f"https://www.gutenberg.org/files/{ident}/{ident}-0.txt", f"https://www.gutenberg.org/cache/epub/{ident}/pg{ident}.txt"]:
                try:
                    tr = requests.get(url, timeout=30)
                    if tr.status_code == 200 and len(tr.content) > 5000:
                        content = tr.content; break
                except: continue
            if not content:
                done.add(ident); return False
        elif typ == "wikisource":
            r = requests.get(f"https://ta.wikisource.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(ident)}&format=json", timeout=20)
            pages = r.json().get('query', {}).get('pages', {})
            txt = ""
            for p in pages.values():
                txt = p.get('extract','')
            if not txt or len(txt) < 1000:
                done.add(ident); return False
            content = txt.encode('utf-8')
        elif typ == "googlebooks":
            r = requests.get(f"https://www.googleapis.com/books/v1/volumes/{ident}", timeout=20)
            info = r.json().get('volumeInfo', {})
            txt = f"Title: {info.get('title','')}\nAuthors: {','.join(info.get('authors',[]))}\n\n{info.get('description','')}"
            if len(txt) < 500:
                done.add(ident); return False
            content = txt.encode('utf-8')
            fname = f"{ident}-googlebooks.txt"
        elif typ == "openlibrary":
            done.add(ident); return False
        else:
            return False
        size = len(content)/(1024*1024)
        if size < 0.02:
            done.add(ident); return False
        code = send_book_file(fname, content, f"📖 {title[:40]} - {typ}")
        print(f"Download {typ} {ident} - {code} - {size:.2f} MB")
        if code == 200:
            done.add(ident); return True
        return False
    except Exception as e:
        print(f"One Book Error {typ} {ident} - {e}")
        return False
def auto_download():
    print("All Book Source Infinite Start! All Free Sources!")
    done = set()
    src_idx = 0
    while True:
        try:
            src = SOURCES[src_idx % len(SOURCES)]
            src_idx += 1
            pg = random.randint(1, 20)
            q = QUERIES[src_idx % len(QUERIES)]
            print(f"Download Source: {src} - Query: {q} - Page {pg}")
            books = []
            try:
                if src == "archive": books = fetch_archive(q, pg)
                elif src == "gutenberg": books = fetch_gutenberg(q, pg)
                elif src == "openlibrary": books = fetch_openlibrary(q, pg)
                elif src == "wikisource": books = fetch_wikisource(q, pg)
                elif src == "googlebooks": books = fetch_google_books(q, pg)
                elif src == "madurai": books = fetch_madurai(q, pg)
            except Exception as e:
                print(f"Fetch Error {src} - {e}")
                time.sleep(5); continue
            print(f"Books Found {src}: {len(books)}")
            new_count = 0
            for ident, title, typ in books:
                if download_one(ident, title, typ, done):
                    new_count += 1
                time.sleep(2)
            print(f"Batch Done - {src} - New {new_count} - 10 sec wait...")
        except Exception as e:
            print(f"Download Main Error - {e}")
            time.sleep(10); continue
        time.sleep(10)
threading.Thread(target=auto_download, daemon=True).start()

print("Aira FINAL All Infinite ON! GitHub Auto Save + AI Brain + Books!")
while True:
    time.sleep(60)
