
# AIRAH1 - All Language Support - Infinite - Final
# Tamil + English + Hindi + Telugu + Malayalam + Kannada + Bengali + All Languages
# File: aira_server_all_lang.py

LANGUAGES = {
 "tamil": {"hi": "Vanakkam! Naan Aira!", "joke": "Joke", "love": "Kadhal na Anbu!"},
 "tanglish": {"hi": "Hi! Naan Aira! Enna pannura?", "joke": "Joke sollu", "love": "Kadhal na Anbu!"},
 "english": {"hi": "Hi! I am Aira! How are you?", "joke": "Tell me a joke", "love": "Love means care!"},
 "hindi": {"hi": "Namaste! Main Aira hoon!", "joke": "Joke sunao", "love": "Pyaar matlab care!"},
 "telugu": {"hi": "Namaste! Nenu Aira!", "joke": "Joke cheppu", "love": "Prema ante care!"},
 "malayalam": {"hi": "Namaskaram! Njan Aira!", "joke": "Joke parayu", "love": "Sneham ennal care!"},
 "kannada": {"hi": "Namaskara! Naanu Aira!", "joke": "Joke heli", "love": "Preethi andre care!"},
 "bengali": {"hi": "Nomoskar! Ami Aira!", "joke": "Joke bolo", "love": "Bhalobasha mane care!"},
 "marathi": {"hi": "Namaskar! Mi Aira!", "joke": "Joke sang", "love": "Prem mhanje care!"},
 "urdu": {"hi": "Assalam! Main Aira hoon!", "joke": "Joke sunao", "love": "Mohabbat matlab care!"},
 "spanish": {"hi": "Hola! Soy Aira!", "joke": "Dime un chiste", "love": "Amor es cuidado!"},
 "french": {"hi": "Bonjour! Je suis Aira!", "joke": "Dis-moi une blague", "love": "Amour c'est soin!"},
 "japanese": {"hi": "Konnichiwa! Watashi wa Aira!", "joke": "Joke oshiete", "love": "Ai wa care!"},
 "korean": {"hi": "Annyeong! Naneun Aira!", "joke": "Joke haejwo", "love": "Sarang eun care!"},
 "chinese": {"hi": "Ni Hao! Wo shi Aira!", "joke": "Jiang ge xiaohua", "love": "Ai shi care!"},
 "arabic": {"hi": "Marhaba! Ana Aira!", "joke": "Qul nokta", "love": "Hubb yaani care!"},
}

def detect_lang(text):
    low = text.lower()
    if any(x in low for x in ["vanakkam","kadhal","tamil","tanglish"]): return "tanglish"
    if any(x in low for x in ["namaste","pyaar","hindi","kya"]): return "hindi"
    if any(x in low for x in ["namaste","telugu","prema"]): return "telugu"
    if any(x in low for x in ["malayalam","sneham"]): return "malayalam"
    if any(x in low for x in ["kannada","preethi"]): return "kannada"
    if any(x in low for x in ["bengali","bhalobasha"]): return "bengali"
    if any(x in low for x in ["hola","spanish"]): return "spanish"
    if any(x in low for x in ["bonjour","french"]): return "french"
    if any(x in low for x in ["konnichiwa","japanese"]): return "japanese"
    if any(x in low for x in ["annyeong","korean"]): return "korean"
    if any(x in low for x in ["ni hao","chinese"]): return "chinese"
    if any(x in low for x in ["marhaba","arabic"]): return "arabic"
    return "english"

def reply_in_lang(text):
    lang = detect_lang(text)
    data = LANGUAGES.get(lang, LANGUAGES["english"])
    low = text.lower()
    if "hi" in low or "hello" in low or "vanakkam" in low or "namaste" in low:
        return data["hi"] + f" - {lang} la pesalam! Enna venum? Joke, Story, Fact?"
    if "joke" in low or "chiste" in low or "blague" in low:
        return f"{data['joke']}: Teacher - Yen late? Student - Road la board paathen! 😂 - Language: {lang}"
    if "love" in low or "kadhal" in low or "pyaar" in low or "prema" in low:
        return data["love"] + f" - Language: {lang}"
    return f"{data['hi']} - Nalla question! Daily try pannu - Jeyichiduva! - Language: {lang}"

# Test
for t in ["Hi Aira","Vanakkam Aira","Namaste Aira","Hola Aira","Bonjour Aira"]:
    print(t, "->", reply_in_lang(t))
