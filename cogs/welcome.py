import discord
from discord import app_commands
from discord.ext import commands
import json
import os

DATA_FILE = "data/config.json"

def ensure_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)

def get_guild_config(guild_id):
    ensure_data()
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    str_id = str(guild_id)
    if str_id not in 
        data[str_id] = {"welcome_channel": None, "welcome_role": None}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    return data[str_id]

def update_guild_config(guild_id, key, value):
    ensure_data()
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    str_id = str(guild_id)
    if str_id not in 
        data[str_id] = {}
    data[str_id][key] = value
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="welcome", description="Définir salon de bienvenue")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def welcome_channel(self, interaction: discord.Interaction, salon: discord.TextChannel):
        update_guild_config(interaction.guild_id, "welcome_channel", salon.id)
        await interaction.response.send_message(f"`✅ Salon de bienvenue :` {salon.mention}", ephemeral=True)

    @app_commands.command(name="welcome_role", description="Définir rôle d'accueil")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def welcome_role(self, interaction: discord.Interaction, role: discord.Role):
        update_guild_config(interaction.guild_id, "welcome_role", role.id)
        await interaction.response.send_message(f"`✅ Rôle attribué à l'arrivée :` {role.mention}", ephemeral=True)

    @app_commands.command(name="welcome_test", description="Tester le message")
    async def welcome_test(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="`Bienvenue sur BENNY'S !`",
            description=f"`Bienvenue {interaction.user.mention} ! 🛠️`\n"
                        "`Vérifie les règles et utilise **/ticket** pour toute demande.`",
            color=0x2b2d31
        )
        embed.set_image(url="https://i.imgur.com/6QbX6yA.gif")
        embed.set_footer(text="Benny's Custom Vehicles • GTA RP")
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = get_guild_config(member.guild.id)
        if config.get("welcome_role"):
            role = member.guild.get_role(config["welcome_role"])
            if role:
                await member.add_roles(role)
        if config.get("welcome_channel"):
            channel = member.guild.get_channel(config["welcome_channel"])
            if channel:
                embed = discord.Embed(
                    title="`Bienvenue sur BENNY'S !`",
                    description=f"`Bienvenue {member.mention} ! 🛠️`\n"
                                "`Vérifie les règles et utilise **/ticket** pour toute demande.`",
                    color=0x2b2d31
                )
                embed.set_image(url="https://i.imgur.com/6QbX6yA.gif")
                embed.set_footer(text="Benny's Custom Vehicles • GTA RP")
                await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))