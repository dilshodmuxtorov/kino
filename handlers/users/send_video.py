from aiogram import types
from loader import dp

from utils.db_api.video_management import get_video

dp.message_handler(content_types=types.ContentType.TEXT)
async def send_film(message: types.Message):
    print("kirdi")
    if message.text.isdigit():
        movie_code = int(message.text)

        result = get_video(movie_code)

        print(result)




    