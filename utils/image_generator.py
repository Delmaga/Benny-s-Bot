# utils/image_generator.py
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import os

# Chemin vers ton fond d'écran (1920x950)
BACKGROUND_PATH = "assets/benny_welcome_bg.jpg"

def ensure_background():
    if not os.path.exists(BACKGROUND_PATH):
        print(f"[WARN] Fond d'écran manquant : {BACKGROUND_PATH}")
        return None
    return Image.open(BACKGROUND_PATH).convert("RGBA")

async def generate_welcome_image(member_avatar_url: str, member_name: str) -> BytesIO:
    """
    Génère une image de bienvenue avec :
    - Fond 1920x950
    - Avatar centré (cercle)
    - Texte "Bienvenue au Benny's" en gros
    """
    background = ensure_background()
    if not background:
        return None

    # Télécharger l'avatar
    try:
        response = requests.get(member_avatar_url, stream=True)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA")
    except Exception as e:
        print(f"[ERROR] Impossible de télécharger l'avatar : {e}")
        return None

    # Redimensionner l'avatar (ex: 300x300)
    avatar_size = 300
    avatar = avatar.resize((avatar_size, avatar_size), Image.LANCZOS)

    # Créer un masque circulaire
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    avatar = Image.composite(avatar, Image.new("RGBA", avatar.size, (0,0,0,0)), mask)

    # Position centrale (x, y)
    x = (background.width - avatar_size) // 2
    y = (background.height - avatar_size) // 2 - 80  # Légèrement au-dessus du centre

    # Coller l'avatar sur le fond
    background.paste(avatar, (x, y), avatar)

    # Ajouter le texte
    draw = ImageDraw.Draw(background)
    try:
        # Essaie d'utiliser une police plus grande (Arial Bold)
        font = ImageFont.truetype("arialbd.ttf", 60)  # Arial Bold
    except:
        # Sinon, utilise la police par défaut
        font = ImageFont.load_default()

    text = f"Bienvenue au Benny's"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (background.width - text_width) // 2
    text_y = y + avatar_size + 40

    # Dessiner le texte avec contour noir pour le rendre visible
    draw.text(
        (text_x, text_y),
        text,
        fill="white",
        font=font,
        stroke_width=3,
        stroke_fill="black"
    )

    # Sauvegarder en mémoire
    img_byte_arr = BytesIO()
    background.save(img_byte_arr, format='PNG')  # Toujours PNG pour Discord
    img_byte_arr.seek(0)
    return img_byte_arr