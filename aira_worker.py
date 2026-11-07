# AIRAH1 - FINAL V4 - Worker - Port First + Single Guard - 100/100 + No Watermark + Japan + China + India + Infinite Source + Infinite Repo + do_HEAD
# File: aira_worker.py - Start: python3 -u aira_worker.py
# NO Pollinations! NO Google / Instagram / Facebook scraping! Only FREE legal sources - No Watermark!
import os, time, threading, requests, base64, random, html, re
from datetime import datetime

BOT1_TOKEN = os.getenv("BOT1_TOKEN","")
BOT2_TOKEN = os.getenv("BOT2_TOKEN","")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN","")
GITHUB_USER = "bigstar7639-krish"

def fix_id(v, default):
    v = (v or default).strip()
    if not v: return default
    if v.startswith("-"): return v
    if v.startswith("100"): return "-" + v
    return "-100" + v

DATA_CHANNEL = fix_id(os.getenv("DATA_CHANNEL",""), "-1004366479419")
print(f"Worker Start - Bot1 OK? {bool(BOT1_TOKEN)} Bot2 OK? {bool(BOT2_TOKEN)} Channel: {DATA_CHANNEL}", flush=True)

CURRENT_REPO = ["H1-Data-3"]; REPO_COUNT = [0]; MAX_PER_REPO = 1000
SAVE_LOCK = threading.Lock()
def get_repo_num(r):
    try: return int(r.split("-")[-1])
    except: return 3
def ensure_repo(repo):
    try:
        r = requests.get(f"https://api.github.com/repos/{GITHUB_USER}/{repo}", headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "AIRAH1"}, timeout=10)
        if r.status_code == 200: return True
        cr = requests.post("https://api.github.com/user/repos", headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "AIRAH1"}, json={"name": repo, "private": False, "auto_init": True, "description": "AIRAH1 Infinite"}, timeout=15)
        print(f"Infinite Repo Create: {cr.status_code} - {repo}", flush=True)
        return cr.status_code in (200,201,422)
    except Exception as e: print(f"Repo Error {e}", flush=True); return False
def next_repo():
    n = get_repo_num(CURRENT_REPO[0])+1; CURRENT_REPO[0]=f"H1-Data-{n}"; REPO_COUNT[0]=0
    print(f"Infinite Repo Switch -> {CURRENT_REPO[0]}", flush=True); ensure_repo(CURRENT_REPO[0]); return CURRENT_REPO[0]
def save_github(filename, content):
    if REPO_COUNT[0] >= MAX_PER_REPO: next_repo()
    if not GITHUB_TOKEN: return False
    with SAVE_LOCK:
        for attempt in range(3):
            repo = CURRENT_REPO[0]; ensure_repo(repo)
            try:
                url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/contents/data/{filename}"
                r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
                sha = r.json().get("sha") if r.status_code==200 else None
                old = ""
                if r.status_code==200:
                    try: old = base64.b64decode(r.json().get("content","")).decode(errors="ignore")
                    except: old = ""
                new = (old + "\n" + content) if old else content
                lines = new.split("\n")
                if len(lines) > 2000: new = "\n".join(lines[-2000:])
                b64 = base64.b64encode(new.encode()).decode()
                payload = {"message": f"Worker Save {filename}", "content": b64}
                if sha: payload["sha"] = sha
                rr = requests.put(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload, timeout=15)
                if rr.status_code in (200,201):
                    REPO_COUNT[0]+=1
                    print(f"Worker GitHub Save OK - {repo}/{filename} - Repo {REPO_COUNT[0]}/{MAX_PER_REPO}", flush=True)
                    return True
                if rr.status_code in (409,422):
                    print(f"Worker Save Retry {rr.status_code} - Try {attempt+1}/3", flush=True); time.sleep(1); continue
                if rr.status_code in (403,413): next_repo(); continue
                time.sleep(1); continue
            except Exception as e: print(f"Worker Save Error {e}", flush=True); time.sleep(1); continue
        return False

# --- 100+ CATEGORIES - Tamil + Japan + China + India + Global ---
START_N = 1
BASE_CATS = ["Tamil","Love","God","Nature","Cat","Dog","Food","Cricket","Space","Story","Health","Music","Movie","Temple","Flower","Sea","Mountain","River","Sky","Star","Moon","Sun","Bird","Animal","Baby","Teacher","Student","Business","Money","Yoga","Meditation","Fitness","Diet","Sleep","Beauty","Fashion","Game","Sport","Football","Science","History","Culture","Festival","Marriage","Family","Friendship","Study","Dream","Success","Motivation","Peace","Courage","Kindness","Truth","Wisdom","Power","Magic","Luck","Destiny","Karma","Rain","Village","City","Chennai","Madurai","Delhi","Mumbai","London","Paris","Tokyo","New York","Egypt","Pyramids","Taj Mahal","Eiffel Tower","Psychology","Philosophy","Economics","Politics","Law","Education","Happiness","Smile","Heart","Future","Freedom","Hope","Faith",
# Japan
"Japan","Tokyo","Sakura","Kimono","Anime","Japanese Food","Sushi","Kyoto","Osaka","Japanese Temple","Japanese Girl","Samurai","Ninja",
# China
"China","Beijing","Great Wall","Panda","Chinese Food","Chinese Temple","Shanghai","Chinese Culture","Dragon","Chinese Girl",
# India
"India","Tamil Nadu","Kerala","Saree","Biryani","Diwali","Pongal","Indian Temple","Indian Food","Indian Girl","Kolkata","Bangalore","Hyderabad",
# Extra
"Beach","Forest","Desert","Snow","Fire","Earth","Water","Coffee","Tea","Cake","Pizza","Burger","Chocolate","Fruit","Vegetable","Summer","Winter","Monsoon","Morning","Night","Home","Garden","Park","Elephant","Tiger","Lion","Horse","Bike","Car","Train","Flight","Phone","Computer","Book","Kavithai","Thirukkural","Pazhamozhi","Joke","Reading","Writing","Poetry","Singing","Dancing"]

