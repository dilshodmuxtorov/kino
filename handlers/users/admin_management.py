from aiogram import types
from loader import dp
from filters.admin import is_admin
from aiogram.dispatcher import FSMContext
from states.video import VideoState, MovieCode, AddChannelState
from utils.db_api.video_management import add_video_db, delete_video , add_channel , is_channel_in_database, get_video
from utils.db_api.user_management import toggle_is_blocked
from loader import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.channel_management import get_channels_from_database, delete_channel_from_database , clear_videos_and_channels
from keyboards.inline.confirm import confirm_btn

@dp.message_handler(text="➕Kino qo'shish")
async def add_video(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer("Kinoni fileni yuboring")
        await VideoState.video.set()

@dp.message_handler(state=VideoState.video, content_types=types.ContentType.VIDEO)
async def get_video_id(message: types.Message, state: FSMContext):
    if not message.video:
        await message.answer("Iltimos, video jo'nating!")
        return
    
    await state.update_data(video=message.video.file_id)
    await message.answer("Video opisaniyasini yuboring:")
    await VideoState.caption.set()

@dp.message_handler(state=VideoState.caption)
async def get_caption(message: types.Message, state: FSMContext):
    await state.update_data(caption=message.text)
    video_data = await state.get_data()

    file_id = video_data['video']
    caption = video_data['caption']

    keyboard = InlineKeyboardMarkup()
    approve_button = InlineKeyboardButton("✅ Tasdiqlash", callback_data="approve_video")
    reject_button = InlineKeyboardButton("❌ Rad etish", callback_data="reject_video")
    keyboard.add(approve_button, reject_button)

    await message.answer("<b> Ushbu kinoni qo'shishni tasdiqlaysizmi?</b>")
    await bot.send_video(chat_id=message.from_user.id, video=file_id, caption=caption, reply_markup=keyboard)

    await VideoState.confirmation.set()

@dp.callback_query_handler(lambda c: c.data in ["approve_video", "reject_video"], state=VideoState.confirmation)
async def confirm_video(callback_query: types.CallbackQuery, state: FSMContext):
    video_data = await state.get_data()
    file_id = video_data['video']
    caption = video_data['caption']

    if callback_query.data == "approve_video":
        try:
            add_video_db(file_id, caption)
            await bot.send_message(callback_query.from_user.id, "✅ Kino databazaga qo'shildi")
        except:
            await bot.send_message(callback_query.from_user.id, "❌ Xatolik yuz berdi")
    
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Kino rad etildi")

    await state.finish()
    await callback_query.answer()

@dp.message_handler(text="🗑Kino o'chirish")
async def delete_videos(message: types.Message):
    """Ask for the movie code"""
    await message.answer("Kino kodini kiriting:")
    await MovieCode.code.set()

@dp.message_handler(state=MovieCode.code)
async def del_video(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        code = int(message.text)
        result = get_video(code)  
        
        if result:  
            video_id, caption = result[0]  
            
            async with state.proxy() as data:
                data["code"] = code  
            
            kb = InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton("✅ Ha, o'chirish", callback_data="delete_yes"),
                InlineKeyboardButton("❌ Yo'q, bekor qilish", callback_data="delete_no")
            )

            await message.answer_video(video=video_id, caption=caption)
            await MovieCode.confirm.set()
            await message.answer(f"Kod {code} bo'lgan kinoni o'chirmoqchimisiz?", reply_markup=kb)
        else:
            await message.answer("❌ Kino mavjud emas! Qaytadan urinib ko'ring.")
    else:
        await message.answer("⛔ Kino kodini to'g'ri kiriting!")


@dp.callback_query_handler(lambda c: c.data in ["delete_yes", "delete_no"], state=MovieCode.confirm)
async def confirm_delete(callback_query: types.CallbackQuery, state: FSMContext):
    """Handle movie deletion confirmation"""
    async with state.proxy() as data:
        code = data["code"]

    if callback_query.data == "delete_yes":
        if delete_video(code): 
            await bot.send_message(callback_query.from_user.id, "✅ Kino muvaffaqiyatli o'chirildi.")
        else:
            await bot.send_message(callback_query.from_user.id, "⚠️ Xatolik yuz berdi! Kino o‘chira olmadi.")
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Kino o‘chirish bekor qilindi.")

    await bot.answer_callback_query(callback_query.id)
    await state.finish()
    

@dp.message_handler(text = "➕Kanal qo'shish")
async def add_channel_handler(message: types.Message):
    if  is_admin(message.from_user.id):  
        await message.answer("Kanal ID sini yuboring (e.g., -1001234567890):\n\nKanal idsini @myidbot dan olishingiz mumkin")
        await AddChannelState.channel_id.set()  
    else:
        await message.answer("<b>❌ Sizda imkoniyatingiz mavjud emas</b>")

@dp.message_handler(state=AddChannelState.channel_id)
async def process_channel_id(message: types.Message, state: FSMContext):
    channel_id = message.text.strip()
    
    try:
        channel_id = int(channel_id) 
        try:
            chat = await bot.get_chat(channel_id)
            chat_name = chat.full_name  
        except Exception:
            await message.answer("<b>❌ Bot berilgan kanalda admin emas! </b>")
            await state.finish()
            return
        
        if is_channel_in_database(channel_id):
            await message.answer("❌ Bu kanal allaqachon botga qo'shilgan!")
        else:
            add_channel(channel_id)
            await message.answer(f" Kanal: '{chat_name}'\nID: {channel_id}\n\n✔️Muvaffaqiyatli qo'shildi!")
        
        await state.finish()
    
    except ValueError:
        await message.answer("❌ Kanal chat idsini to'g'ri yuboring")
        await state.finish()


async def generate_channel_keyboard(channels):
    kb = InlineKeyboardMarkup()
    for channel_id in channels:
        try:
            chat = await bot.get_chat(channel_id)
            channel_name = chat.full_name  
        except Exception:
            channel_name = f"Unknown (ID: {channel_id})"  
        
        kb.add(InlineKeyboardButton(text=channel_name, callback_data=f"delete_channel:{channel_id}"))
    return kb

@dp.message_handler(text = "🗑Kanal o'chirish")
async def delete_channel_handler(message: types.Message):
    if is_admin(message.from_user.id):  
        channels = get_channels_from_database()
        if not channels:
            await message.answer("</b>❌ Kanallar topilmadi</b>")
            return
        
        kb = await generate_channel_keyboard(channels)
        await message.answer("<b>O'chirmoqchi bo'lgan kanalingizni tanlang</b>", reply_markup=kb)
    else:
        await message.answer("❌ You don't have permission to delete channels!")

@dp.callback_query_handler(lambda c: c.data.startswith("delete_channel:"))
async def process_delete_channel(callback_query: types.CallbackQuery):
    channel_id = int(callback_query.data.split(":")[1])  

    try:
        delete_channel_from_database(channel_id)
        await bot.send_message(
            callback_query.from_user.id,
            f"<b>✔️ Channel (ID: {channel_id}) has been deleted successfully!</b>"
        )
    except Exception as e:
        print(f"Xatolik: {e}")
        await bot.send_message(
            callback_query.from_user.id,
            "❌ Failed to delete the channel. Please try again."
        )
    
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(commands=["toggle_block"])
async def toggle_block_handler(message: types.Message):
    if is_admin(message.from_user.id): 
        try:
            args = message.text.split()
            if len(args) != 2:
                await message.answer("❌ Foydalanuvchi ID sini yuboring. Masalan: /toggle_block 123456")
                return
            
            user_id = int(args[1])  
            new_status = toggle_is_blocked(user_id) 
            
            status_text = "blocked" if new_status else "unblocked"
            await message.answer(f"✔️ User (ID: {user_id}) has been {status_text}.")
        except ValueError as e:
            await message.answer(f"❌ Error: {e}")
        except Exception as e:
            print(f"Error toggling block status: {e}")
            await message.answer("❌ Failed to toggle block status. Please try again.")
    else:
        await message.answer("❌ You don't have permission to perform this action.")

@dp.message_handler(lambda message: message.text == "🧹Botni tozalash")
async def clear_bot_prompt(message: types.Message):
    if is_admin(message.from_user.id):  
        await message.answer(
            "<b>Botdagi barcha kino va kanallarni o'chirishni xohlaysizmi?</b>",
            reply_markup=confirm_btn
        )
    else:
        await message.answer("❌ You don't have permission to clear the bot!")

@dp.callback_query_handler(lambda c: c.data in ["confirm_yes", "confirm_no"])
async def clear_bot_confirm(callback_query: types.CallbackQuery):
    if callback_query.data == "confirm_yes":
        try:
            clear_videos_and_channels()
            await bot.send_message(
                callback_query.from_user.id,
                "✔️ Barcha kanal va kinolar o'chirildi!"
            )
        except Exception as e:
            print(f"Error clearing bot data: {e}")
            await bot.send_message(
                callback_query.from_user.id,
                "❌ Xatolik. Qaytadan urinib ko'ring"
            )
    else:
        await bot.send_message(
            callback_query.from_user.id,
            "❌ Rad etildi. Hech qanday ma'lumot o'chirilmadi"
        )

    await bot.answer_callback_query(callback_query.id)