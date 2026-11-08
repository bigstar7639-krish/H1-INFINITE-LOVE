# AIRAH1 - BOOKS FIX - Books ku Books Mattum! Knowledge Vara Koodathu!
# Problem: send_to_all() - Ellame Ellathukum Poguthu - Adhan Books ku Knowledge Vanthuchu!
# Fix: Ovoru Edathukum - Adhukku Etha Message Mattum Pogum!
import os, requests, time
TOKEN = os.getenv("BOT_TOKEN") or ""
GROUP_ID = "-1003935111481"  # H1 Aira Chat - Chat / Emotion / QA / Knowledge - Ellam Pesura Edam
BOOKS_ID = "-1003940504242"  # H1 Tamil Books - Books Mattum! Vera Edhuvum Vara Koodathu!
DATA_ID = "-1004366479419"   # H1 Aira Data - Data Mattum - Save / Count / Full Analysis
def send(chat_id, text):
    try:
        for i in range(0, len(text), 4000):
            part = text[i:i+4000]
            if len(text)>4000: part = f"Part {i//4000+1} -\n{part}"
            r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id":chat_id,"text":part}, timeout=15)
            print(f"TG Send {r.status_code} - {chat_id} - {len(part)} chars", flush=True); time.sleep(1)
    except Exception as e: print(f"TG Err {e}", flush=True)
def send_chat(text):
    # Chat ku - Emotion / QA / Knowledge / Daily / Chat - Pesura Message Mattum!
    send(GROUP_ID, text); print("Send Chat Group - Done", flush=True)
def send_books(text):
    # Books ku - Books Mattum! Book DATA / Book Katha / Book Full Analysis - Mattum!
    # Knowledge / Emotion / QA - Books ku Poga Koodathu!
    send(BOOKS_ID, text); print("Send Books Channel - Books Mattum - Done", flush=True)
def send_data(text):
    # Data ku - Data Mattum - Total Count / Save / Full Analysis Data
    send(DATA_ID, text); print("Send Data Channel - Done", flush=True)
# Eppadi Use Pannanum:
# Emotion -> send_chat(msg) - Chat ku Mattum! Books ku Pogaathu!
# QA -> send_chat(msg) - Chat ku Mattum!
# Knowledge -> send_chat(msg) - Chat ku Mattum!
# Book -> send_books(msg) + send_data(msg) - Books ku + Data ku! Chat ku Pogaathu! (Chat la Book Vendam na)
# Book Full Analysis -> send_books(msg) - Books ku Mattum!
# Total Count -> send_data(msg) - Data ku Mattum!
# Daily -> send_chat(msg) - Chat ku Mattum!
# Daily + Book -> Chat ku Book Vendam - Books ku Daily Vendam!
if __name__=="__main__":
    print("Books Fix - Books ku Books Mattum!", flush=True)
