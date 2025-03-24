import os.path
from aiogram import Router, types, F
from utils.gpt_utils import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboard_utils import create_inline_keyboard
from handlers.common import keyboard_main
from utils.utils_bot import get_prompt
from lexicons.lexicon_ru import LEXICON_FACTS


random_router = Router()
gpt_service = ChatGPTService()
random_inline = create_inline_keyboard(1, 'Возврат в главное меню', **LEXICON_FACTS)


class RandomFactsStates(StatesGroup):
    next = State()


# /random command
@random_router.message(F.text.in_(['/random', 'Рандомный факт 🧠']))
async def gpt_command(message: types.Message, state: FSMContext):
    await message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'random.jpg')))
    prompt = await get_prompt('random')
    gpt_service.set_system_message(prompt)
    await state.set_state(RandomFactsStates.next)
    gpt_service.add_user_message(message.text)
    response = (gpt_service.get_response())
    await message.answer(response, reply_markup=random_inline)


@random_router.callback_query(F.data == 'next_fact', RandomFactsStates.next)
async def callback_next_fact(callback: types.CallbackQuery):
    await callback.answer(show_alert=False)
    gpt_service.add_user_message(callback.message.text)
    response = (gpt_service.get_response())
    await callback.message.answer(response, reply_markup=random_inline)


@random_router.callback_query(RandomFactsStates.next)
async def callback_exit_facts(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(show_alert=False)
    await callback.message.answer(f'{callback.message.chat.first_name}, вы вышли из режима генерации интересных фактов.',
                                        reply_markup=keyboard_main)