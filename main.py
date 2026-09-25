import os
import discord
import google.generativeai as genai

# Inicijalizacija Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Inicijalizacija Discord klijenta
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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
                response = model.generate_content(prompt)
                await message.channel.send(response.text)
            except Exception as e:
                print(f"Greška: {e}")
                await message.channel.send("Greška pri obradi poruke.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    client.run(token)
