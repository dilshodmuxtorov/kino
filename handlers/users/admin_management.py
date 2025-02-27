from aiogram import types
from loader import dp
from filters.admin import is_admin
from aiogram.dispatcher import FSMContext
from states.video import VideoState, MovieCode
from utils.db_api.video_management import add_video_db, delete_video
from utils.db_api.user_management import get_all_user


@dp.message_handler(text = "➕Add Video")
async def add_video(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer("Kinoni fileni yuboring")
        await VideoState.video.set()

@dp.message_handler(state=VideoState.video,content_types=types.ContentType.VIDEO)
async def get_video_id(message: types.Message, state: FSMContext):

    if not message.video:
        await message.answer("Iltimos, video jo'nating!")
        return
    
    await state.update_data(video = message.video.file_id)
    await message.answer("Video opisaniyasini yuboring:")
    await VideoState.caption.set()

@dp.message_handler(state=VideoState.caption)
async def get_caption(message: types.Message, state: FSMContext):
    await state.update_data(caption = message.text)
    video_data = await state.get_data()

    file_id = video_data['video']
    caption = video_data['caption']

    try:
        add_video_db(file_id, caption)
        await message.answer("Kino databazaga qo'shildi")
    except:
        await message.answer("Xatolik yuz berdi")

    await state.finish()

@dp.message_handler(text = "🗑Delete Video")
async def delete_videos(message: types.Message):
    await message.answer("Kino kodini kiriting:")
    await MovieCode.code.set()

@dp.message_handler(state=MovieCode.code)
async def del_video(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        code = int(message.text)
        if delete_video(code):       
            await message.answer("Kino o'chirildi")
            await state.finish()
        else:
            await message.answer("Kino mavjud emas!")
        
    else:
        await message.answer("Kino kodini to'g'ri kiriting:")
    
@dp.message_handler(text = "📊 Statistika")
async def statistics(message: types.Message):
    
    text = f"""Botingi haqida ma'lumot:

Foydalanuvchilar: {get_all_user()[0][0]}
Kinolar: 
"""
    await message.answer(text=text)


