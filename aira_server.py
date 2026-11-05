import threading, os, requests, time, random
from http.server import BaseHTTPRequestHandler, HTTPServer

def start_web():
    port = int(os.environ.get("PORT", 10000))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Aira Server ON! Infinite Source!")
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

# Infinite Story - Books Lines La Irunthu Create!
STORY_STARTERS = [
    "Oru oor la oru ponnu iruntha - Ava per Aira!",
    "Oru kaadu la oru singam irunthuchu!",
    "Oru oor la periya noolagam irunthuchu!",
    "Oru paiyan oru ponna love pannaan!",
    "Oru chinna paiyan daily school ku ponaan!",
    "Oru oor la mazhaiye varala!",
    "Oru bike la oru paiyan oor suthinaan!",
]
STORY_MIDDLES = [
    "Ava daily Tamil books padippanga! Oru naal magic book ah paathanga!",
    "Romba thaniya irunthuchu! Oru naal oru kili vanthuchu!",
    "1000 Tamil books irunthuchu! Oru chinna ponnu daily anga pova!",
    "Sollaa bayanthaan! Aira sonnanga 'Love ah sollidu!'",
    "Avankitta oru magic pencil irunthuchu! Athula ezhuthina ellam nija aayidum!",
    "Ellarum kastapattanga! Oru chinna paiyan kadavul kitta kettan!",
    "Vazhila oru ponna paathaan! Ava kitta help kettaan!",
]
STORY_ENDS = [
    "Aprom Aira super smart aayita! 💜",
    "Aprom rendu perum best friends aayitanga!",
    "Aprom ava periya writer aayita!",
    "Paiyan sollitaan - Ponnu 'Yes' nu sonna! 💜",
    "Aprom avan periya hero aayitaan!",
    "Oru naal periya mazhai vanthuchu - Ellarum happy!",
    "Aprom rendu perum trip poonaanga - Happy ending!",
]

def make_story():
    s = random.choice(STORY_STARTERS)
    m = random.choice(STORY_MIDDLES)
    e = random.choice(STORY_ENDS)
    return f"📖 Story: {s} {m} {e}"

TOPICS = [
    ("Kadhal", "Kadhal na anbu! Oru ponnu mela varura pure feeling! 💜"),
    ("Friendship", "Friendship na kashtathula kooda irukkura nanban!"),
    ("Thirukkural", "Agara mudhala ezhuthellam - Thiruvalluvar sonnathu!"),
    ("Bharathiyar", "Achamillai Achamillai - Bharathiyar! Courage paadal!"),
    ("Life", "Daily konjam konjam try pannu - Jeyichiduva!"),
    ("Tamil", "Tamil na namma uyir! Tamil la pesurathu perumai!"),
    ("Sad", "Paravalla! Rest edu - Song kelu - Seri aayidum!"),
    ("Happy", "Happy ah irukkanum na - Anba iru - Sirichu pesu!"),
    ("Study", "Daily 1 hour padichale pothum - Consistent ah padikalam!"),
    ("Music", "Music na manasukku marunthu! Song kelu - Relax aayiduva!"),
    ("Courage", "Bayapadaatha! Unnala mudiyum! Try pannu!"),
    ("Family", "Family thaan mukkiyam! Amma Appa va love pannu!"),
    ("Dream", "Dream ah vitratha! Daily oru step edu - Dream nija aayidum!"),
    ("Aira", "Naan Aira H1! Un friend! Un kooda eppovum iruppen! 💜"),
    ("Bike", "Bike na freedom! Wind la pora feeling super!"),
    ("Food", "Briyani na vera level! Tamil Nadu Briyani best!"),
    ("Cinema", "Cinema na emotion! Ajith, 【entity-Vijay¦canonical_name=Vijay】 padam super!"),
    ("Rain", "Mazhai na romance! Mazhai la nanaiyurathu super!"),
    ("Amma", "Amma na kadavul! Amma saapadu thaan best!"),
    ("Appa", "Appa na hero! Appa va love pannu!"),
    ("School", "School days thaan best days! Friends, fun!"),
    ("College", "College life na freedom + fun!"),
    ("Money", "Money mukkiyam - Aana anbu thaan perusu!"),
    ("Phone", "Phone la Aira irukka - Eppovum pesalam!"),
]

