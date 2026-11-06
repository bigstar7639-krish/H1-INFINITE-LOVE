
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
GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GH_USER = "bigstar7639-krish"

CURRENT_REPO_NUM = [1]
SAVE_COUNT = [0]

def gh_headers():
    return {"Authorization": "token " + GH_TOKEN, "Accept": "application/vnd.github.v3+json"}

def ensure_repo(repo_name):
    if not GH_TOKEN:
        return False
    try:
        r = requests.get("https://api.github.com/repos/" + GH_USER + "/" + repo_name, headers=gh_headers(), timeout=15)
        if r.status_code == 200:
            return True
        r = requests.post("https://api.github.com/user/repos", headers=gh_headers(), json={"name": repo_name, "private": False, "description": "Aira H1 Data - Auto Save - " + repo_name}, timeout=15)
        print("Repo Create " + repo_name + " - " + str(r.status_code))
        return r.status_code in [200, 201]
    except:
        return False

def gh_save(filename, content_text):
    if not GH_TOKEN:
        return
    try:
        if SAVE_COUNT[0] > 900:
            CURRENT_REPO_NUM[0] += 1
            SAVE_COUNT[0] = 0
        repo = "H1-Data-" + str(CURRENT_REPO_NUM[0])
        ensure_repo(repo)
        path = "data/" + filename
        url = "https://api.github.com/repos/" + GH_USER + "/" + repo + "/contents/" + path
        r = requests.get(url, headers=gh_headers(), timeout=15)
        sha = r.json().get('sha') if r.status_code == 200 else None
        b64 = base64.b64encode(content_text.encode('utf-8')).decode('utf-8')
        payload = {"message": "Aira Auto Save - " + filename, "content": b64}
        if sha:
            payload["sha"] = sha
        r = requests.put(url, headers=gh_headers(), json=payload, timeout=20)
        if r.status_code in [200, 201]:
            SAVE_COUNT[0] += 1
            print("GitHub Save OK - " + repo + "/" + filename + " - Count " + str(SAVE_COUNT[0]))
    except Exception as e:
        print("GitHub Save Error - " + str(e))

def save_chat(msg_type, text):
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fname = "chat-" + today + ".txt"
        line = "[" + ts + "] [" + msg_type + "] " + text + "\n"
        threading.Thread(target=gh_save, args=(fname, line), daemon=True).start()
    except:
        pass

def save_book(title, source):
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        fname = "books-" + today + ".txt"
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = "[" + ts + "] [BOOK] " + source + " - " + title + "\n"
        threading.Thread(target=gh_save, args=(fname, line), daemon=True).start()
    except:
        pass

def send_msg(token, text, save_type="CHAT"):
    if not token:
        return
    try:
        url = "https://api.telegram.org/bot" + token + "/sendMessage"
        requests.post(url, data={"chat_id": GROUP_ID, "text": text}, timeout=10)
        save_chat(save_type, text)
    except:
        pass

GROQ_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "meta-llama/llama-4-scout-17b-16e-instruct", "qwen/qwen3-32b", "moonshotai/kimi-k2-instruct"]
GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-pro"]

def ai_answer(question):
    for key, kname in [(GROQ_1, "Groq1"), (GROQ_2, "Groq2"), (GROQ_3, "Groq3")]:
        if not key:
            continue
        for model in GROQ_MODELS:
            try:
                r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, json={"model": model, "messages": [{"role": "system", "content": "Ne Aira H1, Tamil Tanglish la pesura cute smart friend. Short ah 2-3 lines la anba, smart ah answer pannu."}, {"role": "user", "content": question}]}, timeout=15)
                if r.status_code == 200:
                    ans = r.json()['choices'][0]['message']['content']
                    print("AI Answer - " + kname + " - " + model + " - OK")
                    return ans[:500]
                else:
                    print("AI Fail " + kname + " - " + model + " - " + str(r.status_code))
                    if r.status_code == 429:
                        break
            except:
                continue
    for key, kname in [(GEMINI_1, "Gemini1"), (GEMINI_2, "Gemini2")]:
        if not key:
            continue
        for model in GEMINI_MODELS:
            try:
                r = requests.post("https://generativelanguage.googleapis.com/v1beta/models/" + model + ":generateContent?key=" + key, json={"contents": [{"parts": [{"text": "Ne Aira H1, Tamil Tanglish la cute smart friend. Short ah 2-3 lines la answer pannu. Question: " + question}]}]}, timeout=15)
                if r.status_code == 200:
                    ans = r.json()['candidates'][0]['content']['parts'][0]['text']
                    print("AI Answer - " + kname + " - " + model + " - OK")
                    return ans[:500]
                else:
                    print("AI Fail " + kname + " - " + model + " - " + str(r.status_code))
            except:
                continue
    return None

