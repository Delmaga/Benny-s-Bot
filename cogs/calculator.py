# cogs/calculator.py
import discord
from discord import ui, app_commands
from discord.ext import commands
import re

class CalcView(ui.View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=180)
        self.user = user
        self.expression = "0"
        self.update_display()

    def update_display(self):
        # Bouton affichage en haut
        if self.children and isinstance(self.children[0], ui.Button):
            self.children[0].label = self.expression[-25:] or "0"

    @ui.button(label="0", style=discord.ButtonStyle.blurple, disabled=True, row=0)
    async def display(self, interaction: discord.Interaction, button: ui.Button):
        pass  # Juste affichage

    async def handle_input(self, interaction: discord.Interaction, value: str):
        if interaction.user != self.user:
            await interaction.response.send_message("`❌ Ce n'est pas votre calculatrice.`", ephemeral=True)
            return

        if value == "C":
            self.expression = "0"
        elif value == "=":
            try:
                if re.fullmatch(r'[0-9+\-*/(). ]+', self.expression):
                    result = eval(self.expression)
                    self.expression = str(result)
                else:
                    self.expression = "Erreur"
            except:
                self.expression = "Erreur"
        else:
            if self.expression == "0":
                self.expression = value
            else:
                self.expression += value

        self.update_display()
        await interaction.response.edit_message(view=self)

    @ui.button(label="C", style=discord.ButtonStyle.red, row=1)
    async def clear(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "C")

    @ui.button(label="(", style=discord.ButtonStyle.grey, row=1)
    async def paren_left(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "(")

    @ui.button(label=")", style=discord.ButtonStyle.grey, row=1)
    async def paren_right(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, ")")

    @ui.button(label="/", style=discord.ButtonStyle.green, row=1)
    async def divide(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "/")

    @ui.button(label="7", style=discord.ButtonStyle.grey, row=2)
    async def seven(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "7")

    @ui.button(label="8", style=discord.ButtonStyle.grey, row=2)
    async def eight(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "8")

    @ui.button(label="9", style=discord.ButtonStyle.grey, row=2)
    async def nine(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "9")

    @ui.button(label="*", style=discord.ButtonStyle.green, row=2)
    async def multiply(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "*")

    @ui.button(label="4", style=discord.ButtonStyle.grey, row=3)
    async def four(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "4")

    @ui.button(label="5", style=discord.ButtonStyle.grey, row=3)
    async def five(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "5")

    @ui.button(label="6", style=discord.ButtonStyle.grey, row=3)
    async def six(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "6")

    @ui.button(label="-", style=discord.ButtonStyle.green, row=3)
    async def minus(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "-")

    @ui.button(label="1", style=discord.ButtonStyle.grey, row=4)
    async def one(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "1")

    @ui.button(label="2", style=discord.ButtonStyle.grey, row=4)
    async def two(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "2")

    @ui.button(label="3", style=discord.ButtonStyle.grey, row=4)
    async def three(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "3")

    @ui.button(label="+", style=discord.ButtonStyle.green, row=4)
    async def plus(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "+")

    @ui.button(label="0", style=discord.ButtonStyle.grey, row=5)
    async def zero(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "0")

    @ui.button(label=".", style=discord.ButtonStyle.grey, row=5)
    async def dot(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, ".")

    @ui.button(label="=", style=discord.ButtonStyle.green, row=5)
    async def equals(self, interaction: discord.Interaction, button: ui.Button):
        await self.handle_input(interaction, "=")

class CalculatorCog(commands.Cog):
    @app_commands.command(name="calculatrice", description="Ouvre une calculatrice interactive")
    async def calculator(self, interaction: discord.Interaction):
        view = CalcView(interaction.user)
        await interaction.response.send_message("`🧮 Calculatrice Benny's`", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(CalculatorCog())