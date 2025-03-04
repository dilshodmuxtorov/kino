from aiogram.dispatcher.filters.state import State, StatesGroup


class VideoState(StatesGroup):
    video = State()
    caption = State()


class MovieCode(StatesGroup):
    code = State()   

class AddChannelState(StatesGroup):
    channel_id = State()