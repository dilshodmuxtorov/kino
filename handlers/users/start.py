from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp , bot
from utils.db_api.user_management import add_user
from utils.db_api.video_management import get_video
from filters.admin import is_admin
from keyboards.default.admin import admin_menu
from keyboards.inline.channel_inline import channel_btn

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer(f"<b>Salom Admin {message.from_user.full_name}</b>", reply_markup=admin_menu)
    else:
        add_user(message.from_user.id, message.from_user.username,message.from_user.full_name)
        args = message.get_args()
        if args.isdigit():
            kb = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(
                        "🫂 Do'stlar bilan ulashish", 
                        switch_inline_query=f"🎬 Ushbu kinoni tomosha qiling! 👇\nhttps://t.me/b22044_bot?start={args}"
                    )]
                ]
            )
            result = get_video(int(args))
            if result != []:
                await message.answer_video(video=result[0][0], caption=result[0][1],reply_markup=kb)
            else:
                await message.answer("<b>Ushbu kodda kino mavjud emas!</b>")
        else:
            text =f"""<b>👋Assalomu aleykum {message.from_user.full_name}
botimizga xush kelibsiz.</b>

<i>✍🏻Kino kodini yuboring.</i>
    """ 
            await message.answer(text, reply_markup=channel_btn)


@dp.callback_query_handler(lambda c: c.data == "check_subscribe")
async def check_subscribe_channel(call: types.CallbackQuery):
    text =f"""<b>👋Assalomu aleykum {call.from_user.full_name}
botimizga xush kelibsiz.</b>

<i>✍🏻Kino kodini yuboring.</i>
    """ 
    await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=channel_btn)