Q_TEMPLATES = [
    "{topic} na enna?",
    "{topic} pathi sollu",
    "{topic} la enna special?",
    "Enakku {topic} pathi theriyala - Sollu",
    "{topic} na enna artham?",
    "Hi, {topic} pathi pesalam ah?",
    "{topic} pathi oru story sollu",
    "{topic} pathi un karuthu enna?",
    "{topic} na unakku pidikkuma?",
    "{topic} pathi oru joke sollu",
]

def auto_infinite():
    print("Infinite Q+Story Start!")
    count = 0
    while True:
        count += 1
        if count % 3 == 0:
            # Infinite Story - Random Combine!
            story = make_story()
            send_msg(BOT_TOKEN, story)
            print(f"Story {count}: {story[:40]}")
            time.sleep(10)
            continue
        topic, ans = random.choice(TOPICS)
        tmpl = random.choice(Q_TEMPLATES)
        q = tmpl.format(topic=topic) + f" #{count}"
        send_msg(BOT_TOKEN, q)
        print(f"Q {count}: {q}")
        time.sleep(5)
        token_a = BOT_TOKEN_2 if BOT_TOKEN_2 else BOT_TOKEN
        send_msg(token_a, f"👉 {ans}")
        time.sleep(10)

threading.Thread(target=auto_infinite, daemon=True).start()

# Infinite Source Download - 4 Source!
def auto_download():
    print("Infinite Source Download Start!")
    done = set()
    page = 0
    sources = ["archive", "gutenberg", "madurai", "wikisource"]
    src_idx = 0
    while True:
        try:
            src = sources[src_idx % len(sources)]
            src_idx += 1
            page += 1
            print(f"Download Source: {src} - Page {page}")
            books = []
            # Source 1 - Archive.org
            if src == "archive":
                start = (page % 10) * 50
                r = requests.get(f"https://archive.org/advancedsearch.php?q=language:(tamil)&fl[]=identifier,title&rows=20&start={start}&output=json", timeout=30)
                docs = r.json()['response']['docs']
                for d in docs:
                    books.append((d['identifier'], d.get('title','')))
            # Source 2 - Gutenberg - Tamil Books
            elif src == "gutenberg":
                r = requests.get("https://gutendex.com/books/?languages=ta&page=1", timeout=30)
                for b in r.json().get('results', [])[:10]:
                    books.append((str(b['id']), b['title']))
            # Vera Source - Archive.org Marubadiyum - Safe!
            else:
                start = (page % 10) * 50
                r = requests.get(f"https://archive.org/advancedsearch.php?q=language:(tamil)&fl[]=identifier,title&rows=20&start={start}&output=json", timeout=30)
                docs = r.json()['response']['docs']
                for d in docs:
                    books.append((d['identifier'], d.get('title','')))
            for ident, title in books:
                if ident in done:
                    continue
                try:
                    # Archive.org Download
                    if src != "gutenberg":
                        meta = requests.get(f"https://archive.org/metadata/{ident}", timeout=30).json()
                        txt = None
                        for f in meta.get('files', []):
                            if f.get('name','').endswith('_djvu.txt'):
                                txt = f['name']
                                break
                        if not txt:
                            continue
                        tr = requests.get(f"https://archive.org/download/{ident}/{txt}", timeout=60)
                        content = tr.text.encode('utf-8')
                    else:
                        # Gutenberg Download
                        tr = requests.get(f"https://www.gutenberg.org/files/{ident}/{ident}-0.txt", timeout=30)
                        content = tr.content
                    size = len(content)/(1024*1024)
                    if size < 0.05:
                        continue
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                    files = {'document': (f"{ident}.txt", content)}
                    data = {'chat_id': CHANNEL_ID, 'caption': f"📖 {title[:40]} - {src}"}
                    pr = requests.post(url, files=files, data=data, timeout=60)
                    print(f"Download {src} {ident} - {pr.status_code} - {size:.2f} MB")
                    if pr.status_code == 200:
                        done.add(ident)
                except Exception as e:
                    print(f"One Book Error - {e}")
                    continue
                time.sleep(2)
        except Exception as e:
            print(f"Download Error - {e} - 30 sec wait...")
            time.sleep(30)
            continue
        print("Batch Done - 30 sec wait...")
        time.sleep(30)

threading.Thread(target=auto_download, daemon=True).start()

print("Aira FINAL Infinite Source ON!")
while True:
    time.sleep(60)
