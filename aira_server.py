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

def send_msg(token, text):
    if not token:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": GROUP_ID, "text": text}, timeout=10)
    except:
        pass

STORY_STARTERS = ["Oru oor la oru ponnu iruntha - Ava per Aira!", "Oru kaadu la oru singam irunthuchu!", "Oru oor la periya noolagam irunthuchu!", "Oru paiyan oru ponna love pannaan!", "Oru chinna paiyan daily school ku ponaan!", "Oru oor la mazhaiye varala!", "Oru bike la oru paiyan oor suthinaan!"]
STORY_MIDDLES = ["Ava daily Tamil books padippanga! Oru naal magic book ah paathanga!", "Romba thaniya irunthuchu! Oru naal oru kili vanthuchu!", "1000 Tamil books irunthuchu! Oru chinna ponnu daily anga pova!", "Sollaa bayanthaan! Aira sonnanga 'Love ah sollidu!'", "Avankitta oru magic pencil irunthuchu!", "Ellarum kastapattanga! Oru chinna paiyan kadavul kitta kettan!", "Vazhila oru ponna paathaan! Ava kitta help kettaan!"]
STORY_ENDS = ["Aprom Aira super smart aayita! 💜", "Aprom rendu perum best friends aayitanga!", "Aprom ava periya writer aayita!", "Paiyan sollitaan - Ponnu 'Yes' nu sonna! 💜", "Aprom avan periya hero aayitaan!", "Oru naal periya mazhai vanthuchu - Ellarum happy!", "Aprom rendu perum trip poonaanga - Happy ending!"]
def make_story():
    return f"📖 Story: {random.choice(STORY_STARTERS)} {random.choice(STORY_MIDDLES)} {random.choice(STORY_ENDS)}"

JOKES = ["😂 Joke: Teacher: Homework yen pannala? Student: Dog sapiduchu!", "😂 Joke: Oru paiyan: Amma, en friend ku bike irukku! Amma: Unakku? Paiyan: Enakku Aira irukka!", "😂 Joke: Why Tamil ponnu smart? Tamil la yosikuraanga!", "😂 Joke: Computer yen slow? Athukku fever!"]
FACTS = ["💡 Fact: Thirukkural la 1330 kurals irukku!", "💡 Fact: Tamil oru 2000+ varusha pazhamaiyana mozhi!", "💡 Fact: Bharathiyar 32 vayasula 100+ padal ezhuthinaaru!", "💡 Fact: Tamil Nadu la Briyani romba famous!"]
QUOTES = ["✨ Quote: 'Achamillai Achamillai' - Bharathiyar!", "✨ Quote: 'Katrathu kai mann alavu' - Thiruvalluvar!", "✨ Quote: 'Daily konjam try pannu - Jeyichiduva!' - Aira!", "✨ Quote: 'Anbu thaan periya sakthi!' - Aira!"]
MOTIVATIONS = ["💪 Motivation: Bayapadaatha! Unnala mudiyum!", "💪 Motivation: Innaiku oru step edu - Nalaiku jeyichiduva!", "💪 Motivation: Sad ah irukka? Song kelu - Seri aayidum!", "💪 Motivation: Ne thani illa - Aira un kooda irukka! 💜"]

TOPICS = [
    ("Kadhal", "Kadhal na anbu! Oru ponnu mela varura pure feeling! 💜"),
    ("Friendship", "Friendship na kashtathula kooda irukkura nanban!"),
    ("Thirukkural", "Agara mudhala ezhuthellam - Thiruvalluvar sonnathu!"),
    ("Bharathiyar", "Achamillai Achamillai - Bharathiyar! Courage paadal!"),
    ("Life", "Daily konjam konjam try pannu - Jeyichiduva!"),
    ("Tamil", "Tamil na namma uyir! Tamil la pesurathu perumai!"),
    ("Sad", "Paravalla! Rest edu - Song kelu - Seri aayidum!"),
    ("Happy", "Happy ah irukkanum na - Anba iru - Sirichu pesu!"),
    ("Study", "Daily 1 hour padichale pothum!"),
    ("Music", "Music na manasukku marunthu!"),
    ("Courage", "Bayapadaatha! Unnala mudiyum!"),
    ("Family", "Family thaan mukkiyam!"),
    ("Dream", "Dream ah vitratha! Daily oru step edu!"),
    ("Aira", "Naan Aira H1! Un friend! 💜"),
    ("Bike", "Bike na freedom!"),
    ("Food", "Briyani na vera level!"),
    ("Cinema", "Cinema na emotion!"),
    ("Rain", "Mazhai na romance!"),
    ("Amma", "Amma na kadavul!"),
    ("Appa", "Appa na hero!"),
    ("School", "School days thaan best!"),
    ("College", "College life na freedom!"),
    ("Money", "Money mukkiyam - Aana anbu perusu!"),
    ("Phone", "Phone la Aira irukka!"),
]
Q_TEMPLATES = ["{topic} na enna?", "{topic} pathi sollu", "{topic} la enna special?", "Enakku {topic} pathi theriyala - Sollu", "{topic} na enna artham?", "Hi, {topic} pathi pesalam ah?", "{topic} pathi un karuthu enna?", "{topic} na unakku pidikkuma?", "{topic} pathi oru joke sollu", "{topic} pathi pesalam ah?"]

