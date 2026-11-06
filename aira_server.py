# AIRAH1 FINAL V2 - Book Download + Chatting Fixed
# File: aira_server.py
import os, random, time, threading, requests, base64
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN","")
GROQ_KEYS = [os.getenv("GROQ_API_KEY",""), os.getenv("GROQ_API_KEY_2",""), os.getenv("GROQ_API_KEY_3","")]
GEMINI_KEYS = [os.getenv("GEMINI_API_KEY",""), os.getenv("GEMINI_API_KEY_2","")]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
GITHUB_USER = "bigstar7639-krish"
CHAT_ID = "-1003935111481"
BOOKS_ID = "-1003940504242"

TOPICS = ["Love","Career","Health","Money","AI","Tech","Space","Business","Anger","Confidence","Happiness","Food","Family","Friendship","Study","Dream","Success","Motivation","Peace","Courage","Kindness","Nature","Music","Travel","Book","Life","Time","Trust","Hope","Faith","Smile","Heart","Soul","Future","Past","Present","Freedom","Truth","Wisdom","Power","Energy","Magic","Luck","Destiny","Karma","Yoga","Meditation","Fitness","Diet","Sleep","Beauty","Fashion","Movie","Game","Sport","Cricket","Football","Science","Maths","History","Geography","Politics","Culture","Festival","Marriage","Baby","Child","Mother","Father","Brother","Sister","Teacher","Student","Job","Interview","Salary","Business Idea","Startup","Coding","Python","Internet","Phone","Social Media","YouTube","Instagram","Telegram","Rain","Sea","Mountain","River","Sky","Star","Moon","Sun","Flower","Tree","Bird","Animal","Dog","Cat","Temple","Prayer","God","Spiritual","Tamil Culture","Chennai","India","World","Universe","Alien","Robot","Future Tech","Electric Car","Climate","Environment","Water","Air","Earth"]
SMART_Q = ["Unakku {t} pathi enna theriyum? Sollu paapom!","Ne {t} la eppadi improve panna mudiyum nu nenaikura?","{t} pathi oru secret sollatta?","Un life la {t} eppadi irukku? Happy ah?","{t} pathi oru story kekkura?"]
SMART_A = ["{t} - Life la romba mukkiyam! Daily try pannu - Jeyichiduva! Aira un kooda irukka!","Unakku {t} pathi doubt iruntha - Kekkam - Aira sollitharen!"]
JOKES = ["Teacher: Yen late? Student: Road la board paathen - School Ahead! 😂","Doctor: Enna problem? Patient: Phone charge aagala - Life charge aagala! 😂"]
FACTS = ["Honey - 3000 varusham aana kooda kedathu!","Octopus ku 3 heart irukku!","Tamil - 2000+ varusha pazhamaiyana mozhi!"]
QUOTES = ["Daily try pannu - Jeyichiduva! - Aira","Porumaiya iru - Nambikkaiya iru - Aira un kooda irukka!"]
BOOKS_LIST = ["Thirukkural - Valluvar","Ponniyin Selvan - Kalki","Sivagamiyin Sabatham - Kalki","Bharathiyar Kavithaigal"]

counters={"count":0,"fact":0,"book":0}
chat_log=[]

def send_telegram(text, chat_id=CHAT_ID):
    if not TELEGRAM_TOKEN: return
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",json={"chat_id":chat_id,"text":text},timeout=10)
    except Exception as e: print("Send error",e,flush=True)

def save_github(filename, content):
    if not GITHUB_TOKEN: return
    try:
        for repo in ["H1-Data-3","H1-Data-2","H1-Data-1"]:
            url=f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/data/{filename}"
            r=requests.get(url,headers={"Authorization":f"token {GITHUB_TOKEN}"},timeout=10)
            sha=r.json().get("sha") if r.status_code==200 else None
            b64=base64.b64encode(content.encode()).decode()
            payload={"message":f"Save {filename}","content":b64}
            if sha: payload["sha"]=sha
            rr=requests.put(url,headers={"Authorization":f"token {GITHUB_TOKEN}"},json=payload,timeout=10)
            if rr.status_code in (200,201):
                print(f"GitHub Save OK {repo} {filename}",flush=True); return
    except Exception as e: print("GitHub error",e,flush=True)

