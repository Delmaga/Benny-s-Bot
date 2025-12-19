import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime

MECANO_ROLE_ID = 123456789012345678  # ← À MODIFIER
LOG_FILE = "data/service_log.json"

def ensure_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump({}, f)

def load_log():
    ensure_data()
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def save_log(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def format_duration(sec):
    h, r = divmod(int(sec), 3600)
    m, s = divmod(r, 60)
    parts = []
    if h: parts.append(f"{h}h")
    if m: parts.append(f"{m}m")
    if s or not parts: parts.append(f"{s}s")
    return " ".join(parts)

class ServiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="onservice", description="Passer en service")
    async def onservice(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(MECANO_ROLE_ID)
        if not role:
            await interaction.response.send_message("`❌ Rôle introuvable.`")
            return
        if role in interaction.user.roles:
            await interaction.response.send_message("`✅ Déjà en service.`")
            return
        await interaction.user.add_roles(role)
        log = load_log()
        log[str(interaction.user.id)] = datetime.utcnow().isoformat()
        save_log(log)
        await interaction.response.send_message(
            f"`🟢 {interaction.user.mention} est maintenant **EN SERVICE**.`"
        )

    @app_commands.command(name="offservice", description="Quitter le service")
    async def offservice(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(MECANO_ROLE_ID)
        if not role:
            await interaction.response.send_message("`❌ Rôle introuvable.`")
            return
        if role not in interaction.user.roles:
            await interaction.response.send_message("`✅ Pas en service.`")
            return
        await interaction.user.remove_roles(role)
        log = load_log()
        user_id = str(interaction.user.id)
        start = log.get(user_id)
        if start:
            duration = (datetime.utcnow() - datetime.fromisoformat(start)).total_seconds()
            duration_str = format_duration(duration)
            del log[user_id]
            save_log(log)
            await interaction.response.send_message(
                f"`🔴 {interaction.user.mention} est **HORS SERVICE** après `{duration_str}`.`"
            )
        else:
            await interaction.response.send_message(
                f"`🔴 {interaction.user.mention} est **HORS SERVICE**.`"
            )

async def setup(bot):
    await bot.add_cog(ServiceCog(bot))