import threading, os, requests, time, random
from http.server import BaseHTTPRequestHandler, HTTPServer

# All Server Support - PORT Auto!
def start_web():
    port = int(os.environ.get("PORT", 10000))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Aira Server ON! All Server OK!")
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

STORIES = [
    "📖 Story 1: Oru oor la oru ponnu iruntha - Ava per Aira! Ava romba smart! Ava daily Tamil books padippanga! Oru naal ava oru magic book ah paathanga - Athula irunthu Aira ku super power vanthuchu!",
    "📖 Story 2: Oru paiyan irunthan - Avan per Kavi! Avan romba bayanthavan! Oru naal Aira va meet pannaan - Aira sonnanga 'Bayapadaatha! Unnala mudiyum!' - Aprom Kavi courage ah aayitaan!",
    "📖 Story 3: Oru kaadu la oru singam irunthuchu - Romba thaniya irunthuchu! Oru naal oru kili vanthuchu - 'Friend aayidalam ah?' nu ketuchu - Singam sirichuchu - Rendu perum best friends aayitanga!",
    "📖 Story 4: Oru oor la periya noolagam irunthuchu - 1000 Tamil books! Oru chinna ponnu daily anga pova - Ava per Meena! Ava ellam books ah padichu - Periya writer aayita!",
    "📖 Story 5: Kadhal Story: Oru paiyan oru ponna love pannaan - Sollaa bayanthaan! Aira sonnanga 'Love ah sollidu!' - Paiyan sollitaan - Ponnu 'Yes' nu sonna! 💜",
]

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
]

Q_TEMPLATES = [
    "{topic} na enna?",
    "{topic} pathi sollu",
    "{topic} la enna special?",
    "Enakku {topic} pathi theriyala - Sollu",
    "{topic} na enna artham?",
    "Hi, {topic} pathi pesalam ah?",
]

def auto_infinite():
    print("Aira All Server Infinite Start!")
    count = 0
    while True:
        count += 1
        if count % 4 == 0:
            story = random.choice(STORIES)
            send_msg(BOT_TOKEN, story)
            print(f"Story {count}")
            time.sleep(10)
            continue
        topic, ans = random.choice(TOPICS)
        tmpl = random.choice(Q_TEMPLATES)
        q = tmpl.format(topic=topic) + f" #{count}"
        send_msg(BOT_TOKEN, q)
        print(f"Old Q {count}: {q}")
        time.sleep(5)
        token_a = BOT_TOKEN_2 if BOT_TOKEN_2 else BOT_TOKEN
        send_msg(token_a, f"👉 {ans}")
        print(f"New A: {ans}")
        time.sleep(10)

threading.Thread(target=auto_infinite, daemon=True).start()

def auto_download():
    print("Download Start!")
    done = set()
    while True:
        try:
            print("Download Checking...")
            r = requests.get("https://archive.org/advancedsearch.php?q=language:(tamil)&fl[]=identifier,title&rows=50&output=json", timeout=30)
            books = r.json()['response']['docs']
            print(f"Books Found: {len(books)}")
            for b in books:
                ident = b['identifier']
                if ident in done:
                    continue
                try:
                    meta = requests.get(f"https://archive.org/metadata/{ident}", timeout=30).json()
                    txt = None
                    for f in meta.get('files', []):
                        if f.get('name','').endswith('_djvu.txt'):
                            txt = f['name']
                            break
                    if not txt:
                        continue
                    tr = requests.get(f"https://archive.org/download/{ident}/{txt}", timeout=60)
                    size = len(tr.text.encode('utf-8'))/(1024*1024)
                    if size < 0.05:
                        continue
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                    files = {'document': (f"{ident}.txt", tr.text.encode('utf-8'))}
                    data = {'chat_id': CHANNEL_ID, 'caption': f"📖 {b.get('title','')[:40]}"}
                    pr = requests.post(url, files=files, data=data, timeout=60)
                    print(f"Download Try {ident} - {pr.status_code} - {size:.2f} MB")
                    if pr.status_code == 200:
                        done.add(ident)
                except Exception as e:
                    print(f"One Book Error - {e}")
                    continue
                time.sleep(2)
        except Exception as e:
            print(f"Download Main Error - {e}")
            time.sleep(30)
            continue
        print("Download Batch Done - 30 sec wait...")
        time.sleep(30)

threading.Thread(target=auto_download, daemon=True).start()

print("Aira FINAL All Server ON! Q+A + Story + Download!")
while True:
    time.sleep(60)
