import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Charger le token
load_dotenv()

# Configurer les intents
intents = discord.Intents.default()
intents.members = True        # Pour on_member_join
intents.message_content = True  # Pour lire les messages (si nécessaire)

# Créer le bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"✅ Royal Bot (Benny's) connecté en tant que {bot.user}")

# Charger les cogs depuis le dossier ./cogs
async def load_cogs():
    cog_folder = "./cogs"
    if not os.path.exists(cog_folder):
        print("❌ Dossier 'cogs' introuvable.")
        return

    for filename in os.listdir(cog_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"📦 Cog chargé : {filename}")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {filename}: {e}")

# Fonction principale
async def main():
    await load_cogs()
    await bot.start(os.getenv("TOKEN"))

# Lancer le bot
if __name__ == "__main__":
    asyncio.run(main())