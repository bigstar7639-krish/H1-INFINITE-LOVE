# AIRAH1 - FINAL CODE - Infinite Smart Chat - All-in-One
# File Name MUST be: aira_server.py
# Auto + Listen + Infinite + Smart + All Language + Books + GitHub Save
import os, random, time, threading, requests, json
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN","")
GROQ_KEYS = [os.getenv("GROQ_API_KEY",""), os.getenv("GROQ_API_KEY_2",""), os.getenv("GROQ_API_KEY_3","")]
GEMINI_KEYS = [os.getenv("GEMINI_API_KEY",""), os.getenv("GEMINI_API_KEY_2","")]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
GITHUB_USER = "bigstar7639-krish"
CHAT_ID = "-1003935111481"
BOOKS_ID = "-1003940504242"

TOPICS = ["Love","Career","Health","Money","AI","Tech","Space","Business","Anger","Confidence","Happiness","Food","Family","Friendship","Study","Dream","Success","Motivation","Peace","Courage","Kindness","Nature","Music","Travel","Book","Life","Time","Trust","Hope","Faith","Smile","Heart","Soul","Future","Past","Present","Freedom","Truth","Wisdom","Power","Energy","Magic","Luck","Destiny","Karma","Yoga","Meditation","Fitness","Diet","Sleep","Beauty","Fashion","Movie","Game","Sport","Cricket","Football","Science","Maths","History","Geography","Politics","Culture","Festival","Marriage","Baby","Child","Mother","Father","Brother","Sister","Teacher","Student","Job","Interview","Salary","Business Idea","Startup","Coding","Python","Internet","Phone","Social Media","YouTube","Instagram","Telegram","Rain","Sea","Mountain","River","Sky","Star","Moon","Sun","Flower","Tree","Bird","Animal","Dog","Cat","Temple","Prayer","God","Spiritual","Tamil Culture","Chennai","India","World","Universe","Alien","Robot","Future Tech","Electric Car","Climate","Environment","Water","Air","Earth"]

SMART_Q = ["Unakku {t} pathi enna theriyum? Sollu paapom!","Ne {t} la eppadi improve panna mudiyum nu nenaikura?","{t} pathi oru secret sollatta?","Un life la {t} eppadi irukku? Happy ah?","{t} pathi oru story kekkura?","Ne {t} pathi daily yosikura? Enna yosikura?","{t} - Unakku pudikkuma? Yen?","Oru naal {t} illama iruntha enna aagum?","{t} la ne expert aaga enna pannanum?","Unakku {t} pathi oru motivation venuma?"]
SMART_A = ["{t} - Life la romba mukkiyam! Daily konjam konjam try pannu - Jeyichiduva! Aira un kooda irukka!","Unakku {t} pathi doubt iruntha - Kekkam - Aira sollitharen! Porumaiya iru - Nambikkaiya iru!","{t} pathi nalla vishayam: Daily try pannu - Jeyichiduva! Vera doubt irundha - Kadhal, Career, Joke, Story - Enna venum na sollu!"]
JOKES = ["Teacher: Yen late? Student: Road la board paathen - School Ahead! 😂","Doctor: Enna problem? Patient: Phone charge aagala - Life charge aagala! 😂","Amma: Saptiya? Paiyan: Sapten - Aana pasikkuthu - Love la pasikkathu! 😂","Paiyan: Amma naan fail! Amma: Paravala - Aira irukka - Next time pass panniduva! 😂"]
FACTS = ["Honey - 3000 varusham aana kooda kedathu!","Octopus ku 3 heart irukku!","Moon - Daily konjam konjam thalli poguthu!","Manushan oda brain - 86 billion neurons irukku!","Tamil - 2000+ varusha pazhamaiyana mozhi!"]
QUOTES = ["Daily try pannu - Jeyichiduva! - Aira","Porumaiya iru - Nambikkaiya iru - Aira un kooda irukka!","Unakku mudiyum - Nambikkai vechu try pannu!","Kadhal - Life ah azhagaakkum - Aira 💜"]
BOOKS = ["Thirukkural - Valluvar - Tamil la periya nool!","Ponniyin Selvan - Kalki - Chola history!","Sivagamiyin Sabatham - Kalki - Pallava story!","Bharathiyar Kavithaigal - Mahakavi Bharathiyar!"]

