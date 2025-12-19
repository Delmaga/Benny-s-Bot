import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"🔄 Synchronisation des commandes slash...")
    await bot.tree.sync()  # ⚠️ À garder uniquement pour le déploiement
    print(f"✅ Royal Bot (Benny's) connecté en tant que {bot.user}")
    print(f"📚 Commandes slash synchronisées sur {len(bot.guilds)} serveur(s)")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("__"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"📦 Cog chargé : {filename}")
            except Exception as e:
                print(f"❌ Erreur dans {filename}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())