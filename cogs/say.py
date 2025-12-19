import discord
from discord import ui, app_commands
from discord.ext import commands

SAY_MESSAGES = {}

class SayModal(ui.Modal, title="`Composer un message`"):
    content = ui.TextInput(
        label="Contenu",
        style=discord.TextStyle.paragraph,
        placeholder="*italique*, _souligné_, ``code``, @mention, etc.",
        required=True,
        max_length=2000
    )

    def __init__(self, message_id=None, original=""):
        super().__init__()
        self.message_id = message_id
        if original:
            self.content.default = original

    async def on_submit(self, interaction: discord.Interaction):
        if self.message_id:
            if self.message_id not in SAY_MESSAGES:
                await interaction.response.send_message("`❌ Message non éditable.`")
                return
            channel = interaction.guild.get_channel(SAY_MESSAGES[self.message_id]["channel_id"])
            if not channel:
                await interaction.response.send_message("`❌ Salon introuvable.`")
                return
            try:
                msg = await channel.fetch_message(self.message_id)
                await msg.edit(content=self.content.value)
                await interaction.response.send_message("`✅ Message mis à jour.`")
            except:
                await interaction.response.send_message("`❌ Erreur lors de l'édition.`")
        else:
            msg = await interaction.channel.send(self.content.value)
            SAY_MESSAGES[msg.id] = {"channel_id": interaction.channel.id}
            await interaction.response.send_message("`✅ Message envoyé.`")

class SayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="say", description="Envoyer un message stylé")
    async def say(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SayModal())

    @app_commands.command(name="editsay", description="Modifier un message /say")
    async def editsay(self, interaction: discord.Interaction, message_id: str):
        try:
            msg_id = int(message_id)
        except ValueError:
            await interaction.response.send_message("`❌ ID invalide.`")
            return
        if msg_id not in SAY_MESSAGES:
            await interaction.response.send_message("`❌ Ce message n'est pas éditable.`")
            return
        original_content = ""
        try:
            channel = interaction.guild.get_channel(SAY_MESSAGES[msg_id]["channel_id"])
            if channel:
                msg = await channel.fetch_message(msg_id)
                original_content = msg.content
        except:
            pass
        await interaction.response.send_modal(SayModal(message_id=msg_id, original=original_content))

async def setup(bot):
    await bot.add_cog(SayCog(bot))