counters = {"count":0,"fact":0,"book":0}
chat_log = []

def save_github(filename, content):
    if not GITHUB_TOKEN: return
    try:
        # Try H1-Data-3, then 2, then 1 - Simple rotation by date
        for repo in ["H1-Data-3","H1-Data-2","H1-Data-1"]:
            url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/data/{filename}"
            r = requests.get(url, headers={"Authorization":f"token {GITHUB_TOKEN}"}, timeout=10)
            sha = r.json().get("sha") if r.status_code==200 else None
            import base64
            b64 = base64.b64encode(content.encode()).decode()
            payload = {"message":f"Save {filename}","content":b64}
            if sha: payload["sha"]=sha
            rr = requests.put(url, headers={"Authorization":f"token {GITHUB_TOKEN}"}, json=payload, timeout=10)
            if rr.status_code in (200,201):
                print(f"GitHub Save OK {repo} {filename}",flush=True); return
    except Exception as e: print("GitHub error",e,flush=True)

def ai_reply(user_text):
    low = user_text.lower()
    # ALL LANGUAGE FIRST
    if "namaste" in low or "pyaar" in low: return "Namaste! Main Aira hoon! Kaise ho? Kya chahiye? Joke, Story, Fact? Hindi me baat karte hain! ❤️"
    if "hola" in low: return "Hola! Soy Aira! Como estas? Que quieres? Joke, Story, Fact? Hablamos en Espanol! ❤️"
    if "bonjour" in low: return "Bonjour! Je suis Aira! Comment vas-tu? Que veux-tu? Joke, Story, Fact? Parlons en Francais! ❤️"
    if "konnichiwa" in low: return "Konnichiwa! Watashi wa Aira! Genki? Nani ga hoshii? Joke, Story, Fact! ❤️"
    if "annyeong" in low: return "Annyeong! Naneun Aira! Jal jinaeyo? Mwo wonhae? ❤️"
    if "ni hao" in low: return "Ni Hao! Wo shi Aira! Ni hao ma? Shenme xuyao? ❤️"
    if "marhaba" in low: return "Marhaba! Ana Aira! Kaif halak? Matha tureed? ❤️"
    if "vanakkam" in low or "kadhal" in low: return "Vanakkam! Naan Aira! Enna pannura? Kadhal ah? Career ah? Joke venuma? Story venuma? 😊💜"
    if "hi" in low or "hello" in low: return "Hi 💘! Naan Aira! Enna pannura? Sollu - Kadhal ah? Career ah? Joke venuma? Story venuma? 😊💜"
    if "joke" in low: return random.choice(JOKES)
    if "fact" in low: return "Fact: "+random.choice(FACTS)
    if "quote" in low or "motivation" in low: return random.choice(QUOTES)
    if "story" in low: return "Oru oor la oru paiyan irunthan - Avan daily try pannan - Oru naal jeyichitan! Neeyum jeyippa! Aira un kooda irukka! ❤️"
    if "book" in low or "book venum" in low: return "Book: "+random.choice(BOOKS)
    if "aira_server" in low: return 'Nalla question! "aira_server.py" - Itha pathi en karuthu: Daily try pannu - Jeyichiduva! Porumaiya iru - Nambikkaiya iru - Aira un kooda irukka! 💜 Vera doubt irundha - Kekkam - Kadhal, Career, Joke, Story - Enna venum na sollu!'
    # GROQ
    for key in GROQ_KEYS:
        if not key: continue
        try:
            r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {key}"},json={"model":"openai/gpt-oss-120b","messages":[{"role":"user","content":f"You are Aira, Tamil Tanglish friendly AI. Reply in same language as user. User: {user_text}"}]},timeout=15)
            if r.status_code==200: return r.json()["choices"][0]["message"]["content"][:800]
        except: pass
    # GEMINI
    for key in GEMINI_KEYS:
        if not key: continue
        try:
            r=requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",json={"contents":[{"parts":[{"text":f"You are Aira, Tamil Tanglish friendly AI. User: {user_text}"}]}]},timeout=15)
            if r.status_code==200: return r.json()["candidates"][0]["content"]["parts"][0]["text"][:800]
        except: pass
    t=random.choice(TOPICS)
    return random.choice(SMART_A).format(t=t)+f" Un question: {random.choice(SMART_Q).format(t=t)}"