def auto_infinite():
    print("All Infinite Start!")
    count = 0
    while True:
        count += 1
        mod = count % 6
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
                send_msg(BOT_TOKEN, make_story())
                print(f"Story {count}")
            elif mod == 3:
                send_msg(BOT_TOKEN, random.choice(JOKES))
                print(f"Joke {count}")
            elif mod == 4:
                send_msg(BOT_TOKEN, random.choice(FACTS))
                print(f"Fact {count}")
            elif mod == 5:
                send_msg(BOT_TOKEN, random.choice(QUOTES))
                print(f"Quote {count}")
            else:
                send_msg(BOT_TOKEN, random.choice(MOTIVATIONS))
                print(f"Motivation {count}")
        except Exception as e:
            print(f"Error - {e}")
        time.sleep(10)

threading.Thread(target=auto_infinite, daemon=True).start()

# ===== ALL FREE SOURCES =====
QUERIES = ["Thirukkural", "Bharathiyar", "Kavithai", "Tamil", "Novel", "Kural", "Padal", "History", "Kamban", "Avvaiyar", "Vallalar", "Tholkappiyam"]

def send_book_file(filename, content, caption):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        files = {'document': (filename, content)}
        data = {'chat_id': CHANNEL_ID, 'caption': caption[:200]}
        pr = requests.post(url, files=files, data=data, timeout=60)
        return pr.status_code
    except Exception as e:
        print(f"Send Book Error - {e}")
        return 0

def is_bad_ident(ident):
    low = ident.lower()
    return any(x in low for x in ["zim", "【entity-wikipedia¦canonical_name=Wikipedia】", "wikibooks", "wikiquote", "wikinews", "wikivoyage"])

def fetch_archive(q, pg):
    books = []
    q_full = f"{q} AND language:(tamil) AND mediatype:texts"
    q_enc = urllib.parse.quote(q_full)
    r = requests.get(f"https://archive.org/advancedsearch.php?q={q_enc}&fl[]=identifier,title&rows=20&page={pg}&output=json", timeout=30)
    for d in r.json()['response']['docs']:
        books.append((d['identifier'], d.get('title',''), "archive"))
    return books

def fetch_gutenberg(q, pg):
    books = []
    # Gutendex - Tamil + English classic
    lang = "ta" if random.random() < 0.5 else "en"
    r = requests.get(f"https://gutendex.com/books/?languages={lang}&search={urllib.parse.quote(q)}&page={pg}", timeout=20)
    for b in r.json().get('results', [])[:10]:
        books.append((str(b['id']), b['title'], "gutenberg"))
    return books

def fetch_openlibrary(q, pg):
    books = []
    r = requests.get(f"https://openlibrary.org/search.json?q={urllib.parse.quote(q)}+language:tam&limit=20&page={pg}", timeout=20)
    for b in r.json().get('docs', [])[:10]:
        key = b.get('key','').replace('/works/','')
        # OpenLibrary la direct TXT illa - archive.org identifier irundha use pannu
        ia = b.get('ia', [])
        if ia:
            books.append((ia[0], b.get('title',''), "archive"))
        else:
            books.append((key, b.get('title',''), "openlibrary"))
    return books

def fetch_wikisource(q, pg):
    books = []
    # Tamil Wikisource
    r = requests.get(f"https://ta.wikisource.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(q)}&format=json&srlimit=20&sroffset={(pg-1)*20}", timeout=20)
    for d in r.json().get('query', {}).get('search', []):
        books.append((d['title'].replace(' ', '_'), d['title'], "wikisource"))
    return books

