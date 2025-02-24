from aiogram import types
from loader import dp
from filters.admin import is_admin
from aiogram.dispatcher import FSMContext
from states.video import VideoState
from utils.db_api.video_management import add_video_db


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