# Category -> Search term mapping for Japan / China / India sources
# Openverse + Wikimedia + Unsplash ellam itha use pannum - No Watermark!
SEARCH_MAP = {
    "Japan": "Japan Tokyo", "Tokyo": "Tokyo Japan", "Sakura": "Sakura cherry blossom Japan", "Kimono": "Kimono Japanese woman", "Anime": "Anime illustration", "Japanese Food": "Japanese food sushi", "Sushi": "Sushi Japanese food", "Kyoto": "Kyoto Japan temple", "Osaka": "Osaka Japan", "Japanese Temple": "Japanese temple", "Japanese Girl": "Japanese girl portrait", "Samurai": "Samurai Japan", "Ninja": "Ninja Japan",
    "China": "China Beijing", "Beijing": "Beijing China", "Great Wall": "Great Wall of China", "Panda": "Giant panda", "Chinese Food": "Chinese food", "Chinese Temple": "Chinese temple", "Shanghai": "Shanghai China", "Chinese Culture": "Chinese culture", "Dragon": "Chinese dragon", "Chinese Girl": "Chinese girl portrait",
    "India": "India", "Tamil Nadu": "Tamil Nadu temple", "Kerala": "Kerala India", "Saree": "Saree Indian woman", "Biryani": "Biryani Indian food", "Diwali": "Diwali festival India", "Pongal": "Pongal festival Tamil", "Indian Temple": "Indian temple", "Indian Food": "Indian food", "Indian Girl": "Indian girl portrait", "Chennai": "Chennai Tamil Nadu", "Madurai": "Madurai temple",
    "Science": "science laboratory microscope", "Space": "space stars galaxy rocket", "Nature": "beautiful nature forest mountain", "Health": "yoga healthy fitness meditation", "Food": "delicious food", "Cricket": "cricket stadium match", "Temple": "hindu temple", "God": "hindu god temple divine",
}


