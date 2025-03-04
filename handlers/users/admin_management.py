from aiogram import types
from loader import dp
from filters.admin import is_admin
from aiogram.dispatcher import FSMContext
from states.video import VideoState, MovieCode, AddChannelState
from utils.db_api.video_management import add_video_db, delete_video , add_channel , is_channel_in_database
from utils.db_api.user_management import get_all_user
from loader import bot


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



@dp.message_handler(text = '➕Add Channel')
async def add_channel_handler(message: types.Message):
    if  is_admin(message.from_user.id):  
        await message.answer("Please send the channel ID (e.g., -1001234567890):")
        await AddChannelState.channel_id.set()  
    else:
        await message.answer("<b>❌ You don't have permission to add channels!</b>")

@dp.message_handler(state=AddChannelState.channel_id)
async def process_channel_id(message: types.Message, state: FSMContext):
    channel_id = message.text.strip()
    
    try:
        channel_id = int(channel_id) 
        try:
            chat = await bot.get_chat(channel_id)
            chat_name = chat.full_name  
        except Exception:
            await message.answer("<b>❌ Invalid channel ID! Please send a valid channel ID.</b>")
            await state.finish()
            return
        
        if is_channel_in_database(channel_id):
            await message.answer("❌ This channel is already in the database!")
        else:
            add_channel(channel_id)
            await message.answer(f"✔️ Channel '{chat_name}' (ID: {channel_id}) has been added successfully!")
        
        await state.finish()
    
    except ValueError:
        await message.answer("❌ Invalid input! Please send a valid numeric channel ID.")
        await state.finish()