# cogs/calculatrice.py
import discord
from discord.ext import commands
import ast
import operator

# Opérations sécurisées
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(expr: str):
    if not expr.strip():
        return None
    try:
        node = ast.parse(expr, mode='eval')
        return _eval_node(node.body)
    except:
        return None

def _eval_node(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if left is None or right is None:
            return None
        return OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        if operand is None:
            return None
        return OPERATORS[type(node.op)](operand)
    else:
        return None

class CalculatriceView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)  # 5 min d'inactivité
        self.expression = ""
        self.update_display()

    def update_display(self):
        """Met à jour le message en fonction de l'expression."""
        display_text = self.expression if self.expression else "0"
        self.message_content = f"`🧮 {display_text}`"

    async def update_message(self, interaction=None):
        """Met à jour le message du bot."""
        if interaction:
            await interaction.response.edit_message(content=self.message_content, view=self)
        else:
            await self.message.edit(content=self.message_content, view=self)

    @discord.ui.button(label="C", style=discord.ButtonStyle.red, row=0)
    async def clear(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression = ""
        await self.update_message(interaction)

    @discord.ui.button(label="CE", style=discord.ButtonStyle.gray, row=0)
    async def clear_entry(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.expression:
            self.expression = self.expression[:-1]
        await self.update_message(interaction)

    @discord.ui.button(label="←", style=discord.ButtonStyle.gray, row=0)
    async def backspace(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.expression:
            self.expression = self.expression[:-1]
        await self.update_message(interaction)

    @discord.ui.button(label="÷", style=discord.ButtonStyle.blurple, row=0)
    async def divide(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.expression and self.expression[-1] not in "+-*/":
            self.expression += "/"
        await self.update_message(interaction)

    @discord.ui.button(label="7", style=discord.ButtonStyle.secondary, row=1)
    async def seven(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "7"
        await self.update_message(interaction)

    @discord.ui.button(label="8", style=discord.ButtonStyle.secondary, row=1)
    async def eight(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "8"
        await self.update_message(interaction)

    @discord.ui.button(label="9", style=discord.ButtonStyle.secondary, row=1)
    async def nine(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "9"
        await self.update_message(interaction)

    @discord.ui.button(label="×", style=discord.ButtonStyle.blurple, row=1)
    async def multiply(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.expression and self.expression[-1] not in "+-*/":
            self.expression += "*"
        await self.update_message(interaction)

    @discord.ui.button(label="4", style=discord.ButtonStyle.secondary, row=2)
    async def four(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "4"
        await self.update_message(interaction)

    @discord.ui.button(label="5", style=discord.ButtonStyle.secondary, row=2)
    async def five(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "5"
        await self.update_message(interaction)

    @discord.ui.button(label="6", style=discord.ButtonStyle.secondary, row=2)
    async def six(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "6"
        await self.update_message(interaction)

    @discord.ui.button(label="-", style=discord.ButtonStyle.blurple, row=2)
    async def subtract(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.expression and self.expression[-1] not in "+-*/":
            self.expression += "-"
        await self.update_message(interaction)

    @discord.ui.button(label="1", style=discord.ButtonStyle.secondary, row=3)
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "1"
        await self.update_message(interaction)

    @discord.ui.button(label="2", style=discord.ButtonStyle.secondary, row=3)
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "2"
        await self.update_message(interaction)

    @discord.ui.button(label="3", style=discord.ButtonStyle.secondary, row=3)
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "3"
        await self.update_message(interaction)

    @discord.ui.button(label="+", style=discord.ButtonStyle.blurple, row=3)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.expression and self.expression[-1] not in "+-*/":
            self.expression += "+"
        await self.update_message(interaction)

    @discord.ui.button(label="±", style=discord.ButtonStyle.gray, row=4)
    async def negate(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.expression and self.expression[0] != "-":
            self.expression = "-" + self.expression
        elif self.expression and self.expression[0] == "-":
            self.expression = self.expression[1:]
        await self.update_message(interaction)

    @discord.ui.button(label="0", style=discord.ButtonStyle.secondary, row=4)
    async def zero(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expression += "0"
        await self.update_message(interaction)

    @discord.ui.button(label=".", style=discord.ButtonStyle.gray, row=4)
    async def decimal(self, interaction: discord.Interaction, button: discord.ui.Button):
        if "." not in self.expression.split()[-1]:
            self.expression += "."
        await self.update_message(interaction)

    @discord.ui.button(label="=", style=discord.ButtonStyle.green, row=4)
    async def equals(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = safe_eval(self.expression)
        if result is None:
            await interaction.response.send_message("`❌ Expression invalide.`", ephemeral=True)
            return
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        self.expression = str(result)
        await self.update_message(interaction)

class CalculatriceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="calculatrice", description="Ouvrir une calculatrice interactive")
    async def calculatrice(self, interaction: discord.Interaction):
        view = CalculatriceView()
        message = await interaction.channel.send("`🧮 0`", view=view)
        view.message = message
        await interaction.response.send_message("`✅ Calculatrice ouverte.`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CalculatriceCog(bot))