# --- NEW IMAGE PROMPT - INFINITE PROMPT - ALL CATEGORY - 1 Category ku 5 Prompt - Rotate Aagum! ---
# Bot1 - Oru category la 100 image - 1,2,3,4,5,1,2,3,4,5 nu infinite rotate aagum - Same photo varaathu!
IMAGE_PROMPTS = {
    "Tamil": ["Tamil Nadu temple beautiful", "Tamil girl saree smiling cute Aira style", "Chennai Marina beach sunset", "Madurai Meenakshi temple", "Tamil village kolam festival"],
    "Love": ["love couple heart romantic cute", "couple holding hands sunset", "heart shape love red", "romantic couple rain", "cute couple smiling"],
    "God": ["Hindu god temple divine beautiful", "Lord Shiva temple", "Lord Murugan temple", "Goddess Amman temple", "Divine light temple"],
    "Nature": ["beautiful nature green forest", "mountain river sunset nature", "green forest waterfall", "flower garden beautiful", "nature sunrise peaceful"],
    "Cat": ["cute cat kitten playing", "white cat cute eyes", "cat sleeping cute", "kitten playing ball", "cat with flower"],
    "Dog": ["cute dog puppy playing", "golden retriever puppy", "dog smiling happy", "puppy in garden", "dog with ball"],
    "Food": ["delicious Indian food biryani", "Tamil food dosa idli", "cake chocolate delicious", "fruit fresh colourful", "street food India"],
    "Cricket": ["cricket stadium match", "cricket batsman batting", "cricket ball bowling", "cricket crowd stadium", "cricket trophy winning"],
    "Space": ["space stars galaxy rocket", "astronaut space moon", "planet galaxy beautiful", "rocket launch space", "earth from space"],
    "Story": ["story book magic fantasy", "fairy tale castle", "magic book reading", "story village old", "fantasy forest magic"],
    "Health": ["yoga meditation peaceful", "healthy food fruits", "fitness gym workout", "morning walk park", "meditation calm"],
    "Music": ["music concert guitar", "singer singing stage", "piano music beautiful", "Tamil music concert", "guitar playing"],
    "Movie": ["cinema movie theatre", "movie poster action", "film shooting", "cinema popcorn", "actor movie"],
    "Temple": ["Hindu temple beautiful architecture", "South Indian temple gopuram", "temple sunset", "temple festival", "temple pond"],
    "Flower": ["beautiful flower rose", "lotus flower pink", "jasmine flower white", "sunflower yellow", "flower garden colourful"],
    "Sea": ["sea beach waves blue", "beach sunset beautiful", "ocean wave", "beach palm tree", "sea boat"],
    "Mountain": ["mountain snow beautiful", "mountain trekking", "Himalaya mountain", "mountain sunrise", "mountain forest"],
    "River": ["river beautiful flowing", "river sunset", "river bridge", "river boat", "river forest"],
    "Sky": ["sky clouds blue beautiful", "sunset sky orange", "night sky stars", "rainbow sky", "clouds white"],
    "Star": ["stars night sky beautiful", "shooting star", "galaxy stars", "star twinkling", "night sky moon stars"],
    "Moon": ["moon night beautiful full moon", "moon stars night", "crescent moon", "moon over sea", "moon sky"],
    "Sun": ["sunrise beautiful morning", "sunset orange sky", "sun over sea", "morning sun", "sun rays"],
    "Bird": ["beautiful bird parrot", "peacock feather", "bird flying sky", "sparrow bird", "kingfisher bird"],
    "Animal": ["elephant baby cute", "lion king forest", "tiger beautiful", "deer forest", "monkey cute"],
    "Baby": ["cute baby smiling", "baby playing", "baby sleeping cute", "baby with mother", "baby laughing"],
    "Teacher": ["teacher classroom teaching", "teacher students school", "teacher book", "school teacher", "teacher happy"],
    "Student": ["student studying book", "school students happy", "student classroom", "college student", "student graduation"],
    "Business": ["business meeting office", "business success", "startup office", "money business", "business handshake"],
    "Money": ["money coins success", "rupees cash", "money saving", "business money", "gold coins"],
    "Yoga": ["yoga pose meditation", "yoga sunrise", "yoga girl", "yoga beach", "yoga peaceful"],
    "Meditation": ["meditation peaceful calm", "meditation Buddha", "meditation nature", "meditation sunset", "meditation lotus"],
    "Fitness": ["fitness gym workout", "running fitness", "fitness girl", "workout dumbbell", "fitness healthy"],
    "Diet": ["healthy diet salad", "fruits healthy", "vegetables fresh", "healthy food bowl", "diet food"],
    "Sleep": ["sleeping baby peaceful", "night sleep moon", "bedroom sleep", "sleep cat", "peaceful sleep"],
    "Beauty": ["beautiful girl smiling", "beauty makeup", "beautiful woman saree", "beauty face", "beautiful eyes"],
    "Fashion": ["fashion girl saree", "fashion style", "fashion dress", "fashion model", "fashion shopping"],
    "Game": ["video game playing", "game console", "chess game", "football game", "game fun"],
    "Sport": ["football match stadium", "sports running", "tennis sport", "sports trophy", "sports training"],
    "Football": ["football match goal", "football player kicking", "football stadium", "football trophy", "football training"],
    "Science": ["science laboratory microscope", "scientist lab experiment", "science atom molecule", "science test tube", "science research"],
    "History": ["history ancient temple", "history fort", "history palace", "history museum", "history old"],
    "Culture": ["Indian culture festival", "Tamil culture dance", "culture traditional", "culture art", "culture festival"],
    "Festival": ["Diwali festival lights", "Pongal festival Tamil", "festival celebration", "festival fireworks", "festival dance"],
    "Marriage": ["Indian wedding couple", "wedding bride saree", "wedding celebration", "wedding couple", "wedding decorations"],
    "Family": ["happy family together", "family picnic", "family smiling", "family home", "family festival"],
    "Friendship": ["friends together happy", "friendship group", "friends laughing", "friends travel", "best friends"],
    "Study": ["study book reading", "student studying library", "study desk", "study notes", "study exam"],
    "Dream": ["dream clouds sky", "dream fantasy", "dream stars", "dream girl", "dream beautiful"],
    "Success": ["success trophy winning", "success business", "success celebration", "success goal", "success motivation"],
    "Motivation": ["motivation sunrise success", "motivation quote", "motivation gym", "motivation book", "motivation mountain"],
    "Peace": ["peace dove white", "peaceful nature", "peace meditation", "peace sunset", "peaceful lake"],
    "Courage": ["courage lion brave", "courage mountain", "courage fire", "courage hero", "courage success"],
    "Kindness": ["kindness helping", "kindness heart", "kindness children", "kindness love", "kindness sharing"],
    "Truth": ["truth light", "truth book", "truth wisdom", "truth temple", "truth sunrise"],
    "Wisdom": ["wisdom old book", "wisdom Buddha", "wisdom owl", "wisdom temple", "wisdom light"],
    "Power": ["power lightning", "power lion", "power fire", "power mountain", "power energy"],
    "Magic": ["magic fantasy castle", "magic wand", "magic stars", "magic book", "magic forest"],
    "Luck": ["luck four leaf clover", "luck horseshoe", "luck gold", "luck festival", "luck rainbow"],
    "Destiny": ["destiny stars fate", "destiny path", "destiny road", "destiny sunset", "destiny dream"],
    "Karma": ["karma cycle", "karma temple", "karma meditation", "karma Buddha", "karma peace"],
    "Rain": ["rain monsoon beautiful", "rain drops", "rain umbrella", "rain forest", "rain window"],
    "Village": ["Indian village beautiful", "village hut", "village field", "village festival", "village sunset"],
    "City": ["city skyline night", "Chennai city", "city traffic", "city buildings", "city lights"],
    "Chennai": ["Chennai Marina beach", "Chennai temple", "Chennai city", "Chennai Marina", "Chennai food"],
    "Madurai": ["Madurai Meenakshi temple", "Madurai city", "Madurai temple festival", "Madurai street", "Madurai food"],
    "Delhi": ["Delhi India Gate", "Delhi Red Fort", "Delhi city", "Delhi temple", "Delhi street"],
    "Mumbai": ["Mumbai Gateway of India", "Mumbai city", "Mumbai beach", "Mumbai skyline", "Mumbai street"],
    "London": ["London Big Ben", "London bridge", "London city", "London tower", "London street"],
    "Paris": ["Paris Eiffel Tower", "Paris city", "Paris cafe", "Paris sunset", "Paris street"],
    "Tokyo": ["Tokyo Japan tower", "Tokyo city night", "Tokyo street", "Tokyo sakura", "Tokyo temple"],
    "New York": ["New York Times Square", "New York city", "New York Statue of Liberty", "New York skyline", "New York street"],
    "Egypt": ["Egypt pyramids", "Egypt sphinx", "Egypt desert", "Egypt temple", "Egypt Nile"],
    "Pyramids": ["Pyramids Egypt desert", "Pyramids sunset", "Pyramids ancient", "Pyramids camel", "Pyramids night"],
    "Taj Mahal": ["Taj Mahal India beautiful", "Taj Mahal sunset", "Taj Mahal marble", "Taj Mahal Agra", "Taj Mahal morning"],
    "Eiffel Tower": ["Eiffel Tower Paris", "Eiffel Tower sunset", "Eiffel Tower night", "Eiffel Tower city", "Eiffel Tower beautiful"],
    "Psychology": ["psychology brain mind", "psychology book", "psychology meditation", "psychology brain", "psychology therapy"],
    "Philosophy": ["philosophy book wisdom", "philosophy Buddha", "philosophy temple", "philosophy thought", "philosophy sunset"],
    "Economics": ["economics money chart", "economics business", "economics graph", "economics coins", "economics office"],
    "Politics": ["politics parliament", "politics flag", "politics meeting", "politics India", "politics vote"],
    "Law": ["law court justice", "law book", "law scales", "law judge", "law building"],
    "Education": ["education school books", "education graduation", "education classroom", "education library", "education students"],
    "Happiness": ["happy smiling girl", "happiness family", "happiness friends", "happiness sunset", "happiness dance"],
    "Smile": ["smiling girl cute", "smile happy", "smile baby", "smile friends", "smile beautiful"],
    "Heart": ["heart shape red love", "heart hands", "heart cute", "heart pink", "heart love"],
    "Future": ["future technology robot", "future city", "future space", "future dream", "future sunset"],
    "Freedom": ["freedom bird flying", "freedom flag", "freedom sky", "freedom dove", "freedom happy"],
    "Hope": ["hope sunrise", "hope light", "hope rainbow", "hope hands", "hope dream"],
    "Faith": ["faith temple prayer", "faith light", "faith cross", "faith meditation", "faith hope"],
    "Japan": ["Japan Tokyo tower", "Japan sakura cherry blossom", "Japan kimono girl", "Japan temple Kyoto", "Japan sushi food"],
    "Sakura": ["Sakura cherry blossom Japan pink", "Sakura tree Japan", "Sakura petals", "Sakura park Japan", "Sakura spring"],
    "Kimono": ["Kimono Japanese woman beautiful", "Kimono girl Japan", "Kimono red", "Kimono traditional", "Kimono festival"],
    "Anime": ["Anime girl cute illustration", "Anime boy cool", "Anime fantasy", "Anime city", "Anime couple"],
    "Japanese Food": ["Japanese food sushi ramen", "Sushi Japanese", "Ramen Japanese", "Japanese curry", "Japanese tea"],
    "Sushi": ["Sushi Japanese food plate", "Sushi salmon", "Sushi chef", "Sushi rice", "Sushi beautiful"],
    "Kyoto": ["Kyoto Japan temple red", "Kyoto torii gate", "Kyoto bamboo forest", "Kyoto street", "Kyoto sakura"],
    "Osaka": ["Osaka Japan castle", "Osaka street food", "Osaka city night", "Osaka tower", "Osaka temple"],
    "Japanese Temple": ["Japanese temple Kyoto", "Japanese shrine torii", "Japanese temple sunset", "Japanese temple garden", "Japanese temple snow"],
    "Japanese Girl": ["Japanese girl kimono smiling", "Japanese girl cute", "Japanese girl portrait", "Japanese girl sakura", "Japanese girl street"],
    "Samurai": ["Samurai Japan sword", "Samurai warrior", "Samurai armor", "Samurai katana", "Samurai castle"],
    "Ninja": ["Ninja Japan", "Ninja warrior", "Ninja shadow", "Ninja sword", "Ninja night"],
    "China": ["China Beijing Great Wall", "China panda cute", "China temple red", "China Shanghai city", "China dragon"],
    "Beijing": ["Beijing Forbidden City", "Beijing Great Wall", "Beijing temple", "Beijing street", "Beijing city"],
    "Great Wall": ["Great Wall of China mountain", "Great Wall sunset", "Great Wall ancient", "Great Wall fog", "Great Wall tourist"],
    "Panda": ["Panda cute baby", "Panda eating bamboo", "Panda smiling", "Panda zoo", "Panda baby"],
    "Chinese Food": ["Chinese food noodles", "Chinese dim sum", "Chinese rice", "Chinese dumplings", "Chinese restaurant"],
    "Chinese Temple": ["Chinese temple red lantern", "Chinese temple Beijing", "Chinese temple dragon", "Chinese temple sunset", "Chinese temple garden"],
    "Shanghai": ["Shanghai city skyline", "Shanghai night", "Shanghai tower", "Shanghai street", "Shanghai river"],
    "Chinese Culture": ["Chinese culture dragon dance", "Chinese lantern festival", "Chinese tea ceremony", "Chinese calligraphy", "Chinese opera"],
    "Dragon": ["Chinese dragon festival", "Dragon fire", "Dragon fantasy", "Dragon red", "Dragon temple"],
    "Chinese Girl": ["Chinese girl hanfu smiling", "Chinese girl cute", "Chinese girl portrait", "Chinese girl traditional", "Chinese girl street"],
    "India": ["India Taj Mahal", "India temple", "India festival Diwali", "India food biryani", "India village"],
    "Tamil Nadu": ["Tamil Nadu temple gopuram", "Tamil Nadu Madurai", "Tamil Nadu Chennai", "Tamil Nadu village", "Tamil Nadu dance"],
    "Kerala": ["Kerala backwaters boat", "Kerala coconut trees", "Kerala Kathakali", "Kerala beach", "Kerala tea plantation"],
    "Saree": ["Saree Indian woman beautiful", "Saree red bride", "Saree silk", "Saree girl smiling", "Saree traditional"],
    "Biryani": ["Biryani Indian food plate", "Chicken biryani", "Biryani rice", "Biryani Hyderabadi", "Biryani delicious"],
    "Diwali": ["Diwali festival lights diya", "Diwali fireworks", "Diwali rangoli", "Diwali family", "Diwali sweets"],
    "Pongal": ["Pongal festival Tamil pot", "Pongal kolam", "Pongal village", "Pongal sugarcane", "Pongal celebration"],
    "Indian Temple": ["Indian temple gopuram south", "Indian temple sunset", "Indian temple festival", "Indian temple architecture", "Indian temple pond"],
    "Indian Food": ["Indian food thali", "Indian dosa", "Indian curry", "Indian sweets", "Indian street food"],
    "Indian Girl": ["Indian girl saree smiling", "Indian girl cute", "Indian girl portrait", "Indian girl traditional", "Indian girl festival"],
    "Kolkata": ["Kolkata Howrah bridge", "Kolkata Durga Puja", "Kolkata street", "Kolkata tram", "Kolkata temple"],
    "Bangalore": ["Bangalore city garden", "Bangalore palace", "Bangalore IT city", "Bangalore park", "Bangalore street"],
    "Hyderabad": ["Hyderabad Charminar", "Hyderabad biryani", "Hyderabad city", "Hyderabad Golconda", "Hyderabad lake"],
    "Beach": ["Beach sunset palm", "Beach waves", "Beach sand", "Beach coconut", "Beach boat"],
    "Forest": ["Forest green trees", "Forest waterfall", "Forest animals", "Forest mist", "Forest path"],
    "Desert": ["Desert dunes camel", "Desert sunset", "Desert cactus", "Desert night stars", "Desert Rajasthan"],
    "Snow": ["Snow mountain white", "Snow falling", "Snow winter", "Snow man", "Snow forest"],
    "Fire": ["Fire flames", "Fire camp", "Fire diya", "Fire fireworks", "Fire sunset"],
    "Earth": ["Earth planet space", "Earth globe", "Earth nature", "Earth green", "Earth sunrise"],
    "Water": ["Water drops", "Water waterfall", "Water lake", "Water ocean", "Water glass"],
    "Coffee": ["Coffee cup hot", "Coffee latte art", "Coffee beans", "Coffee cafe", "Coffee morning"],
    "Tea": ["Tea cup masala", "Tea plantation", "Tea green", "Tea pouring", "Tea evening"],
    "Cake": ["Cake chocolate birthday", "Cake slice", "Cake strawberry", "Cake baking", "Cake celebration"],
    "Pizza": ["Pizza cheese", "Pizza oven", "Pizza slice", "Pizza Italian", "Pizza delicious"],
    "Burger": ["Burger cheese", "Burger fries", "Burger fast food", "Burger delicious", "Burger chicken"],
    "Chocolate": ["Chocolate dark", "Chocolate cake", "Chocolate box", "Chocolate melting", "Chocolate sweets"],
    "Fruit": ["Fruits fresh mango", "Fruits apple", "Fruits banana", "Fruits strawberry", "Fruits basket"],
    "Vegetable": ["Vegetables fresh green", "Vegetables market", "Vegetables tomato", "Vegetables farm", "Vegetables salad"],
    "Summer": ["Summer beach sun", "Summer ice cream", "Summer sun", "Summer mango", "Summer vacation"],
    "Winter": ["Winter snow sweater", "Winter fog", "Winter morning", "Winter bonfire", "Winter hills"],
    "Monsoon": ["Monsoon rain clouds", "Monsoon umbrella", "Monsoon window rain", "Monsoon green", "Monsoon chai"],
    "Morning": ["Morning sunrise tea", "Morning yoga", "Morning mist", "Morning birds", "Morning coffee"],
    "Night": ["Night stars moon", "Night city lights", "Night sky", "Night lamp", "Night peaceful"],
    "Home": ["Home cozy living room", "Home garden", "Home kitchen", "Home warm", "Home family"],
    "Garden": ["Garden flowers beautiful", "Garden green", "Garden roses", "Garden bench", "Garden sunset"],
    "Park": ["Park green trees", "Park children playing", "Park bench", "Park morning walk", "Park flowers"],
    "Elephant": ["Elephant baby cute", "Elephant temple Kerala", "Elephant forest", "Elephant family", "Elephant water"],
    "Tiger": ["Tiger forest beautiful", "Tiger cub", "Tiger roaring", "Tiger jungle", "Tiger eyes"],
    "Lion": ["Lion king mane", "Lion roaring", "Lion family", "Lion safari", "Lion cub"],
    "Horse": ["Horse white running", "Horse brown", "Horse riding", "Horse farm", "Horse sunset"],
    "Bike": ["Bike Royal Enfield", "Bike rider", "Bike road", "Bike sunset", "Bike racing"],
    "Car": ["Car luxury", "Car road trip", "Car red", "Car vintage", "Car sunset"],
    "Train": ["Train Indian railways", "Train journey", "Train station", "Train sunset", "Train mountain"],
    "Flight": ["Flight airplane sky", "Flight takeoff", "Flight window clouds", "Flight sunset", "Flight airport"],
    "Phone": ["Phone smartphone", "Phone holding", "Phone camera", "Phone new", "Phone desk"],
    "Computer": ["Computer laptop coding", "Computer desk", "Computer gaming", "Computer keyboard", "Computer screen"],
    "Book": ["Book reading library", "Book open", "Book stack", "Book coffee", "Book story"],
    "Kavithai": ["Kavithai Tamil poetry", "Poetry book", "Poetry pen", "Poetry sunset", "Poetry love"],
    "Thirukkural": ["Thirukkural Tamil book", "Thiruvalluvar statue", "Tamil book old", "Thirukkural temple", "Tamil palm leaf"],
    "Pazhamozhi": ["Pazhamozhi Tamil proverb", "Tamil village old", "Tamil grandmother story", "Tamil culture", "Tamil book"],
    "Joke": ["Joke funny laughing", "Comedy laughing", "Funny clown", "Funny meme", "Laughing friends"],
    "Reading": ["Reading book library", "Reading girl", "Reading coffee book", "Reading night", "Reading park"],
    "Writing": ["Writing pen diary", "Writing book", "Writing letter", "Writing desk", "Writing poetry"],
    "Poetry": ["Poetry book pen", "Poetry sunset", "Poetry love", "Poetry rose", "Poetry rain"],
    "Singing": ["Singing microphone stage", "Singing girl", "Singing concert", "Singing karaoke", "Singing choir"],
    "Dancing": ["Dancing Bharatanatyam", "Dancing couple", "Dancing stage", "Dancing festival", "Dancing happy"],
}

