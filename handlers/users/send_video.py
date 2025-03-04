from aiogram import types
from loader import dp

from utils.db_api.video_management import get_video

@dp.message_handler(lambda message: str(message.text).isdigit() and len(str(message.text).split()) == 1)
async def send_film(message: types.Message):
    movie_code = int(message.text)

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                "🫂 Do'stlar bilan ulashish", 
                switch_inline_query=f"🎬 Ushbu kinoni tomosha qiling! 👇\nhttps://t.me/b22044_bot?start={movie_code}"
            )]
        ]
    )
    result = get_video(movie_code)
    if result != []:
        await message.answer_video(video=result[0][0], caption=result[0][1],reply_markup=kb)
    else:
        await message.answer("<b>❌Ushbu kodda kino mavjud emas!</b>")





    