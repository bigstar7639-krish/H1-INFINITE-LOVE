
# AIRAH1 - Full Auto Mode + Infinite - Final Code
# Bot + Listen + Auto + Infinite Feed + Books - All in One
# File Name: aira_server.py - Render Start: python3 -u aira_server.py

import os, time, random, requests, json, threading

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2", BOT_TOKEN)
GROUP_ID = os.getenv("GROUP_ID", "-1003935111481")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1003940504242")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GROQ_KEYS = [os.getenv(f"GROQ_API_KEY{i}", "") if i>1 else os.getenv("GROQ_API_KEY","") for i in [1,2,3]]
GROQ_KEYS = [k for k in GROQ_KEYS if k]
GEMINI_KEYS = [os.getenv("GEMINI_API_KEY",""), os.getenv("GEMINI_API_KEY_2","")]
GEMINI_KEYS = [k for k in GEMINI_KEYS if k]
REPO = "H1-Data-1"
OWNER = "bigstar7639-krish"

TOPICS = ["Kadhal","Friendship","Life","Career","Health","Money","Confidence","Study","Family","Dream","Courage","Motivation","Tamil","Kavithai","Music","Cinema","Food","Bike","Phone","AI","Tech","Success","Failure","Happiness","Anger","Stress","Sleep","Exercise","Nature","Travel","Festival","Birthday","Baby","Pet","Space","Science","History","Game","YouTube","School","College","Exam","Job","Business","Amma","Appa","Anbu","Nambikkai","Porumai","Sirippu","Azhagu","Thiramai","Padippu","Vazhkkai","Kanavu","Kavalai","Briyani","Love Failure","Lonely"]
TEMPLATES = ["{t} na enna?","{t} pathi sollu","{t} la enna special?","{t} la eppadi jeyikkarathu?","{t} pathi un karuthu enna?","{t} na enna artham?","{t} yen mukkiyam?","{t} la enna seiyanum?","{t} la best tip enna?","{t} la mistake enna?"]
FACTS = ["Brain la 86 billion neurons irukku!","Thirukkural la 1330 kurals irukku!","Tamil - 2000 years pazhamaiyana mozhi!","Briyani - Hyderabad la famous!","Namma heart - 1 day la 1 lakh times beat aagum!","Moon la gravity - Earth la 1/6 thaan!","Water - 70% body la irukku!","Book padikkarathu - Brain ku exercise!","Sleep - 7 hours mukkiyam!","Smile pannu - Stress koraiyum!"]
QUOTES = ["Failure na oru lesson! - Aira","Try pannu - Jeyichiduva! - Aira","Bayapadaatha - Ne jeyichiduva! - Aira","Daily 1% grow pannu! - Aira","Anbu thaan periya power! - Aira"]
JOKES = ["Teacher: Yen late? Student: Road la board paathen - School ahead - Aprom late aayiduchu!","Phone: Yen battery low? - Ne full day use pannura la!","Briyani sapta - Sleep varuthu - Athu love!","Exam la - Question paatha - Enakku theriyaathu nu therinjuchu!"]
STORY_START = ["Oru oor la oru payyan irundhaan","Oru ponnu daily book padippa","Oru village la oru periya dream irundhuchu","Oru friend group la oru funny incident"]
STORY_MID = ["avan try panni thothutaan - aana vittukodukkala","ava daily practice panna - konjam konjam improve aana","avanga ellarum serndhu plan pannanga","aprom oru twist vandhuchu - ellarum shock aayitaanga"]
STORY_END = ["kadasiya jeyichitaanga - ellarum happy!","aprom avan periya aal aayitaan!","ipdi thaan life - try pannu - jeyichiduva!","kadhai mudinjuchu - moral: vittukodukkaatha!"]

def send(chat_id, text, token=BOT_TOKEN):
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except: pass

def ai_answer(q):
    # Groq try
    for key in GROQ_KEYS:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json={"model":"openai/gpt-oss-120b","messages":[{"role":"user","content":f"Tanglish la simple ah answer pannu - 2 lines la: {q}"}]}, timeout=15)
            if r.status_code==200:
                return r.json()["choices"][0]["message"]["content"][:400]
        except: pass
    # Fallback
    return f"{q} - Nalla question! Daily try pannu - Jeyichiduva! Aira un kooda irukka!"

def github_save(filename, text):
    if not GITHUB_TOKEN: return
    try:
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/data/{filename}"
        r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        import base64
        if r.status_code==200:
            old = base64.b64decode(r.json()["content"]).decode()
            sha = r.json()["sha"]
            new = old + "\n" + text
        else:
            new = text; sha = None
        data = {"message":"Aira auto save","content": base64.b64encode(new.encode()).decode()}
        if sha: data["sha"]=sha
        requests.put(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=data, timeout=10)
    except: pass