def get_infinite_prompt(cat, n):
    # n = 1..100 - 5 prompt rotate infinite - 1,2,3,4,5,1,2,3,4,5...
    lst = IMAGE_PROMPTS.get(cat)
    if not lst:
        return cat
    return lst[(n-1) % len(lst)]

def search_term(cat):
    return SEARCH_MAP.get(cat, cat)

def send_to_channel(text, bot_token, bot_name="Worker"):
    if not bot_token or not DATA_CHANNEL: return False
    for attempt in range(2):
        try:
            r = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": DATA_CHANNEL, "text": text[:4000]}, timeout=15)
            print(f"Worker Send: {r.status_code} to Data Channel - {bot_name}", flush=True)
            if r.status_code==200: return True
            if r.status_code==400:
                print(f"Worker Send 400 - {bot_name} - {r.text[:200]}", flush=True)
                time.sleep(2); continue
            time.sleep(1)
        except Exception as e: print(f"Worker Send Error {e}", flush=True); time.sleep(2)
    return False

# --- FREE SOURCES - No Watermark - No Key - No Login ---
# 1. Openverse - 800M free photos - No watermark - Best for Japan/China/India!
# 2. Wikimedia - 100M free photos - No watermark
# 3. Unsplash Source - Free - No watermark
def fetch_openverse(query, page=1):
    try:
        r = requests.get("https://api.openverse.org/v1/images/", params={"q": query, "page": page, "page_size": 20}, headers={"User-Agent": "AIRAH1-Bot/1.0"}, timeout=20)
        if r.status_code == 200:
            out = []
            for it in r.json().get("results", []):
                u = it.get("foreign_landing_url") or it.get("url")
                if u: out.append(u)
            return out
    except Exception as e: print(f"Openverse Error {e}", flush=True)
    return []