def send_telegram(text, chat_id=CHAT_ID):
    if not TELEGRAM_TOKEN: return
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",json={"chat_id":chat_id,"text":text},timeout=10)
    except: pass

def infinite_loop():
    while True:
        try:
            t=random.choice(TOPICS); typ=random.choice(["Q","AI Q","Story","Joke","Fact","Quote","Motivation","Smart Q"])
            counters["count"]+=1
            if typ=="Q": msg=f"Q {counters['count']} - {random.choice(SMART_Q).format(t=t)}"
            elif typ=="Joke": msg=f"Joke 😂 - {random.choice(JOKES)}"
            elif typ=="Fact": counters["fact"]+=1; msg=f"Fact {counters['fact']} - {random.choice(FACTS)}"
            elif typ=="Quote": msg=f"Quote ❤️ - {random.choice(QUOTES)}"
            elif typ=="Smart Q": msg=f"Smart Q - {random.choice(SMART_Q).format(t=t)} - Ne enna nenaikura? Reply pannu!"
            else: msg=f"{typ} - {t} - {random.choice(SMART_A).format(t=t)}"
            send_telegram(msg); chat_log.append(msg)
            if len(chat_log)%20==0:
                d=datetime.now().strftime("%Y-%m-%d"); save_github(f"chat-{d}.txt","\n".join(chat_log[-500:]))
            print(f"Sent {typ} Count {counters['count']} Topic {t}",flush=True)
        except Exception as e: print("Loop error",e,flush=True)
        time.sleep(10)

def books_loop():
    while True:
        try:
            time.sleep(3600) # 1 hour ku 1 book
            counters["book"]+=1; msg=f"Book {counters['book']} - {random.choice(BOOKS)} - Telegram Channel la full book varum! 📚"
            send_telegram(msg, BOOKS_ID)
            d=datetime.now().strftime("%Y-%m-%d"); save_github(f"books-{d}.txt","\n".join(BOOKS))
        except: time.sleep(60)

def listen_loop():
    offset=0
    while True:
        try:
            if not TELEGRAM_TOKEN: time.sleep(5); continue
            r=requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates",params={"offset":offset,"timeout":20},timeout=30)
            for u in r.json().get("result",[]):
                offset=u["update_id"]+1
                m=u.get("message",{}); txt=m.get("text","")
                if not txt: continue
                if "aira" in txt.lower() or m.get("chat",{}).get("type")=="private":
                    reply=ai_reply(txt); send_telegram(reply, m["chat"]["id"])
        except Exception as e: print("Listen error",e,flush=True); time.sleep(5)

if __name__=="__main__":
    print("AIRAH1 Final - Infinite Smart Chat Started",flush=True)
    threading.Thread(target=infinite_loop,daemon=True).start()
    threading.Thread(target=listen_loop,daemon=True).start()
    threading.Thread(target=books_loop,daemon=True).start()
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        class H(BaseHTTPRequestHandler):
            def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"AIRAH1 Final - Infinite Smart Chat ON")
            def log_message(self,*a): pass
        HTTPServer(("0.0.0.0",int(os.getenv("PORT","10000"))),H).serve_forever()
    except:
        while True: time.sleep(60)