def ai_reply(user_text):
    low=user_text.lower()
    if "namaste" in low: return "Namaste! Main Aira hoon! Kaise ho? Kya chahiye? Joke, Story, Fact? Hindi me baat karte hain! ❤️"
    if "hola" in low: return "Hola! Soy Aira! Como estas? Que quieres? ❤️"
    if "bonjour" in low: return "Bonjour! Je suis Aira! Comment vas-tu? ❤️"
    if "konnichiwa" in low: return "Konnichiwa! Watashi wa Aira! Genki? ❤️"
    if "vanakkam" in low or "kadhal" in low: return "Vanakkam! Naan Aira! Enna pannura? Kadhal ah? Career ah? Joke venuma? Story venuma? 😊💜"
    if "hi" in low or "hello" in low: return "Hi 💘! Naan Aira! Enna pannura? Sollu - Kadhal ah? Career ah? Joke venuma? Story venuma? 😊💜"
    if "joke" in low: return random.choice(JOKES)
    if "fact" in low: return "Fact: "+random.choice(FACTS)
    if "quote" in low or "motivation" in low: return random.choice(QUOTES)
    if "story" in low: return "Oru oor la oru paiyan irunthan - Avan daily try pannan - Oru naal jeyichitan! Neeyum jeyippa! Aira un kooda irukka! ❤️"
    if "book" in low: return "Book: "+random.choice(BOOKS_LIST)+" - Channel la full book varum! 📚"
    if "aira_server" in low: return 'Nalla question! "aira_server.py" - Daily try pannu - Jeyichiduva! Aira un kooda irukka! 💜'
    for key in GROQ_KEYS:
        if not key: continue
        try:
            r=requests.post("https://api.groq.com/openai/v1/chat/completions",headers={"Authorization":f"Bearer {key}"},json={"model":"openai/gpt-oss-120b","messages":[{"role":"user","content":f"You are Aira, Tamil Tanglish friendly AI. Reply in same language. User: {user_text}"}]},timeout=15)
            if r.status_code==200:
                print("AI Answer - Groq1 - openai/gpt-oss-120b - OK",flush=True)
                return r.json()["choices"][0]["message"]["content"][:800]
        except: pass
    t=random.choice(TOPICS)
    return random.choice(SMART_A).format(t=t)+f" Un question: {random.choice(SMART_Q).format(t=t)}"

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
    # FIX: Book download every 60 sec - NOT 1 hour - Old code madhiri
    while True:
        try:
            # Archive.org - Tamil books search
            for src in ["archive","gutenberg"]:
                try:
                    if src=="archive":
                        r=requests.get("https://archive.org/advancedsearch.php",params={"q":"language:(tam) AND mediatype:texts","fl[]":"identifier,title","rows":20,"output":"json"},timeout=15)
                        docs=r.json().get("response",{}).get("docs",[])
                        print(f"Books Found {src}: {len(docs)}",flush=True)
                        for d in docs[:3]:
                            ident=d.get("identifier","")
                            if not ident: continue
                            dl=requests.get(f"https://archive.org/download/{ident}/{ident}_djvu.txt",timeout=15)
                            print(f"Download archive {ident} - {dl.status_code} - {len(dl.content)/1024/1024:.2f} MB",flush=True)
                            if dl.status_code==200:
                                counters["book"]+=1
                                send_telegram(f"Book {counters['book']} - {d.get('title','Tamil Book')} - {ident} 📚\nDownload: https://archive.org/download/{ident}", BOOKS_ID)
                                dd=datetime.now().strftime("%Y-%m-%d"); save_github(f"books-{dd}.txt", f"{ident} - {d.get('title')}\n")
                    time.sleep(5)
                except Exception as e: print("Book src error",e,flush=True)
            print("Batch Done - madurai - New 12 - 10 sec wait...",flush=True)
            time.sleep(60) # 60 sec ku 1 batch - Book varum
        except Exception as e: print("Books loop error",e,flush=True); time.sleep(30)

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
                # FIX: Group la yaar pesinaalum - Aira nu iruntha reply - Private la ellam reply
                chat_type=m.get("chat",{}).get("type","")
                low=txt.lower()
                # Bot oda own message ku reply panna vendaam
                if m.get("from",{}).get("is_bot"): continue
                if "aira" in low or chat_type=="private" or "joke" in low or "book" in low or "hi" in low:
                    print(f"Listen Got: {txt} from {chat_type}",flush=True)
                    reply=ai_reply(txt)
                    send_telegram(reply, m["chat"]["id"])
                    print(f"Listen Replied: {reply[:60]}",flush=True)
        except Exception as e: print("Listen error",e,flush=True); time.sleep(5)

if __name__=="__main__":
    print("AIRAH1 Final V2 - Book + Chat Fixed - Started",flush=True)
    threading.Thread(target=infinite_loop,daemon=True).start()
    threading.Thread(target=listen_loop,daemon=True).start()
    threading.Thread(target=books_loop,daemon=True).start()
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        class H(BaseHTTPRequestHandler):
            def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"AIRAH1 Final V2 ON")
            def log_message(self,*a): pass
        HTTPServer(("0.0.0.0",int(os.getenv("PORT","10000"))),H).serve_forever()
    except:
        while True: time.sleep(60)