def fetch_wikimedia(query):
    try:
        r = requests.get("https://commons.wikimedia.org/w/api.php", params={"action":"query","format":"json","list":"search","srsearch":query,"srnamespace":6,"srlimit":20}, headers={"User-Agent": "AIRAH1-Bot/1.0 (Tamil Books)"}, timeout=20)
        if "application/json" not in r.headers.get("content-type",""): return []
        out = []
        for item in r.json().get("query",{}).get("search",[])[:20]:
            t = item.get("title","")
            if t: out.append(f"https://commons.wikimedia.org/wiki/{t.replace(' ','_')}")
        return out
    except Exception as e: print(f"Wikimedia Error {e}", flush=True); return []

def bot1_image_worker():
    # RESUME: GitHub la Last Category Paaru - Tamil la Irundhu Thirumba Start Aaga Venaam!
    _resume_cat, _resume_n = load_progress()
    idx = 0
    global START_N
    START_N = 1
    if _resume_cat and _resume_cat in BASE_CATS:
        idx = BASE_CATS.index(_resume_cat)
        print(f"RESUME: Start Category {_resume_cat} - Idx {idx} - Last N {_resume_n}", flush=True)
        if _resume_n and _resume_n < 100:
            START_N = _resume_n + 1
            print(f"RESUME: Count Resume - {START_N}/100 la Irundhu Thodarum! - 1 la Irundhu Illa!", flush=True)
        # If last category was 100/100 mudinjiduchu - Next category ku Po!
        if _resume_n >= 100:
            idx += 1
            print(f"RESUME: {_resume_cat} 100/100 Mudinjiduchu - Next {BASE_CATS[idx % len(BASE_CATS)]}", flush=True)

    while True:
        try:
            cat = BASE_CATS[idx % len(BASE_CATS)]; idx += 1
            q = search_term(cat)
            print(f"Bot1 - Category: {cat} - Search: {q} - 100 Image Start! - Repo {CURRENT_REPO[0]}", flush=True)
            # Collect pool - Openverse + Wikimedia - Infinite source
            pool = []
            # Openverse - 3 pages = 60 images
            for p in [1,2,3]:
                pool += fetch_openverse(q, page=p)
                time.sleep(1)
            # Wikimedia - 20 images
            pool += fetch_wikimedia(q)
            # Unsplash - backup - 20 slots (same base URL with different query, Telegram will preview)
            # Deduplicate, keep order
            seen = set(); uniq = []
            for u in pool:
                if u not in seen: seen.add(u); uniq.append(u)
            pool = uniq
            print(f"Bot1 - {cat} - Pool {len(pool)} - Start 100 loop", flush=True)
            # FIX: Oru category ku 100/100 varaikkum angaye iru! 7/100 illa!
            # INFINITE PROMPT: 5 prompt rotate - cache per prompt
            prompt_cache = {}
            def get_pool_for_prompt(prompt_text):
                if prompt_text in prompt_cache: return prompt_cache[prompt_text]
                pool2 = []
                for pp in [1,2]:
                    pool2 += fetch_openverse(prompt_text, page=pp)
                    time.sleep(0.5)
                pool2 += fetch_wikimedia(prompt_text)
                seen2 = set(); uniq2 = []
                for u in pool2:
                    if u not in seen2: seen2.add(u); uniq2.append(u)
                prompt_cache[prompt_text] = uniq2
                return uniq2
            for n in range(START_N, 101):
                try:
                    prompt_now, master_now = get_master_prompt(cat, n)
                    pool_now = get_pool_for_prompt(prompt_now)
                    if pool_now:
                        url = pool_now[(n-1) % len(pool_now)]
                        if "commons.wikimedia" in url: src = "Wikimedia"
                        elif "unsplash" in url: src = "Unsplash"
                        else: src = "Openverse"
                    else:
                        url = f"https://source.unsplash.com/800x600/?{prompt_now.replace(' ','%20')}"
                        src = "Unsplash"
                    if n % 10 == 0:
                        url = f"https://source.unsplash.com/800x600/?{prompt_now.replace(' ','%20')}"
                        src = "Unsplash"
                    send_to_channel(f"Auto Image - {cat} - {n}/100 | Master Prompt: {master_now} 📸\nSource: {src} - No Watermark - Made by Aira H1 ❤️\n{url}", BOT1_TOKEN, "Bot1-Image")
                    save_github(f"images-{cat}-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{cat} - {src} - {url}")
                    print(f"Bot1 - {cat} - {n}/100 Done!", flush=True)
                    save_progress(cat, n)
                    time.sleep(2)  # Slow - 2 sec ku 1 image - Spam illa
                except Exception as e: print(f"Bot1 100 Error {e}", flush=True); time.sleep(2)
            print(f"Bot1 Done - {cat} - 100/100 - Next Category!", flush=True)
            START_N = 1  # FIX: Next Category 1 la Irundhu Start Aaganum - 12 la Illa!
            time.sleep(10)
        except Exception as e: print(f"Bot1 Error {e}", flush=True); time.sleep(30)