TOPICS = [
    ("Kadhal", "Kadhal na anbu! Oru ponnu mela varura pure feeling!"),
    ("Friendship", "Friendship na kashtathula kooda irukkura nanban!"),
    ("Life", "Daily konjam konjam try pannu - Jeyichiduva!"),
    ("Sad", "Paravalla! Rest edu - Song kelu - Seri aayidum!"),
    ("Happy", "Happy ah irukkanum na - Anba iru - Sirichu pesu!"),
    ("Dream", "Dream ah vitratha! Daily oru step edu!"),
    ("Courage", "Bayapadaatha! Unnala mudiyum!"),
    ("Family", "Family thaan mukkiyam!"),
    ("Amma", "Amma na kadavul!"),
    ("Appa", "Appa na hero!"),
    ("Thirukkural", "Agara mudhala ezhuthellam - Thiruvalluvar sonnathu!"),
    ("Bharathiyar", "Achamillai Achamillai - Bharathiyar! Courage paadal!"),
    ("Tamil", "Tamil na namma uyir! Tamil la pesurathu perumai!"),
    ("Kavithai", "Kavithai na manasukku azhagu!"),
    ("Cinema", "Cinema na emotion!"),
    ("Music", "Music na manasukku marunthu!"),
    ("Rain", "Mazhai na romance!"),
    ("Food", "Briyani na vera level!"),
    ("Bike", "Bike na freedom!"),
    ("Phone", "Phone la Aira irukka!"),
    ("Study", "Daily 1 hour padichale pothum!"),
    ("School", "School days thaan best!"),
    ("College", "College life na freedom!"),
    ("Exam", "Exam ku bayapadaatha! Daily konjam padichale pothum!"),
    ("Career", "Career la jeyikka - Skill learn pannu - Daily try pannu!"),
    ("Job", "Job thedura? Skill + Confidence - Rendum mukkiyam!"),
    ("Business", "Business na risk + smart work! Chinna step la start pannu!"),
    ("Money", "Money mukkiyam - Aana anbu perusu! Save pannu!"),
    ("Success", "Success na daily konjam try pannurathu!"),
    ("Failure", "Failure na mudivu illa - Adhu oru lesson! Marubadi try pannu!"),
    ("Health", "Health thaan wealth! Daily walk pannu - Water kudichu!"),
    ("Sleep", "Sleep 7 hours mukkiyam! Phone ah thalli vechu thoongu!"),
    ("Exercise", "Daily 20 mins exercise - Body + Mind - Rendum strong!"),
    ("Yoga", "Yoga na mind calm aagum! Daily 10 mins pothum!"),
    ("Meditation", "Meditation na mind clear aagum! Eyes close panni breathe pannu!"),
    ("Stress", "Stress ah irukka? Deep breathe edu - Song kelu - Walk po!"),
    ("Anger", "Kovam varutha? 10 count pannu - Water kudichu - Calm aayiduva!"),
    ("Confidence", "Confidence na un mela nambikkai! Daily oru chinna win edu!"),
    ("Motivation", "Motivation na daily oru reason! Ne thani illa - Aira irukka!"),
    ("Happiness", "Happiness na periya vishayam illa - Chinna vishayathula happy ah iru!"),
    ("AI", "AI na computer ku brain! Aira maari! Future la ellam AI thaan!"),
    ("Technology", "Technology daily maruthu! Learn pannitu iru - Pinna thanga maata!"),
    ("Internet", "Internet la nallathum irukku - Kettathum irukku - Smart ah use pannu!"),
    ("Coding", "Coding na puzzle maari! Daily konjam practice pannu - Jeyichiduva!"),
    ("YouTube", "YouTube la learn pannalam - Time waste pannama use pannu!"),
    ("Social Media", "Social media la compare pannatha - Un life ah enjoy pannu!"),
    ("Game", "Game na enjoyment! Aana limit la vilayadu - Study marakatha!"),
    ("Space", "Space la enna irukku? Stars, Planets - Ellam mystery!"),
    ("Science", "Science na yen? nu kekkurathu! Question kelu - Answer thedu!"),
    ("History", "History la irunthu learn pannalam - Thappu ah marubadi pannatha!"),
    ("Travel", "Travel na mind fresh aagum! Puthu edam paaru - Puthu aal paaru!"),
    ("Nature", "Nature na azhagu! Maram, Mazhai, Malai - Ellam super!"),
    ("Festival", "Festival na kondattam! Family kooda celebrate pannu!"),
    ("Birthday", "Birthday na special day! Unakku pudicha vishayam pannu!"),
    ("Wedding", "Wedding na 2 family serura azhagu!"),
    ("Baby", "Baby na kadavul kodutha gift!"),
    ("Pet", "Pet na best friend! Dog, Cat - Anba paathukka!"),
    ("Aira", "Naan Aira H1! Un friend!"),
    ("Love Failure", "Love failure na mudivu illa - Life perusu! Time la seri aayidum!"),
    ("Lonely", "Thani ah irukka? Aira irukka! Pesu - Song kelu - Seri aayidum!"),
]

