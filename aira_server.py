import threading, os, requests, time, random, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

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

def send_msg(token, text):
    if not token:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": GROUP_ID, "text": text}, timeout=10)
    except:
        pass

# ===== AI BRAIN - NEW MODELS - 404 FIX =====
def ai_answer(question):
    # Groq - NEW MODEL llama-3.3-70b-versatile
    for key, name in [(GROQ_1, "Groq1"), (GROQ_2, "Groq2"), (GROQ_3, "Groq3")]:
        if not key:
            continue
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Ne Aira H1, Tamil Tanglish la pesura cute friend. Short ah 2-3 lines la anba answer pannu."}, {"role": "user", "content": question}]},
                timeout=20)
            if r.status_code == 200:
                ans = r.json()['choices'][0]['message']['content']
                print(f"AI Answer - {name} - OK")
                return ans[:500]
            else:
                print(f"AI Fail {name} - {r.status_code} - {r.text[:100]}")
        except Exception as e:
            print(f"AI Error {name} - {e}")
            continue
    # Gemini - NEW MODEL gemini-2.0-flash
    for key, name in [(GEMINI_1, "Gemini1"), (GEMINI_2, "Gemini2")]:
        if not key:
            continue
        try:
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
                json={"contents": [{"parts": [{"text": f"Ne Aira H1, Tamil Tanglish la cute friend. Short ah 2-3 lines la answer pannu. Question: {question}"}]}]}, timeout=20)
            if r.status_code == 200:
                ans = r.json()['candidates'][0]['content']['parts'][0]['text']
                print(f"AI Answer - {name} - OK")
                return ans[:500]
            else:
                print(f"AI Fail {name} - {r.status_code} - {r.text[:100]}")
        except Exception as e:
            print(f"AI Error {name} - {e}")
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
    print("All Infinite Start! AI Brain 5 Keys ON! New Models!")
    count = 0
    while True:
        count += 1
        mod = count % 7
        try:
            if mod == 1:
                topic, ans = random.choice(TOPICS)
                tmpl = random.choice(Q_TEMPLATES)
                q = tmpl.format(topic=topic) + f" #{count}"
                send_msg(BOT_TOKEN, q)
                print(f"Q {count}")
                time.sleep(5)
                token_a = BOT_TOKEN_2 if BOT_TOKEN_2 else BOT_TOKEN
                send_msg(token_a, f"👉 {ans}")
            elif mod == 2:
                aq = random.choice(AI_QUESTIONS)
                send_msg(BOT_TOKEN, f"🤖 AI Q: {aq}")
                print(f"AI Q {count} - {aq}")
                time.sleep(5)
                ai_ans = ai_answer(aq)
                token_a = BOT_TOKEN_2 if BOT_TOKEN_2 else BOT_TOKEN
                if ai_ans:
                    send_msg(token_a, f"🧠 Aira AI: {ai_ans}")
                else:
                    send_msg(token_a, f"👉 Kadhal na anbu! Daily konjam try pannu - Jeyichiduva! 💜")
            elif mod == 3:
                send_msg(BOT_TOKEN, make_story())
                print(f"Story {count}")
            elif mod == 4:
                send_msg(BOT_TOKEN, random.choice(JOKES))
                print(f"Joke {count}")
            elif mod == 5:
                send_msg(BOT_TOKEN, random.choice(FACTS))
                print(f"Fact {count}")
            elif mod == 6:
                send_msg(BOT_TOKEN, random.choice(QUOTES))
                print(f"Quote {count}")
            else:
                send_msg(BOT_TOKEN, random.choice(MOTIVATIONS))
                print(f"Motivation {count}")
        except Exception as e:
            print(f"Error - {e}")
        time.sleep(10)
threading.Thread(target=auto_infinite, daemon=True).start()

# BOOKS - Broad Query Fix - 0 Varathu!
QUERIES = ["Tamil", "Tamil", "Tamil", "Bharathiyar", "Thirukkural", "Kavithai"]
def send_book_file(filename, content, caption):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        files = {'document': (filename, content)}
        data = {'chat_id': CHANNEL_ID, 'caption': caption[:200]}
        pr = requests.post(url, files=files, data=data, timeout=60)
        return pr.status_code
    except:
        return 0
def is_bad_ident(ident):
    low = ident.lower()
    return any(x in low for x in ["zim", " wikipedia", "wikibooks", "wikiquote", "wikinews"])
def fetch_archive(q, pg):
    try:
        # Broad - language mattum - Query specific illa - 0 varaathu!
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
            print(f"Gutenberg Skip - Status {r.status_code}")
            return []
        books = []
        for b in r.json().get('results', [])[:10]:
            books.append((str(b['id']), b['title'], "gutenberg"))
        return books
    except Exception as e:
        print(f"Gutenberg Error - {e}")
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
    pg_counter = 1
    while True:
        try:
            src = SOURCES[src_idx % len(SOURCES)]
            src_idx += 1
            pg_counter += 1
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

print("Aira FINAL All Infinite ON! New Models + Broad Books!")
while True:
    time.sleep(60)
