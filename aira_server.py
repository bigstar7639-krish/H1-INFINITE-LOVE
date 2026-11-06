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

QUERIES = [
    "language:(tamil) AND mediatype:texts AND title:(Thirukkural*)",
    "language:(tamil) AND mediatype:texts AND title:(Bharathiyar*)",
    "language:(tamil) AND mediatype:texts AND title:(Tamil*)",
    "language:(tamil) AND mediatype:texts AND title:(Kavithai*)",
    "language:(tamil) AND mediatype:texts AND title:(Novel*)",
    "language:(tamil) AND mediatype:texts AND title:(History*)",
    "language:(tamil) AND mediatype:texts AND title:(Kural*)",
    "language:(tamil) AND mediatype:texts AND title:(Padal*)",
]

def auto_download():
    print("All Book Source Infinite Start!")
    done = set()
    q_idx = 0
    while True:
        try:
            q_raw = QUERIES[q_idx % len(QUERIES)]
            q_idx += 1
            pg = random.randint(1, 5)
            q_enc = urllib.parse.quote(q_raw)
            print(f"Download Query: {q_raw} - Page {pg}")
            r = requests.get(f"https://archive.org/advancedsearch.php?q={q_enc}&fl[]=identifier,title&rows=20&page={pg}&output=json", timeout=30)
            books = r.json()['response']['docs']
            print(f"Books Found: {len(books)}")
            new_count = 0
            for b in books:
                ident = b['identifier']
                low = ident.lower()
                if "zim" in low or "wikipedia" in low or "wikibooks" in low or "wikiquote" in low or "wikinews" in low:
                    print(f"Skip ZIM {ident}")
                    continue
                if ident in done:
                    print(f"Skip Already Done {ident}")
                    continue
                try:
                    meta = requests.get(f"https://archive.org/metadata/{ident}", timeout=30).json()
                    txt = None
                    for f in meta.get('files', []):
                        name = f.get('name','')
                        if name.endswith('_djvu.txt'):
                            txt = name
                            break
                    if not txt:
                        for f in meta.get('files', []):
                            name = f.get('name','')
                            if name.endswith('_text.txt'):
                                txt = name
                                break
                    if not txt:
                        print(f"Skip No TXT {ident}")
                        done.add(ident)
                        continue
                    tr = requests.get(f"https://archive.org/download/{ident}/{txt}", timeout=60)
                    content = tr.text.encode('utf-8')
                    size = len(content)/(1024*1024)
                    if size < 0.05:
                        print(f"Skip Small {ident} - {size:.2f} MB")
                        done.add(ident)
                        continue
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                    files = {'document': (f"{ident}.txt", content)}
                    data = {'chat_id': CHANNEL_ID, 'caption': f"📖 {b.get('title','')[:40]}"}
                    pr = requests.post(url, files=files, data=data, timeout=60)
                    print(f"Download {ident} - {pr.status_code} - {size:.2f} MB")
                    if pr.status_code == 200:
                        done.add(ident)
                        new_count += 1
                except Exception as e:
                    print(f"One Book Error {ident} - {e}")
                    continue
                time.sleep(2)
            print(f"Batch Done - New {new_count} - 10 sec wait...")
        except Exception as e:
            print(f"Download Main Error - {e}")
            time.sleep(10)
            continue
        time.sleep(10)

threading.Thread(target=auto_download, daemon=True).start()

print("Aira FINAL All Infinite ON! Query Rotate + ZIM Filter!")
while True:
    time.sleep(60)
