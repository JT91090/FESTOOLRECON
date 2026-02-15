import requests
import os

TOKEN = os.getenv(8583009431:AAHUyQVxGlueQJ4imaNX-6Ci3aWPn5U44y4)
CHAT_ID = os.getenv(8463304596)
# This is the "secret" clean data feed for the store
URL = "https://www.festoolrecon.com/products.json"
FILE_NAME = "last_seen_ids.txt"

def check_festool():
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print("Checking Festool Recon product feed...")
        response = requests.get(URL, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"Error: Could not access feed (Status {response.status_code})")
            return False

        data = response.json()
        products = data.get('products', [])
        
        # Get a list of all current product IDs
        # We filter for products that don't have "Wow, that went fast" in the description if possible
        current_ids = [str(p['id']) for p in products]
        current_ids_str = ",".join(sorted(current_ids))

        # Load the previous IDs
        last_ids_str = ""
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                last_ids_str = f.read().strip()

        # Compare
        if current_ids_str != last_ids_str:
            # Find exactly what is new
            last_ids_list = last_ids_str.split(",")
            new_products = [p for p in products if str(p['id']) not in last_ids_list]

            if new_products:
                print(f"Found {len(new_products)} new items!")
                for item in new_products:
                    title = item['title']
                    handle = item['handle']
                    price = item['variants'][0]['price']
                    link = f"https://www.festoolrecon.com/products/{handle}"
                    
                    msg = f"🚀 NEW FESTOOL DROP!\n\n🔨 {title}\n💰 ${price}\n🔗 {link}"
                    
                    # Send alert
                    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': msg})
            
            # Save the new state
            with open(FILE_NAME, "w") as f:
                f.write(current_ids_str)
            return True

        print("No new products found.")
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_festool()
