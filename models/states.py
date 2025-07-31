from aiogram.fsm.state import State, StatesGroup


class LanguageStates(StatesGroup):
    selecting_language = State()


class EditStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_topic = State()
    processing = State()
    waiting_for_manual_edit = State()


class PublishStates(StatesGroup):
    waiting_for_channel = State()
    confirming_publish = State()
    publishing = State()


class PostForm(StatesGroup):
    preview = State()
    manual_input = State()
    confirmation = State()
