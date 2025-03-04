from aiogram.dispatcher.filters.state import State, StatesGroup


class VideoState(StatesGroup):
    video = State()
    caption = State()
    confirmation = State()


class MovieCode(StatesGroup):
    code = State()  
    confirm = State() 

class AddChannelState(StatesGroup):
    channel_id = State()

class MessageState(StatesGroup):
    message = State()
    confirm = State()