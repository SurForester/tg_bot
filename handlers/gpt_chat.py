import os.path
from aiogram import Router, types, F
from aiogram.filters.command import Command
from utils.gpt_utils import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.keyboard_utils import create_inline_keyboard
from handlers.common import keyboard_main
from utils.utils_bot import get_prompt


gpt_router = Router()
gpt_inline = create_inline_keyboard(1, 'Выход из общения с ИИ', None)
gpt_service = ChatGPTService()


class GptState(StatesGroup):
    gpt = State()


# /gpt command
@gpt_router.message(F.text.in_(['/gpt', 'ChatGPT интерфейс 🤖']))
async def gpt_command(message: types.Message, state: FSMContext):
    await message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'gpt.jpg')))
    prompt = await get_prompt('gpt')
    gpt_service.set_system_message(prompt)
    await state.set_state(GptState.gpt)
    await message.answer(f'Привет {message.chat.first_name}! Введите свой запрос для ChatGPT', reply_markup=gpt_inline)


@gpt_router.message(GptState.gpt)
async def gpt_message_handler(message: types.Message):
    gpt_service.add_user_message(message.text)
    response = (gpt_service.get_response())
    await message.answer(response, reply_markup=gpt_inline)


@gpt_router.callback_query(GptState.gpt)
async def gpt_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer(show_alert=False)
    await callback_query.message.answer(f'{callback_query.message.chat.first_name}, вы вышли из диалога общения с ИИ.',
                                        reply_markup=keyboard_main)