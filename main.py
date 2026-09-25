import os
import discord
from google import genai

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
    # Ignoriši poruke od samog bota
    if message.author == client.user:
        return

    # Proveri da li je bot tagovan
    if client.user.mentioned_in(message):
        # Ukloni tag iz poruke da ostane samo pitanje
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

client.run(os.getenv("DISCORD_TOKEN"))