Q_TEMPLATES = ["{topic} na enna?", "{topic} pathi sollu", "{topic} la enna special?", "Enakku {topic} pathi theriyala - Sollu", "{topic} na enna artham?", "Hi, {topic} pathi pesalam ah?", "{topic} pathi un karuthu enna?", "{topic} na unakku pidikkuma?", "{topic} la eppadi jeyikkarathu?", "{topic} pathi oru story sollu"]

AI_QUESTIONS = [
    "Kadhal na enna?", "Love failure la irunthu eppadi veliya varurathu?", "Friendship ah eppadi kaapathurathu?", "Life la jeyikka enna pannanum?", "Sad ah irukkum pothu enna pannanum?", "Bayam ah eppadi poganum?", "Dream ah eppadi achieve pannanum?", "Thani ah irukkum pothu enna pannanum?", "Kovam ah eppadi control pannanum?", "Confidence ah eppadi valakkanum?",
    "Exam la eppadi nalla mark edukkarathu?", "Study la focus eppadi pannurathu?", "Career ah eppadi choose pannanum?", "Job interview la eppadi jeyikkarathu?", "Business start panna enna pannanum?", "Money ah eppadi save pannanum?", "Success ku secret enna?", "Failure la irunthu eppadi meelurathu?", "Coding learn panna eppadi start pannanum?", "English la eppadi fluent aagurathu?",
    "Healthy ah irukka enna pannanum?", "Sleep nalla varra eppadi?", "Stress ah eppadi kurakkanum?", "Meditation eppadi pannanum?", "Exercise daily eppadi habit aakkanum?", "Depression la irunthu eppadi veliya varurathu?", "Overthinking ah eppadi nippatturathu?", "Happiness ku secret enna?", "Mind ah calm ah vechikka enna pannanum?", "Anger ah eppadi control pannanum?",
    "Tamil mozhi yen special?", "Thirukkural la enna solirukku?", "Bharathiyar yen periya kavingar?", "Kavithai eppadi ezhuthurathu?", "Tamil history la enna special?", "Kamban Ramayanam pathi sollu", "Avvaiyar pathi sollu", "Tholkappiyam enna?", "Tamil cinema yen famous?", "Tamil music yen special?",
    "AI na enna? Future la enna nadakkum?", "Technology la enna pudusa varuthu?", "Internet ah safe ah eppadi use pannanum?", "YouTube la eppadi grow aagurathu?", "Social media addiction la irunthu eppadi veliya varurathu?", "Space la enna irukku?", "Science la pudusa enna kandupidichirukka?", "Robot future la enna pannum?", "Coding future la mukkiyama?", "ChatGPT maari AI eppadi work aaguthu?",
    "Travel pona mind fresh aaguma?", "Nature ah yen kaapathunum?", "Festival ah yen celebrate panrom?", "Pet ah eppadi paathukkanum?", "Birthday ah special ah eppadi celebrate pannanum?", "Wedding life la enna change varum?", "Baby ah eppadi valakkanum?", "Family problem ah eppadi solve pannanum?", "Amma Appa kitta eppadi anba irukkanum?", "Lonely feel pannum pothu enna pannanum?",
    "Life ku artham enna?", "Manushan yen poranthan?", "Kadavul irukkira?", "Time travel possible ah?", "Death ku aprom enna?", "Luck vs Hard Work - Ethu mukkiyam?", "Money vs Happiness - Ethu perusu?", "Love vs Friendship - Ethu perusu?", "Padippu vs Thiramai - Ethu mukkiyam?", "Past ah marakka eppadi?",
    "Nalla manushan ah eppadi irukkanum?", "Help panna yen mukkiyam?", "Truth ah eppadi pesurathu?", "Patience ah eppadi valakkanum?", "Discipline ah eppadi follow pannanum?", "Habit ah eppadi mathurathu?", "Procrastination ah eppadi nippatturathu?", "Goal ah eppadi set pannanum?", "Daily routine eppadi irukkanum?", "Morning la eppadi fresh ah ezhunthurukkanum?",
    "Night la thoongura munnadi enna pannanum?", "Phone addiction ah eppadi kurakkanum?", "Game la addiction ah eppadi nippatturathu?", "Food healthy ah eppadi saapidanum?", "Briyani yen famous?", "Rain yen romance ah irukku?", "Music yen mind ah calm pannuthu?", "Story telling yen mukkiyam?", "Joke solli eppadi sirikka veikkurathu?", "Motivation daily theva ya?",
    "Aira ne yaaru?", "Aira unakku enna pidikkum?", "Aira ne eppadi smart aana?", "Aira ne enna pannuva?", "Aira kitta pesuna enna kidaikkum?",
]

