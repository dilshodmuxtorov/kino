from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton


confirm_btn= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("✅ Ha", callback_data='confirm_yes'),InlineKeyboardButton("❌ Yo'q", callback_data='confirm_no')
        ]
    ]    
)