def bot2_knowledge_worker():
    idx = 0
    while True:
        try:
            topic = BASE_CATS[idx % len(BASE_CATS)]; idx += 1
            print(f"Bot2 - Topic: {topic} - Batch {idx}", flush=True)
            try:
                r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ','_')}", headers={"User-Agent": "AIRAH1-Bot/1.0"}, timeout=10)
                if r.status_code==200:
                    ex = r.json().get("extract","")[:600]
                    if ex:
                        send_to_channel(f"Auto Knowledge - {topic} 🧠\n{ex}", BOT2_TOKEN, "Bot2-Wiki")
                        save_github(f"knowledge-worker-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{topic} - {ex}")
            except Exception as e: print(f"Wiki Error {e}", flush=True)
            try:
                r = requests.get("https://openlibrary.org/search.json", params={"q":topic,"limit":5}, timeout=10)
                for b in r.json().get("docs",[])[:3]:
                    title = b.get("title","")
                    if title:
                        send_to_channel(f"Auto Book - {topic} - {title} 📚", BOT2_TOKEN, "Bot2-Book")
                        save_github(f"books-worker-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{topic} - {title}")
            except Exception as e: print(f"OpenLibrary Error {e}", flush=True)
            try:
                r = requests.get("https://archive.org/advancedsearch.php", params={"q":f"title:({topic}) AND mediatype:texts","fl[]":"identifier,title","rows":5,"output":"json"}, timeout=15)
                for d in r.json().get("response",{}).get("docs",[])[:2]:
                    ident = d.get("identifier",""); title = d.get("title","Book")
                    if ident:
                        send_to_channel(f"Auto Book Archive - {topic} - {title} 📚\nhttps://archive.org/details/{ident}", BOT2_TOKEN, "Bot2-Archive")
                        save_github(f"books-archive-{datetime.now().strftime('%Y-%m-%d')}.txt", f"{topic} - {ident} - {title}")
            except Exception as e: print(f"Archive Error {e}", flush=True)
            try:
                r = requests.get("https://opentdb.com/api.php", params={"amount":1,"type":"multiple"}, timeout=10)
                if r.status_code==200:
                    qd = r.json().get("results",[])[0]
                    # FIX: &quot; pogum - html.unescape + tags remove
                    ques = re.sub(r'<[^>]+>', '', html.unescape(qd.get('question','')))
                    ans = re.sub(r'<[^>]+>', '', html.unescape(qd.get('correct_answer','')))
                    cat2 = re.sub(r'<[^>]+>', '', html.unescape(qd.get('category','')))
                    msg = f"Auto Quiz - {topic} 🧠\nQ: {ques}\nA: {ans} - {cat2}"
                    send_to_channel(msg, BOT2_TOKEN, "Bot2-Quiz")
                    save_github(f"quiz-worker-{datetime.now().strftime('%Y-%m-%d')}.txt", msg)
            except Exception as e: print(f"Quiz Error {e}", flush=True)
            print(f"Bot2 Done - {topic} - Infinite Next!", flush=True)
            time.sleep(30)
        except Exception as e: print(f"Bot2 Error {e}", flush=True); time.sleep(30)