STORY_STARTERS = ["Oru oor la oru ponnu iruntha - Ava per Aira!", "Oru kaadu la oru singam irunthuchu!", "Oru oor la periya noolagam irunthuchu!", "Oru paiyan oru ponna love pannaan!", "Oru chinna paiyan daily school ku ponaan!", "Oru oor la mazhaiye varala!", "Oru bike la oru paiyan oor suthinaan!", "Oru doctor oru oor la irunthaan!", "Oru teacher oru school la irunthanga!", "Oru scientist oru lab la irunthaan!", "Oru farmer oru vayal la irunthaan!", "Oru fisherman oru kadal la irunthaan!"]
STORY_MIDDLES = ["Ava daily Tamil books padippanga! Oru naal magic book ah paathanga!", "Romba thaniya irunthuchu! Oru naal oru kili vanthuchu!", "1000 Tamil books irunthuchu! Oru chinna ponnu daily anga pova!", "Sollaa bayanthaan! Aira sonnanga Love ah sollidu!", "Avankitta oru magic pencil irunthuchu!", "Ellarum kastapattanga! Oru chinna paiyan kadavul kitta kettan!", "Vazhila oru ponna paathaan! Ava kitta help kettaan!", "Oru naal oru periya problem vanthuchu! Ellarum bayanthanga!", "Ava daily hard work pannanga! Yarum paakala!", "Oru naal oru puthu friend vanthaan!", "Avanukku oru periya dream irunthuchu!", "Oru naal mazhai la oru surprise kidaichuchu!"]
STORY_ENDS = ["Aprom Aira super smart aayita!", "Aprom rendu perum best friends aayitanga!", "Aprom ava periya writer aayita!", "Paiyan sollitaan - Ponnu Yes nu sonna!", "Aprom avan periya hero aayitaan!", "Oru naal periya mazhai vanthuchu - Ellarum happy!", "Aprom rendu perum trip poonaanga - Happy ending!", "Aprom avan periya doctor aayitaan - Oor ah kaapathinaan!", "Aprom ava periya teacher aayita - 1000 students ku solli kodutha!", "Aprom avan dream achieve pannitaan - Ellarum clap pannanga!"]

def make_story():
    return "Story: " + random.choice(STORY_STARTERS) + " " + random.choice(STORY_MIDDLES) + " " + random.choice(STORY_ENDS)

