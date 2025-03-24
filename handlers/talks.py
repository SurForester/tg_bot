import os.path
from aiogram import Router, types, F
from utils.gpt_utils import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboard_utils import create_inline_keyboard
from handlers.common import keyboard_main
from utils.utils_bot import get_prompt
from lexicons.lexicon_ru import LEXICON_TALKS


talks_router = Router()
gpt_service = ChatGPTService()
talks_inline = create_inline_keyboard(1, 'Возврат в главное меню', **LEXICON_TALKS)
talks_inline_person = create_inline_keyboard(1, 'Возврат в список собеседников', None)


class TalksStates(StatesGroup):
    list = State()
    person = State()


# /random command
@talks_router.message(F.text.in_(['/talk', 'Диалог с известной личностью 👤']))
async def talks_command(message: types.Message, state: FSMContext):
    await message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'talk.jpg')))
    await state.set_state(TalksStates.list)
    await message.answer('Выберите собеседника для беседы:', reply_markup=talks_inline)


@talks_router.callback_query(F.data == 'Возврат в главное меню', TalksStates.list)
async def callback_exit_talks(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(show_alert=False)
    await callback.message.answer(f'{callback.message.chat.first_name}, вы вышли из выбора собеседника для беседы.',
                                        reply_markup=keyboard_main)


@talks_router.callback_query(F.data == 'grande', TalksStates.list)
async def callback_select_person(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'photo_grande.jpg')))
    prompt = await get_prompt('prompt_grande')
    gpt_service.set_system_message(prompt)
    await state.set_state(TalksStates.person)
    await callback.message.answer('Задавайте вопросы собеседнику.', reply_markup=talks_inline_person)


@talks_router.callback_query(F.data == 'hardy', TalksStates.list)
async def callback_select_person(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'photo_hardy.jpg')))
    prompt = await get_prompt('prompt_hardy')
    gpt_service.set_system_message(prompt)
    await state.set_state(TalksStates.person)
    await callback.message.answer('Задавайте вопросы собеседнику.', reply_markup=talks_inline_person)


@talks_router.callback_query(F.data == 'tolkien', TalksStates.list)
async def callback_select_person(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'photo_tolkien.jpg')))
    prompt = await get_prompt('prompt_tolkien')
    gpt_service.set_system_message(prompt)
    await state.set_state(TalksStates.person)
    await callback.message.answer('Задавайте вопросы собеседнику.', reply_markup=talks_inline_person)


@talks_router.callback_query(TalksStates.person)
async def callback_talk_to_list(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(TalksStates.list)
    await callback.message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'talk.jpg')))
    await callback.message.answer('Выберите собеседника для беседы:', reply_markup=talks_inline)


@talks_router.message(TalksStates.person)
async def talk_with_person(message: types.Message):
    gpt_service.add_user_message(message.text)
    response = (gpt_service.get_response())
    await message.answer(response, reply_markup=talks_inline_person)