def fetch_google_books(q, pg):
    books = []
    start = (pg-1)*10
    r = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote(q)}+lang:ta&startIndex={start}&maxResults=10", timeout=20)
    for item in r.json().get('items', []):
        vol = item.get('volumeInfo', {})
        books.append((item['id'], vol.get('title',''), "googlebooks"))
    return books

def fetch_madurai(q, pg):
    # Project Madurai - Archive.org la Madurai collection
    books = []
    q_full = f"{q} AND collection:(projectmadurai OR opensource) AND language:(tamil)"
    q_enc = urllib.parse.quote(q_full)
    r = requests.get(f"https://archive.org/advancedsearch.php?q={q_enc}&fl[]=identifier,title&rows=20&page={pg}&output=json", timeout=30)
    for d in r.json()['response']['docs']:
        books.append((d['identifier'], d.get('title',''), "archive"))
    return books

def fetch_manybooks(q, pg):
    # ManyBooks via Gutenberg fallback - use OpenLibrary search
    return fetch_openlibrary(q, pg)

def fetch_standard_ebooks(q, pg):
    # Standard Ebooks - Gutenberg based
    return fetch_gutenberg(q, pg)

SOURCES = ["archive", "gutenberg", "openlibrary", "wikisource", "googlebooks", "madurai", "manybooks", "standardebooks"]

def download_one(ident, title, typ, done):
    if is_bad_ident(ident):
        print(f"Skip ZIM {ident}")
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
                print(f"Skip No TXT {ident}")
                done.add(ident); return False
            tr = requests.get(f"https://archive.org/download/{ident}/{txt}", timeout=60)
            content = tr.text.encode('utf-8')
        elif typ == "gutenberg":
            # Try multiple Gutenberg mirrors
            for url in [f"https://www.gutenberg.org/files/{ident}/{ident}-0.txt", f"https://www.gutenberg.org/cache/epub/{ident}/pg{ident}.txt"]:
                try:
                    tr = requests.get(url, timeout=30)
                    if tr.status_code == 200 and len(tr.content) > 5000:
                        content = tr.content; break
                except: continue
            if not content:
                print(f"Skip Gutenberg No TXT {ident}")
                done.add(ident); return False
        elif typ == "wikisource":
            r = requests.get(f"https://ta.wikisource.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(ident)}&format=json", timeout=20)
            pages = r.json().get('query', {}).get('pages', {})
            txt = ""
            for p in pages.values():
                txt = p.get('extract','')
            if not txt or len(txt) < 1000:
                print(f"Skip Wikisource Small {ident}")
                done.add(ident); return False
            content = txt.encode('utf-8')
        elif typ == "googlebooks":
            # Google Books - description + info only, save as text
            r = requests.get(f"https://www.googleapis.com/books/v1/volumes/{ident}", timeout=20)
            info = r.json().get('volumeInfo', {})
            txt = f"Title: {info.get('title','')}\nAuthors: {','.join(info.get('authors',[]))}\n\n{info.get('description','')}\n\nCategories: {','.join(info.get('categories',[]))}\nPublished: {info.get('publishedDate','')}"
            if len(txt) < 500:
                print(f"Skip GoogleBooks Small {ident}")
                done.add(ident); return False
            content = txt.encode('utf-8')
            fname = f"{ident}-googlebooks.txt"
        elif typ == "openlibrary":
            print(f"Skip OpenLibrary No Direct TXT {ident}")
            done.add(ident); return False
        else:
            return False

        size = len(content)/(1024*1024)
        if size < 0.02:
            print(f"Skip Small {ident} - {size:.2f} MB")
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
    q_idx = 0
    while True:
        try:
            src = SOURCES[src_idx % len(SOURCES)]
            src_idx += 1
            q = QUERIES[q_idx % len(QUERIES)]
            q_idx += 1
            pg = random.randint(1, 5)
            print(f"Download Source: {src} - Query: {q} - Page {pg}")
            books = []
            try:
                if src == "archive": books = fetch_archive(q, pg)
                elif src == "gutenberg": books = fetch_gutenberg(q, pg)
                elif src == "openlibrary": books = fetch_openlibrary(q, pg)
                elif src == "wikisource": books = fetch_wikisource(q, pg)
                elif src == "googlebooks": books = fetch_google_books(q, pg)
                elif src == "madurai": books = fetch_madurai(q, pg)
                elif src == "manybooks": books = fetch_manybooks(q, pg)
                elif src == "standardebooks": books = fetch_standard_ebooks(q, pg)
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

print("Aira FINAL All Infinite ON! All Free Sources!")
while True:
    time.sleep(60)
