import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def health_check():
    return "Bot is running!", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Ensure it binds to Render's PORT
    app.run(host="0.0.0.0", port=port)
