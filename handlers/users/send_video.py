from aiogram import types
from loader import dp

from utils.db_api.video_management import get_video

@dp.message_handler(content_types=types.ContentType.TEXT)
async def send_film(message: types.Message):
    if message.text.isdigit():
        movie_code = int(message.text)

        result = get_video(movie_code)
        if result != []:
            await message.answer_video(video=result[0][0], caption=result[0][1])
        else:
            await message.answer("Ushbu kodda kino mavjud emas!")





    