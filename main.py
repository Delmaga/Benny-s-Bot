import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Charger le token
load_dotenv()

# Configurer les intents nécessaires
intents = discord.Intents.default()
intents.members = True        # Pour /welcome et on_member_join
intents.message_content = True  # Pour lire les messages (si nécessaire)

# Créer le bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None  # Désactiver la commande !help
)

@bot.event
async def on_ready():
    print(f"✅ Royal Bot (Benny's) connecté en tant que {bot.user}")
    print(f"🔗 Connecté à {len(bot.guilds)} serveur(s)")

async def load_extensions():
    """Charge tous les cogs dans le dossier ./cogs/"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("__"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"📦 Cog chargé : {filename}")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {filename}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())