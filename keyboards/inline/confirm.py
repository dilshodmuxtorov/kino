from aiogram.types import InlineKeyboardButton , InlineKeyboardMarkup


confirm_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Yes", callback_data="confirm_yes"), InlineKeyboardButton(text="No",callback_data="confirm_no")]
    ]
)