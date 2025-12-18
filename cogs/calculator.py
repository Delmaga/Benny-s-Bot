import discord
from discord import ui, app_commands
from discord.ext import commands
import re

class CalcButton(ui.Button):
    def __init__(self, label, style=discord.ButtonStyle.grey, row=0):
        super().__init__(label=label, style=style, row=row)
        self.calc_label = label

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        if view.owner != interaction.user:
            await interaction.response.send_message("`❌ Ce n'est pas votre calculatrice.`", ephemeral=True)
            return

        if self.calc_label == "C":
            view.expr = "0"
        elif self.calc_label == "=":
            try:
                if re.fullmatch(r'[0-9+\-*/(). ]+', view.expr):
                    view.expr = str(eval(view.expr))
                else:
                    view.expr = "Erreur"
            except:
                view.expr = "Erreur"
        else:
            view.expr = self.calc_label if view.expr == "0" else view.expr + self.calc_label

        display_btn = view.children[0]
        display_btn.label = view.expr[-25:] if len(view.expr) <= 25 else "..." + view.expr[-22:]
        await interaction.response.edit_message(view=view)

class CalcView(ui.View):
    def __init__(self, owner):
        super().__init__(timeout=300)
        self.owner = owner
        self.expr = "0"
        self.add_item(ui.Button(label="0", style=discord.ButtonStyle.blurple, disabled=True, row=0))

        buttons = [
            ("C", 1, discord.ButtonStyle.red),
            ("(", 1, discord.ButtonStyle.grey), (")", 1, discord.ButtonStyle.grey), ("/", 1, discord.ButtonStyle.green),
            ("7", 2, discord.ButtonStyle.grey), ("8", 2, discord.ButtonStyle.grey), ("9", 2, discord.ButtonStyle.grey), ("*", 2, discord.ButtonStyle.green),
            ("4", 3, discord.ButtonStyle.grey), ("5", 3, discord.ButtonStyle.grey), ("6", 3, discord.ButtonStyle.grey), ("-", 3, discord.ButtonStyle.green),
            ("1", 4, discord.ButtonStyle.grey), ("2", 4, discord.ButtonStyle.grey), ("3", 4, discord.ButtonStyle.grey), ("+", 4, discord.ButtonStyle.green),
            ("0", 5, discord.ButtonStyle.grey), (".", 5, discord.ButtonStyle.grey), ("=", 5, discord.ButtonStyle.green)
        ]
        for label, row, style in buttons:
            self.add_item(CalcButton(label, style=style, row=row))

class CalculatorCog(commands.Cog):
    @app_commands.command(name="calculatrice", description="Calculatrice interactive Benny's")
    async def calculator(self, interaction: discord.Interaction):
        view = CalcView(owner=interaction.user)
        view.children[0].label = "0"
        await interaction.response.send_message("`🧮 Calculatrice Benny's`", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(CalculatorCog())