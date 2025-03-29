import importlib
import sys
import asyncio
import threading
from flask import flask

from ubb import Ubot
from ubb.modules import ALL_MODULES


for module_name in ALL_MODULES:
    imported_module = importlib.import_module(f"ubb.modules.{module_name}")

# Create a simple Flask app for Render health checks
app = Flask(__name__)

@app.route("/")
def health_check():
    return "Bot is running!", 200

# Run Flask server in a separate thread
def run_web_server():
    app.run(host="0.0.0.0", port=8080)

async def main():
    async with Ubot:
        # Run the client until Ctrl+C is pressed, or the client disconnects
        print('Your bot is alive .alive to check\n'
              '.help to check command list\n'
              '(Press Ctrl+C to stop this)')
        await Ubot.run_until_disconnected()
        

if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()
    asyncio.run(main())
