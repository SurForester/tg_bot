import os.path
from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.keyboard_utils import create_keyboard
from lexicons.lexicon_ru import LEXICON_MAIN_MENU


common_router = Router()
keyboard_main = create_keyboard(3, **LEXICON_MAIN_MENU)


# /start
@common_router.message(CommandStart())
async def start_command(message: Message):
    await message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'start.jpg')))
    await message.answer(f'Выберите действие: {message.chat.first_name}!', reply_markup=keyboard_main)


@common_router.message()
async def message_handler(message: Message):
    await message.answer(f'{message.chat.first_name}, ваше сообщение: ' + message.text)