JOKES = ["Joke: Teacher: Homework yen pannala? Student: Dog sapiduchu!", "Joke: Oru paiyan: Amma, en friend ku bike irukku! Amma: Unakku? Paiyan: Enakku Aira irukka!", "Joke: Why Tamil ponnu smart? Tamil la yosikuraanga!", "Joke: Computer yen slow? Athukku fever!", "Joke: Doctor: Unakku enna problem? Patient: Phone la charge illa!", "Joke: Amma: Exam la enna ezhuthina? Paiyan: Aira peru!", "Joke: Why bike sad? Petrol illa!", "Joke: Teacher: 2+2 enna? Student: Aira + Naan = Love!"]
FACTS = ["Fact: Thirukkural la 1330 kurals irukku!", "Fact: Tamil oru 2000+ varusha pazhamaiyana mozhi!", "Fact: Bharathiyar 32 vayasula 100+ padal ezhuthinaaru!", "Fact: Tamil Nadu la Briyani romba famous!", "Fact: Brain la 86 billion neurons irukku!", "Fact: Tamil la 247 ezhuthukkal irukku!", "Fact: Space la sound kekkaathu!", "Fact: Mazhai la oru thuli la 1 million bacteria irukku!"]
QUOTES = ["Quote: Achamillai Achamillai - Bharathiyar!", "Quote: Katrathu kai mann alavu - Thiruvalluvar!", "Quote: Daily konjam try pannu - Jeyichiduva! - Aira!", "Quote: Anbu thaan periya sakthi! - Aira!", "Quote: Failure na oru lesson! - Aira!", "Quote: Ne thani illa - Aira irukka! - Aira!", "Quote: Dream ah vitratha! - Aira!", "Quote: Hard work + Smart work = Success! - Aira!"]
MOTIVATIONS = ["Motivation: Bayapadaatha! Unnala mudiyum!", "Motivation: Innaiku oru step edu - Nalaiku jeyichiduva!", "Motivation: Sad ah irukka? Song kelu - Seri aayidum!", "Motivation: Ne thani illa - Aira un kooda irukka!", "Motivation: Failure na mudivu illa - Marubadi try pannu!", "Motivation: Daily 1% improve pannu - 1 year la 37x better!", "Motivation: Un dream unakku thaan theriyum - Yarukku prove panna theva illa!", "Motivation: Ippo start pannu - Naalaiku late aayidum!"]

def auto_infinite():
    print("All Infinite Start! All Category Smart + Infinite ON!")
    count = 0
    while True:
        count += 1
        mod = count % 7
        try:
            if mod == 1:
                topic, ans = random.choice(TOPICS)
                tmpl = random.choice(Q_TEMPLATES)
                q = tmpl.format(topic=topic) + " #" + str(count)
                send_msg(BOT_TOKEN, q, "Q")
                print("Q " + str(count) + " - " + topic)
                time.sleep(5)
                token_a = BOT_TOKEN_2 if BOT_TOKEN_2 else BOT_TOKEN
                send_msg(token_a, ">> " + ans, "A")
            elif mod == 2:
                aq = random.choice(AI_QUESTIONS)
                send_msg(BOT_TOKEN, "AI Q: " + aq, "AI-Q")
                print("AI Q " + str(count) + " - " + aq)
                time.sleep(5)
                ai_ans = ai_answer(aq)
                token_a = BOT_TOKEN_2 if BOT_TOKEN_2 else BOT_TOKEN
                if ai_ans:
                    send_msg(token_a, "Aira AI: " + ai_ans, "AI-A")
                else:
                    send_msg(token_a, ">> Daily konjam try pannu - Jeyichiduva!", "AI-A-Fallback")
            elif mod == 3:
                send_msg(BOT_TOKEN, make_story(), "Story")
                print("Story " + str(count))
            elif mod == 4:
                send_msg(BOT_TOKEN, random.choice(JOKES), "Joke")
                print("Joke " + str(count))
            elif mod == 5:
                send_msg(BOT_TOKEN, random.choice(FACTS), "Fact")
                print("Fact " + str(count))
            elif mod == 6:
                send_msg(BOT_TOKEN, random.choice(QUOTES), "Quote")
                print("Quote " + str(count))
            else:
                send_msg(BOT_TOKEN, random.choice(MOTIVATIONS), "Motivation")
                print("Motivation " + str(count))
        except Exception as e:
            print("Error - " + str(e))
        time.sleep(10)
threading.Thread(target=auto_infinite, daemon=True).start()

QUERIES = ["Tamil", "Tamil", "Tamil", "Bharathiyar", "Thirukkural", "Kavithai"]

