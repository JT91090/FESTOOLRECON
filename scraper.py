import requests
import os

TOKEN = os.getenv("8583009431:AAHUyQVxGlueQJ4imaNX-6Ci3aWPn5U44y4")
CHAT_ID = os.getenv("8463304596")
URL = "https://www.festoolrecon.com"

def check_festool():
    response = requests.get(URL, timeout=15)
    current_len = str(len(response.text))

    # Read the previous size from a file in the repo
    try:
        with open("last_size.txt", "r") as f:
            last_len = f.read()
    except FileNotFoundError:
        last_len = ""

    if current_len != last_len:
        msg = f"🚀 FESTOOL UPDATE! Check now: {URL}"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={'chat_id': CHAT_ID, 'text': msg})
        
        # Write the new size back so we can "commit" it
        with open("last_size.txt", "w") as f:
            f.write(current_len)
        return True # Signal that a change happened
    return False

if __name__ == "__main__":
    check_festool()
