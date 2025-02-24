from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api.user_management import add_user
from filters.admin import is_admin
from keyboards.default.admin import admin_menu

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer("Salom Admin!", reply_markup=admin_menu)
    else:
        await message.answer(f"Salom, {message.from_user.full_name}!\nBotimizga xush kelibsiz")
        await message.answer("Kino kodini kiriting")
        add_user(message.from_user.id, message.from_user.username,message.from_user.full_name)
