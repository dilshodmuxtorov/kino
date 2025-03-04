from loader import dp
from aiogram import types
from filters.admin import is_admin
from utils.db_api.user_management import get_all_user, active_users, inactive_users, blocked_users
from utils.db_api.video_management import count_video



@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def button_handler(message: types.Message):
    if is_admin(message.from_user.id):
        users = get_all_user()
        videos = count_video()
        active_user = active_users()
        inactive_user = inactive_users()
        blocked_user = blocked_users()
        text = f"""
🗒<b>Barcha foydalanuvchilar</b>: {users[0][0]}

♻️<b>Aktiv foydalanuvchilar</b>: {active_user}
⭕️<b>Aktiv bo'lmagan foydalanuvchilar</b>: {inactive_user}
<b>❌Bloklangan foydalanuvchilar</b>: {blocked_user}

📹<b>Kinolar</b> : {videos}
    """
        await message.answer(text=text)