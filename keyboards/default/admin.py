from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📤Foydalanuvchilarga xabar yuborish"),KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="➕Kino qo'shish"), KeyboardButton("🗑Kino o'chirish")],
        [KeyboardButton("➕Kanal qo'shish"),KeyboardButton("🗑Kanal o'chirish")],
        [KeyboardButton("🧹Botni tozalash")]
    ],
    resize_keyboard=True
)