def self_heal():
    while True:
        try:
            time.sleep(60)
            print(f"Self-Heal - Worker - Repo {CURRENT_REPO[0]} - OK", flush=True)
            save_github(f"heartbeat-worker-{datetime.now().strftime('%Y-%m-%d')}.txt", f"Worker Alive - {datetime.now()} - Repo {CURRENT_REPO[0]}")
        except Exception as e: print(f"Self-Heal Error {e}", flush=True); time.sleep(30)




# --- RESUME FIX V6 - Category Reset Aaga Koodaathu! ---
# Problem: Deploying vantha - Puthu Bot Tamil 1/100 la Irundhu Start Aaguthu - Love/God/Nature Progress Poiduthu!
# Fix: Oru Category Mudiyum Pothu + Oru Image Mudiyum Pothu - GitHub la Progress Save Pannuvom - Puthu Bot Athula Irundhu Thodarum!
def save_progress(cat, n):
    try: save_github("progress-worker.txt", f"{cat}|{n}|{datetime.now().isoformat()}")
    except: pass
def load_progress():
    try:
        import base64 as _b64
        url = f"https://api.github.com/repos/{GITHUB_USER}/{CURRENT_REPO[0]}/contents/data/progress-worker.txt"
        r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        if r.status_code == 200:
            content = _b64.b64decode(r.json().get("content","")).decode(errors="ignore").strip().split("\n")[-1]
            parts = content.split("|")
            if len(parts) >= 2:
                print(f"RESUME: Last Progress - {parts[0]} - {parts[1]}/100 - Athula Irundhu Thodarum!", flush=True)
                return parts[0], int(parts[1])
    except Exception as e: print(f"Resume Load Error {e}", flush=True)
    return None, 0

# --- CHATGPT IMAGEGEN MASTER - INFINITE - A TO Z - V5 ---
# Professional Prompt Structure: Subject + Appearance + Clothing + Pose + Expression + Environment + Camera + Lighting + Style + Colour + Composition + Detail + Aspect + Preserve + Avoid
# Infinite = Category (150+) x Camera (10) x Lighting (10) x Style (10) = 150,000+ Combo! Vera Photo Varaathu!
IMAGEGEN_CAMERAS = ["50mm natural perspective, eye level, full-body shot", "85mm portrait, three-quarter view, close-up", "35mm environmental photography, wide angle", "24mm wide angle, low angle", "100mm macro, extreme close-up", "14mm ultra-wide, bird's-eye view", "135mm compressed portrait, side view", "50mm, over-the-shoulder, medium shot", "85mm, front view, medium shot", "35mm, Dutch angle, full-body shot"]
IMAGEGEN_LIGHTINGS = ["golden hour, soft daylight, warm glow", "studio softbox, diffused lighting, clean", "rim lighting, backlighting, dramatic", "neon lighting, cinematic, colourful", "moonlight, blue hour, calm", "candlelight, warm, intimate", "volumetric lighting, god rays", "chiaroscuro, dramatic contrast", "soft daylight, natural, bright", "ambient lighting, balanced"]
IMAGEGEN_STYLES = ["photorealism, hyperrealism, sharp detail", "Japanese anime, manga style, vibrant", "cinematic realism, film grain, depth of field", "Pixar-inspired cartoon, cute, stylized 3D", "watercolor, soft, artistic", "oil painting, rich texture", "digital painting, detailed", "cyberpunk, neon, futuristic", "dark fantasy, moody", "storybook illustration, warm"]
IMAGEGEN_ASPECTS = ["9:16 vertical", "1:1 square", "16:9 landscape", "4:5 portrait", "3:4 portrait"]

