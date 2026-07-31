# REPLACE your old run_polling() line with this:
import time

while True:
    try:
        print("Attempting to connect to Telegram...")
        application.run_polling()  # If you use 'bot.polling()' instead, use that here.
        break # If it connects successfully, it will stay here.
    except Exception as e:
        print(f"Error connecting: {e}")
        print("Bot crashed. Waiting 5 seconds to retry...")
        time.sleep(5) # Wait 5 seconds before trying again
