from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕Add Video"), KeyboardButton("🗑Delete Video")],
        [KeyboardButton(text="📊 Statistika")]
    ],
    resize_keyboard=True
)
