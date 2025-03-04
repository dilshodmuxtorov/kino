from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton


channel_btn= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("🔎Kino kodlarini qidirish", callback_data='channel_search_code', url="https://t.me/muxtorov_IT")
        ]
    ]    
)

