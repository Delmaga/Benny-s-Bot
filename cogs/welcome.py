import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

BACKGROUND_PATH = "assets/welcome_bg.jpg"

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Générer l'image
        image_buffer = await self.create_welcome_image(member)
        if not image_buffer:
            # Si échec, envoie un message de secours
            channel = discord.utils.get(member.guild.text_channels, name="général")
            if channel:
                await channel.send(f"`📥 Bienvenue {member.mention} !`")
            return

        # Trouver le salon "bienvenue" ou "général"
        channel = discord.utils.get(member.guild.text_channels, name="bienvenue")
        if not channel:
            channel = discord.utils.get(member.guild.text_channels, name="général")
        if channel:
            file = discord.File(image_buffer, filename="bienvenue.png")
            await channel.send(file=file)

    async def create_welcome_image(self, member):
        # 1. Charger le fond
        if not os.path.exists(BACKGROUND_PATH):
            print("❌ Fichier assets/welcome_bg.jpg manquant")
            return None

        try:
            background = Image.open(BACKGROUND_PATH).convert("RGBA")
            if background.size != (1920, 950):
                background = background.resize((1920, 950), Image.LANCZOS)
        except Exception as e:
            print(f"❌ Erreur fond : {e}")
            return None

        # 2. Télécharger l'avatar
        avatar_url = member.display_avatar.replace(size=256).url
        try:
            response = requests.get(avatar_url)
            avatar = Image.open(BytesIO(response.content)).convert("RGBA")
        except Exception as e:
            print(f"❌ Erreur avatar : {e}")
            return None

        # 3. Redimensionner l'avatar (300x300)
        avatar = avatar.resize((300, 300), Image.LANCZOS)

        # 4. Créer un masque circulaire
        mask = Image.new("L", (300, 300), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 300, 300), fill=255)
        avatar_cropped = Image.new("RGBA", (300, 300))
        avatar_cropped.paste(avatar, (0, 0), mask)

        # 5. Coller l'avatar au centre
        x = (1920 - 300) // 2
        y = (950 - 300) // 2 - 50  # légèrement au-dessus du centre
        background.paste(avatar_cropped, (x, y), avatar_cropped)

        # 6. Ajouter le texte
        draw = ImageDraw.Draw(background)
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        except:
            try:
                font = ImageFont.truetype("arialbd.ttf", 72)
            except:
                font = ImageFont.load_default()

        text = f"Bienvenue au Benny's"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (1920 - text_width) // 2
        text_y = y + 300 + 30

        # Texte blanc avec contour noir
        draw.text((text_x - 2, text_y - 2), text, fill="black", font=font)
        draw.text((text_x + 2, text_y - 2), text, fill="black", font=font)
        draw.text((text_x - 2, text_y + 2), text, fill="black", font=font)
        draw.text((text_x + 2, text_y + 2), text, fill="black", font=font)
        draw.text((text_x, text_y), text, fill="white", font=font)

        # 7. Sauvegarder en mémoire
        buffer = BytesIO()
        background.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))