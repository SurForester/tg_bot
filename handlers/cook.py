import os.path
from aiogram import Router, types, F
from utils.gpt_utils import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboard_utils import create_inline_keyboard
from handlers.common import keyboard_main
from utils.utils_bot import get_prompt
from lexicons.lexicon_ru import LEXICON_NEXT_COOK


cook_router = Router()
gpt_service = ChatGPTService()
cook_inline = create_inline_keyboard(1, 'Возврат в главное меню', None)


class CoockStates(StatesGroup):
    next = State()


# /random command
@cook_router.message(F.text.in_(['/cook', 'Рецепт 🍅']))
async def gpt_command(message: types.Message, state: FSMContext):
    await message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'cook.jpg')))
    prompt = await get_prompt('cook')
    gpt_service.set_system_message(prompt)
    await state.set_state(CoockStates.next)
    await message.answer('Введите компоненты рецепта:', reply_markup=cook_inline)


@cook_router.message(CoockStates.next)
async def callback_next_cook(message: types.Message):
    gpt_service.add_user_message(message.text)
    response = (gpt_service.get_response())
    await message.answer(response, reply_markup=cook_inline)


@cook_router.callback_query(CoockStates.next)
async def callback_exit_facts(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(show_alert=False)
    await callback.message.answer(f'{callback.message.chat.first_name}, вы вышли из режима генерации рецептов.',
                                        reply_markup=keyboard_main)