def get_master_prompt(cat, n):
    # n = 1..100 - Infinite combo rotate - Camera, Lighting, Style, Aspect ellam rotate aagum!
    base = IMAGE_PROMPTS.get(cat, [cat])[ (n-1) % len(IMAGE_PROMPTS.get(cat, [cat])) ] if cat in IMAGE_PROMPTS else cat
    cam = IMAGEGEN_CAMERAS[(n-1) % len(IMAGEGEN_CAMERAS)]
    light = IMAGEGEN_LIGHTINGS[(n-1) % len(IMAGEGEN_LIGHTINGS)]
    style = IMAGEGEN_STYLES[(n-1) % len(IMAGEGEN_STYLES)]
    aspect = IMAGEGEN_ASPECTS[(n-1) % len(IMAGEGEN_ASPECTS)]
    # Professional Master Prompt - For Openverse Search: short search term + For Caption: full master prompt
    search_term = base
    master_prompt = f"SUBJECT: {base} | APPEARANCE: beautiful, natural, detailed | POSE: natural pose | EXPRESSION: smiling, warm | ENVIRONMENT: beautiful background | CAMERA: {cam} | LIGHTING: {light} | ART STYLE: {style} | COLOUR: vibrant, balanced | COMPOSITION: rule of thirds, focal point, negative space | DETAIL: sharp, high texture | ASPECT: {aspect} | AVOID: watermark, blur, distorted hands, bad text"
    return search_term, master_prompt

# --- SINGLE INSTANCE GUARD - Double Bot Stop! ---
# Render la Deploying Thirumba Varum pothu - Pazhaya Bot innum Saagala - Puthu Bot Start Aagidum - Athanala Double!
# Ithu: Start aagum pothu GitHub Heartbeat paakum - 2 Min kulla Heartbeat iruntha - Vera Bot Oduthu nu - Ithu Wait Pannum / Exit Aagum!
import json as _json
def check_other_instance():
    try:
        from datetime import datetime as _dt, timezone as _tz
        url = f"https://api.github.com/repos/{GITHUB_USER}/{CURRENT_REPO[0]}/contents/data/heartbeat-worker-{_dt.now().strftime('%Y-%m-%d')}.txt"
        r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, timeout=10)
        if r.status_code == 200:
            import base64 as _b64
            content = _b64.b64decode(r.json().get("content","")).decode(errors="ignore")
            # Last line la timestamp irukku - "Worker Alive - 2026-11-07 11:54:xx"
            last_line = content.strip().split("\n")[-1]
            # Try parse datetime from line
            for fmt in ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"]:
                try:
                    # Find datetime substring
                    import re as _re
                    m = _re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", last_line)
                    if m:
                        last_dt = _dt.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
                        diff = (_dt.now() - last_dt).total_seconds()
                        print(f"Single-Instance Check - Last Heartbeat {diff:.0f} sec ago - {last_line[:80]}", flush=True)
                        if diff < 120:
                            print("Single-Instance GUARD: Vera Bot Oduthu! Ithu 90 sec Wait Panni Thirumba Check Pannum...", flush=True)
                            return False
                        break
                except: pass
    except Exception as e:
        print(f"Single-Instance Check Error {e} - Continue", flush=True)
    return True

def wait_for_single_instance():
    # Max 3 try - 90 sec each - Vera bot saagala na - Ithu Exit Aagidum - Double aagaathu!
    for attempt in range(3):
        if check_other_instance():
            print("Single-Instance GUARD: OK - Naan Mattum Thaan Oduren!", flush=True)
            return True
        print(f"Single-Instance GUARD: Wait {attempt+1}/3 - 90 sec...", flush=True)
        time.sleep(90)
    print("Single-Instance GUARD: Vera Bot Innum Oduthu - Naan Exit Aaguren - Double Stop!", flush=True)
    # Exit - Render will restart later - Pazhaya bot saagum pothu puthu bot varum
    import sys; sys.exit(0)


if __name__ == "__main__":
    print("AIRAH1 WORKER FINAL V4 - Started - Data Channel!", flush=True)
    # V4 FIX: Port First! - Render ku Port Udaney Kedaikkanum - Guard Wait Panna Kooda Port Open Irukkanum!
    def start_http():
        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
            class H(BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200); self.end_headers(); self.wfile.write(b"AIRAH1 Worker Final V4 ON")
                def do_HEAD(self):
                    self.send_response(200); self.end_headers()
                def log_message(self,*a): pass
            HTTPServer(("0.0.0.0", int(os.getenv("PORT","10000"))), H).serve_forever()
        except Exception as e:
            print(f"HTTP Error {e}", flush=True)
    threading.Thread(target=start_http, daemon=True).start()
    print("HTTP Server Started - Port Open - Render OK!", flush=True)
    # Guard Next - Double Stop!
    wait_for_single_instance()
    print("AIRAH1 WORKER FINAL V4 - Single Instance OK - Workers Start!", flush=True)
    threading.Thread(target=bot1_image_worker, daemon=True).start()
    threading.Thread(target=bot2_knowledge_worker, daemon=True).start()
    threading.Thread(target=self_heal, daemon=True).start()
    while True: time.sleep(60)
