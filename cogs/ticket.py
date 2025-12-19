# cogs/ticket.py
import discord
from discord import app_commands, ui
from discord.ext import commands
import json
import os
from datetime import datetime

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
        data[str_id] = {
            "categories": ["Problème technique", "Commande véhicule", "Renseignement", "Autre"],
            "ping_role": None
        }
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

class TicketView(ui.View):
    def __init__(self, categories, guild_id):
        super().__init__(timeout=180)
        self.guild_id = guild_id
        self.categories = categories
        self.add_item(TicketSelect(categories))

class TicketSelect(ui.Select):
    def __init__(self, categories):
        options = [discord.SelectOption(label=cat, value=cat) for cat in categories]
        super().__init__(placeholder="Choisissez une catégorie...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # ⚡ Réponse IMMÉDIATE (obligatoire)
        await interaction.response.defer(ephemeral=True)

        category = self.values[0]
        guild = interaction.guild
        user = interaction.user

        # Créer la catégorie de tickets si absente
        ticket_cat = discord.utils.get(guild.categories, name="🎟・Tickets")
        if not ticket_cat:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            ticket_cat = await guild.create_category("🎟・Tickets", overwrites=overwrites)

        # Créer le salon
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(f"ticket-{user.name}", category=ticket_cat, overwrites=overwrites)

        # Charger config
        config = get_guild_config(guild.id)
        ping = f"<@&{config['ping_role']}>" if config.get("ping_role") else "@everyone"
        now = datetime.now().strftime("%d %b %Y à %Hh%M")

        embed = discord.Embed(
            title="`***🎫Ticket - BENNY'S***`",
            description=(
                f"{ping}\n\n"
                "`***------------------------------***`\n\n"
                f"`***Nom :***` {user.mention}\n"
                f"`***Catégorie :***` `({category})`\n"
                f"`***Date :***` `({now})`\n\n"
                "Veuillez `***Détailler***` votre demande,\n"
                "Un Mécano vous répondra le plus `***rapidement possible 🔧,***`\n"
                "Délais possible entre `***24-48H***` 🕥."
            ),
            color=0x2b2d31
        )
        embed.set_footer(text="Benny's Custom Vehicles • GTA RP")
        await channel.send(embed=embed)

        # ✅ Répondre à l’utilisateur
        await interaction.followup.send(f"`✅ Votre ticket a été créé :` {channel.mention}", ephemeral=True)

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket", description="Ouvrir un ticket d'assistance")
    async def ticket(self, interaction: discord.Interaction):
        config = get_guild_config(interaction.guild_id)
        embed = discord.Embed(
            title="`***🎫Ticket - BENNY'S***`",
            description=(
                "Veuillez `***choisir***` la catégorie souhaitée,\n"
                "Un Mécano vous répondra le plus `***rapidement possible 🔧,***`\n"
                "Délais possible entre `***24-48H***` 🕥."
            ),
            color=0x2b2d31
        )
        embed.set_footer(text="Benny's Custom Vehicles • GTA RP")
        await interaction.response.send_message(
            embed=embed,
            view=TicketView(config["categories"], interaction.guild_id),
            ephemeral=True
        )

    @app_commands.command(name="add_categorie")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def add_categorie(self, interaction: discord.Interaction, nom: str):
        config = get_guild_config(interaction.guild_id)
        if nom in config["categories"]:
            await interaction.response.send_message("`❌ Catégorie déjà existante.`", ephemeral=True)
            return
        config["categories"].append(nom)
        update_guild_config(interaction.guild_id, "categories", config["categories"])
        await interaction.response.send_message(f"`✅ Catégorie '{nom}' ajoutée.`", ephemeral=True)

    @app_commands.command(name="del_categorie")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def del_categorie(self, interaction: discord.Interaction, nom: str):
        config = get_guild_config(interaction.guild_id)
        if nom not in config["categories"]:
            await interaction.response.send_message("`❌ Catégorie introuvable.`", ephemeral=True)
            return
        config["categories"].remove(nom)
        update_guild_config(interaction.guild_id, "categories", config["categories"])
        await interaction.response.send_message(f"`✅ Catégorie '{nom}' supprimée.`", ephemeral=True)

    @app_commands.command(name="ticket_ping")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def ticket_ping(self, interaction: discord.Interaction, role: discord.Role):
        update_guild_config(interaction.guild_id, "ping_role", role.id)
        await interaction.response.send_message(f"`✅ Rôle de ping :` {role.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketCog(bot))