import os
import threading
import discord
from google import genai
from flask import Flask

# Flask web server da Render ne izbacuje Deploy Failed
app = Flask(__name__)

@app.route('/')
def home():
    return "Žile bot je aktivan!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Inicijalizacija Discord klijenta
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Inicijalizacija Gemini AI
ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@client.event
async def on_ready():
    print(f'Bot Žile je online kao {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        clean_text = message.content.replace(f'<@{client.user.id}>', '').strip()
        
        if not clean_text:
            await message.channel.send("Reci?")
            return

        async with message.channel.typing():
            try:
                prompt = f"Ti si Discord bot po imenu Žile. Odgovori izuzetno kratko, direktno i prirodno na srpskom (maksimalno 1 do 2 rečenice) na sledeće pitanje: {clean_text}"
                
                response = ai_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                await message.channel.send(response.text)
            except Exception as e:
                print(f"Greška: {e}")
                await message.channel.send("Greška pri obradi poruke.")

if __name__ == "__main__":
    # Pokreni Flask u posebnom thread-u
    threading.Thread(target=run_flask, daemon=True).start()
    # Pokreni Discord bota
    client.run(os.getenv("DISCORD_TOKEN"))

