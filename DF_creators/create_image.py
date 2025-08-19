import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from .formatter import format_number
from DB.database import db


async def create_image_with_text():
    users_count = await db.view_users()
    unique_users_count = format_number(users_count)
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    font_path = "DF_creators/Roboto_font.ttf"  # Путь к шрифту
    text_font_size = 150  # Размер шрифта для текста
    date_font_size = 36  # Размер шрифта для даты и времени
    test_font_size = 64  # Размер шрифта для "TEST BOT"
    text_font = ImageFont.truetype(font_path, text_font_size)
    date_font = ImageFont.truetype(font_path, date_font_size)
    test_font = ImageFont.truetype(font_path, test_font_size)
    img = Image.open("DF_creators/admin_photo.png")
    draw = ImageDraw.Draw(img)
    draw.text((306, 320), unique_users_count, fill=(110, 168, 255), font=text_font, anchor="mm")
    date_img = Image.new('RGBA', (400, 50), (255, 255, 255, 0))
    date_draw = ImageDraw.Draw(date_img)
    date_draw.text((0, 0), date, fill=(255, 255, 255), font=date_font)

    rotated_date_img = date_img.rotate(41, expand=True)

    img.paste(rotated_date_img, (645, 220), rotated_date_img)

    name_bot = "TELEGRAM BOT"

    draw.text((480, 56), name_bot, fill=(110, 168, 255), font=test_font, anchor="mm", align='center')

    output_stream = io.BytesIO()
    img.save(output_stream, format='PNG')
    output_stream.seek(0)
    return output_stream.getvalue()