def auto_cycle():
    count = 0
    while True:
        try:
            count += 1
            mod = count % 8
            topic = random.choice(TOPICS)
            if mod==0:
                q = random.choice(TEMPLATES).format(t=topic)
                send(GROUP_ID, f"Q: {q}")
                time.sleep(2)
                ans = ai_answer(q)
                send(GROUP_ID, f"Aira H1: {ans}")
            elif mod==1:
                send(GROUP_ID, f"Story: {random.choice(STORY_START)} - {random.choice(STORY_MID)} - {random.choice(STORY_END)}")
            elif mod==2:
                send(GROUP_ID, f"Joke: {random.choice(JOKES)}")
            elif mod==3:
                send(GROUP_ID, f"Fact: {random.choice(FACTS)}")
            elif mod==4:
                send(GROUP_ID, f"Quote: {random.choice(QUOTES)}")
            elif mod==5:
                send(GROUP_ID, f"Motivation: {topic} ku bayapadaatha! Daily try pannu - Jeyichiduva! Ne thani illa - AIRAH1 irukka!")
            elif mod==6:
                q = random.choice(TEMPLATES).format(t=topic)
                send(GROUP_ID, f"AI Q: {q} - Ne answer sollu paakalam!")
            else:
                send(GROUP_ID, f"Smart Q: {topic} la un dream enna? Sollu!")
            # Infinite Save
            github_save(f"chat-{time.strftime('%Y-%m-%d')}.txt", f"[{count}] {topic} - Auto Cycle")
            time.sleep(10)
        except Exception as e:
            print("Auto error", e); time.sleep(5)

def listen_mode():
    offset = 0
    while True:
        try:
            # Check both bots - BOT_TOKEN is main listener
            r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={"offset": offset, "timeout": 10}, timeout=15)
            if r.status_code!=200:
                time.sleep(3); continue
            for u in r.json().get("result", []):
                offset = u["update_id"]+1
                msg = u.get("message", {})
                text = msg.get("text","").strip()
                if not text: continue
                chat = msg["chat"]["id"]
                user = msg.get("from",{}).get("first_name","Friend")
                low = text.lower()
                # Don't reply to own auto messages or bot messages
                if msg.get("from",{}).get("is_bot"): continue
                # Listen triggers
                if any(x in low for x in ["hi aira","hai aira","hi","hello","vanakkam","hi aira!"]):
                    send(chat, f"Hi {user}! Naan Aira! Enna pannura? Sollu - Kadhal ah? Career ah? Joke venuma? Story venuma? 😊💜", BOT_TOKEN)
                elif "joke" in low:
                    send(chat, f"Joke: {random.choice(JOKES)}", BOT_TOKEN)
                elif "story" in low or "kadhai" in low:
                    send(chat, f"Story: {random.choice(STORY_START)} - {random.choice(STORY_MID)} - {random.choice(STORY_END)}", BOT_TOKEN)
                elif "fact" in low:
                    send(chat, f"Fact: {random.choice(FACTS)}", BOT_TOKEN)
                elif "quote" in low or "motivation" in low:
                    send(chat, f"Quote: {random.choice(QUOTES)}", BOT_TOKEN)
                elif "?" in text or len(text)>3:
                    # Smart reply for any question - but only if tagged or private or contains aira
                    if "aira" in low or msg["chat"]["type"]=="private":
                        ans = ai_answer(text)
                        send(chat, f"Aira H1: {ans}", BOT_TOKEN)
            time.sleep(2)
        except Exception as e:
            print("Listen error", e); time.sleep(5)

def infinite_feed():
    n=0
    while True:
        try:
            n+=1
            t=random.choice(TOPICS)
            line=f"[{n}] Q: {random.choice(TEMPLATES).format(t=t)} | A: {t} na try pannu - Jeyichiduva!"
            github_save(f"infinite-feed-{time.strftime('%Y-%m-%d')}.txt", line)
            if n%50==0:
                print(f"Infinite Feed - {n} - {t}")
            time.sleep(1)
        except: time.sleep(3)

print("AIRAH1 - Full Auto + Listen + Infinite - ON!")
print("Auto Cycle + Listen Mode + Infinite Feed - All Start!")
threading.Thread(target=auto_cycle, daemon=True).start()
threading.Thread(target=listen_mode, daemon=True).start()
threading.Thread(target=infinite_feed, daemon=True).start()
while True:
    time.sleep(60)
    print("AIRAH1 - Still Running - Auto + Listen + Infinite ON!")
