from aiogram import types
from filters.admin import is_admin
from loader import dp
from states.video import MessageState
from aiogram.dispatcher import FSMContext
from keyboards.inline.confirm import confirm_btn
from loader import bot
from utils.db_api.user_management import get_all_userid, set_inactive
from aiogram.utils.exceptions import BotBlocked


@dp.message_handler(lambda message: message.text == "📤Foydalanuvchilarga xabar yuborish")
async def button_handler(message: types.Message):
    if  is_admin(message.from_user.id):
        await MessageState.message.set()
        await message.answer("Xabaringini yuboring:")

# @dp.message_handler(state=MessageState.message)
# async def process_message(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['message_to_send'] = message.text  
#     await MessageState.confirm.set()
#     await message.answer(f'{bold("You want to send the following message to all users:")}\n\n"{italic(message.text)}"', reply_markup=confirm_btn)
 
# @dp.callback_query_handler(lambda c: c.data in ['confirm_yes', 'confirm_no'], state=MessageState.confirm)
# async def process_callback_confirm(callback_query: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         message_to_send = data['message_to_send']

#     if callback_query.data == 'confirm_yes':
#         users = get_all_user()  
#         count = 1
#         for user_id in users:           
#             if count%1001 == 0:
#                 await bot.send_message(callback_query.from_user.id, italic(f" Message have been sent to {count} users."))            
#             try:
#                 await bot.send_message(chat_id=user_id[0], text=message_to_send)
#                 count = count+1
#             except BotBlocked:
#                 set_inactive(user_id=int(user_id[0]))

#         await bot.send_message(callback_query.from_user.id, bold(f"✅ Message sent to all {count-1} users."))
#     else:
#         await bot.send_message(callback_query.from_user.id, bold("❌Message not sent."))
    
#     await bot.answer_callback_query(callback_query.id)
#     await state.finish()

@dp.message_handler(content_types=types.ContentTypes.ANY, state=MessageState.message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_type'] = message.content_type  
        if message.text:
            data['message_content'] = message.text
        elif message.photo:
            data['message_content'] = message.photo[-1].file_id  
            data['caption'] = message.caption
        elif message.video:
            data['message_content'] = message.video.file_id
            data['caption'] = message.caption
        elif message.voice:
            data['message_content'] = message.voice.file_id
        elif message.animation:
            data['message_content'] = message.animation.file_id
            data['caption'] = message.caption
        elif message.audio:
            data['message_content'] = message.audio.file_id
            data['caption'] = message.caption
        elif message.document:
            data['message_content'] = message.document.file_id
            data['caption'] = message.caption
        else:
            await message.answer("❌ Xatolik boshqa file yuborilgan")
            return

    await MessageState.confirm.set()

    if message.text:
        await message.answer(message.text)
    elif message.photo:
        await message.answer_photo(photo=message.photo[-1].file_id, caption=message.caption)
    elif message.video:
        await message.answer_video(video=message.video.file_id, caption=message.caption)
    elif message.voice:
        await message.answer_voice(voice=message.voice.file_id)
    elif message.animation:
        await message.answer_animation(animation=message.animation.file_id, caption=message.caption)
    elif message.audio:
        await message.answer_audio(audio=message.audio.file_id, caption=message.caption)
    elif message.document:
        await message.answer_document(document=message.document.file_id, caption=message.caption)
    
    await message.answer(f"<b>Yuqoridagi xabarni foydalanuvchilarga yuborishni tasdiqlaysizmi:</b>", reply_markup=confirm_btn)
    

@dp.callback_query_handler(lambda c: c.data in ['confirm_yes', 'confirm_no'], state=MessageState.confirm)
async def process_callback_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.from_user.id, text="✅Xabar yuborish boshlandi")
    async with state.proxy() as data:
        message_type = data['message_type']
        message_content = data['message_content']
        caption = data.get('caption', None)  

    if callback_query.data == 'confirm_yes':
        users = get_all_userid()

        for user_id in users:
            try:
                if message_type == "text":
                    await bot.send_message(chat_id=user_id[0], text=message_content)
                elif message_type == "photo":
                    await bot.send_photo(chat_id=user_id[0], photo=message_content, caption=caption)
                elif message_type == "video":
                    await bot.send_video(chat_id=user_id[0], video=message_content, caption=caption)
                elif message_type == "voice":
                    await bot.send_voice(chat_id=user_id[0], voice=message_content)
                elif message_type == "animation":
                    await bot.send_animation(chat_id=user_id[0], animation=message_content, caption=caption)
                elif message_type == "audio":
                    await bot.send_audio(chat_id=user_id[0], audio=message_content, caption=caption)
                elif message_type == "document":
                    await bot.send_document(chat_id=user_id[0], document=message_content, caption=caption)

            except:
                set_inactive(user_id=int(user_id[0]))
        
        await bot.send_message(chat_id=callback_query.from_user.id, text="✅Xabar yuborish yakunlandi")
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text="❌Rad etildi")
    await state.finish()