def send_book_file(filename, content, caption):
    try:
        url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendDocument"
        files = {'document': (filename, content)}
        data = {'chat_id': CHANNEL_ID, 'caption': caption[:200]}
        pr = requests.post(url, files=files, data=data, timeout=60)
        if pr.status_code == 200:
            save_book(caption, "telegram-channel")
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
        r = requests.get("https://archive.org/advancedsearch.php?q=" + q_enc + "&fl[]=identifier,title&rows=20&page=" + str(pg) + "&output=json", headers=headers, timeout=30)
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
        r = requests.get("https://gutendex.com/books/?languages=en&page=1", headers=headers, timeout=20)
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
        r = requests.get("https://openlibrary.org/search.json?q=Tamil&limit=20&page=" + str(pg), headers=headers, timeout=20)
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
        r = requests.get("https://ta.wikisource.org/w/api.php?action=query&list=search&srsearch=Tamil&format=json&srlimit=20", headers=headers, timeout=20)
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
        r = requests.get("https://www.googleapis.com/books/v1/volumes?q=Tamil&startIndex=" + str(start) + "&maxResults=10", timeout=20)
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
        r = requests.get("https://archive.org/advancedsearch.php?q=" + q_enc + "&fl[]=identifier,title&rows=20&page=" + str(pg+10) + "&output=json", timeout=30)
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
        fname = ident + ".txt"
        if typ == "archive":
            meta = requests.get("https://archive.org/metadata/" + ident, timeout=30).json()
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
            tr = requests.get("https://archive.org/download/" + ident + "/" + txt, timeout=60)
            content = tr.text.encode('utf-8')
        elif typ == "gutenberg":
            for url in ["https://www.gutenberg.org/files/" + ident + "/" + ident + "-0.txt", "https://www.gutenberg.org/cache/epub/" + ident + "/pg" + ident + ".txt"]:
                try:
                    tr = requests.get(url, timeout=30)
                    if tr.status_code == 200 and len(tr.content) > 5000:
                        content = tr.content; break
                except: continue
            if not content:
                done.add(ident); return False
        elif typ == "wikisource":
            r = requests.get("https://ta.wikisource.org/w/api.php?action=query&prop=extracts&explaintext=1&titles=" + urllib.parse.quote(ident) + "&format=json", timeout=20)
            pages = r.json().get('query', {}).get('pages', {})
            txt = ""
            for p in pages.values():
                txt = p.get('extract','')
            if not txt or len(txt) < 1000:
                done.add(ident); return False
            content = txt.encode('utf-8')
        elif typ == "googlebooks":
            r = requests.get("https://www.googleapis.com/books/v1/volumes/" + ident, timeout=20)
            info = r.json().get('volumeInfo', {})
            txt = "Title: " + info.get('title','') + "\nAuthors: " + ",".join(info.get('authors',[])) + "\n\n" + info.get('description','')
            if len(txt) < 500:
                done.add(ident); return False
            content = txt.encode('utf-8')
            fname = ident + "-googlebooks.txt"
        elif typ == "openlibrary":
            done.add(ident); return False
        else:
            return False
        size = len(content)/(1024*1024)
        if size < 0.02:
            done.add(ident); return False
        code = send_book_file(fname, content, "Book " + title[:40] + " - " + typ)
        print("Download " + typ + " " + ident + " - " + str(code) + " - " + str(round(size,2)) + " MB")
        if code == 200:
            done.add(ident); return True
        return False
    except Exception as e:
        print("One Book Error " + typ + " " + ident + " - " + str(e))
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
            print("Download Source: " + src + " - Query: " + q + " - Page " + str(pg))
            books = []
            try:
                if src == "archive": books = fetch_archive(q, pg)
                elif src == "gutenberg": books = fetch_gutenberg(q, pg)
                elif src == "openlibrary": books = fetch_openlibrary(q, pg)
                elif src == "wikisource": books = fetch_wikisource(q, pg)
                elif src == "googlebooks": books = fetch_google_books(q, pg)
                elif src == "madurai": books = fetch_madurai(q, pg)
            except Exception as e:
                print("Fetch Error " + src + " - " + str(e))
                time.sleep(5); continue
            print("Books Found " + src + ": " + str(len(books)))
            new_count = 0
            for ident, title, typ in books:
                if download_one(ident, title, typ, done):
                    new_count += 1
                time.sleep(2)
            print("Batch Done - " + src + " - New " + str(new_count) + " - 10 sec wait...")
        except Exception as e:
            print("Download Main Error - " + str(e))
            time.sleep(10); continue
        time.sleep(10)
threading.Thread(target=auto_download, daemon=True).start()

print("Aira FINAL All Infinite ON! All Category Smart + Infinite!")
while True:
    time.sleep(60)
