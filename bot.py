import threading
import requests
import time

def keep_alive():
    # Replace with your actual Railway URL from Image 2
    url = "https://web-production-ee3d6.up.railway.app" 
    while True:
        try:
            requests.get(url)
            print("Pinged Railway to stay awake")
        except Exception as e:
            print(f"Keep-alive failed: {e}")
        time.sleep(300) # Ping every 5 minutes

# Add this right before bot.run_polling()
threading.Thread(target=keep_alive, daemon=True).start()
