import threading, os, requests, time, random
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

def auto_download():
    print("All Book Source Infinite Start!")
    done = set()
    page = 0
    sources = ["archive", "gutenberg", "openlibrary", "madurai", "wikisource"]
    src_idx = 0
    while True:
        try:
            src = sources[src_idx % len(sources)]
            src_idx += 1
            page += 1
            print(f"Download Source: {src} - Page {page}")
            books = []
            if src == "gutenberg":
                pg = (page % 10) + 1
                r = requests.get(f"https://gutendex.com/books/?languages=ta&page={pg}", timeout=30)
                for b in r.json().get('results', [])[:10]:
                    books.append((str(b['id']), b['title'], "gutenberg"))
            elif src == "openlibrary":
                pg = (page % 10) + 1
                r = requests.get(f"https://openlibrary.org/search.json?q=language:tam&limit=20&page={pg}", timeout=30)
                for b in r.json().get('docs', [])[:10]:
                    key = b.get('key','').replace('/works/','')
                    books.append((key, b.get('title',''), "openlibrary"))
            else:
                start = (page % 20) * 50
                r = requests.get(f"https://archive.org/advancedsearch.php?q=language:(tamil)&fl[]=identifier,title&rows=20&start={start}&output=json", timeout=30)
                for d in r.json()['response']['docs']:
                    books.append((d['identifier'], d.get('title',''), "archive"))
            print(f"Books Found {src}: {len(books)}")
            for ident, title, typ in books:
                if ident in done:
                    continue
                try:
                    content = None
                    if typ == "archive":
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
                    elif typ == "gutenberg":
                        tr = requests.get(f"https://www.gutenberg.org/files/{ident}/{ident}-0.txt", timeout=30)
                        content = tr.content
                    else:
                        continue
                    if not content:
                        continue
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
                    print(f"One Book Error {src} - {e}")
                    continue
                time.sleep(3)
        except Exception as e:
            print(f"Download Main Error - {e}")
            time.sleep(10)
            continue
        print("Batch Done - 10 sec wait...")
        time.sleep(10)

threading.Thread(target=auto_download, daemon=True).start()

print("Aira FINAL All Infinite ON!")
while True:
    time.sleep(60)
