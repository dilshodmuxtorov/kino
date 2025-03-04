from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕Add Video"), KeyboardButton("🗑Delete Video")],
        [KeyboardButton(text="📊 Statistika"),KeyboardButton("➕Add Channel")]
    ],
    resize_keyboard=True
)
