import os.path
from aiogram import Router, types, F
from utils.gpt_utils import ChatGPTService
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboard_utils import create_inline_keyboard
from handlers.common import keyboard_main
from utils.utils_bot import get_prompt
from lexicons.lexicon_ru import LEXICON_QUIZ, LEXICON_NEXT_QUIZ


quiz_router = Router()
gpt_service = ChatGPTService()
quiz_inline = create_inline_keyboard(1, 'Возврат в главное меню', **LEXICON_QUIZ)
quiz_inline_theme = create_inline_keyboard(1, 'Возврат в список тем', **LEXICON_NEXT_QUIZ)
user_dict: dict[int, dict[str, str | int | bool]] = {}


class QuizStates(StatesGroup):
    list = State()
    theme = State()


# /quiz command
@quiz_router.message(F.text.in_(['/quiz', 'Квиз ❓']))
async def quiz_command(message: types.Message, state: FSMContext):
    await message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'quiz.jpg')))
    await state.set_state(QuizStates.list)
    prompt = await get_prompt('quiz')
    gpt_service.set_system_message(prompt)
    await message.answer('Выберите тему для викторины:', reply_markup=quiz_inline)


@quiz_router.callback_query(F.data == 'Возврат в главное меню', QuizStates.list)
async def callback_exit_quiz(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(show_alert=False)
    await callback.message.answer(f'{callback.message.chat.first_name}, вы вышли из викторины.',
                                        reply_markup=keyboard_main)


@quiz_router.callback_query(F.data == 'quiz_biology', QuizStates.list)
async def quiz_biology(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(QuizStates.theme)
    await state.update_data(theme='quiz_biology')
    await state.update_data(counter=0)
    await state.update_data(counter_true=0)
    await callback.answer(show_alert=False)
    gpt_service.add_user_message('quiz_biology')
    response = (gpt_service.get_response())
    await callback.message.answer(response, reply_markup=quiz_inline_theme)


@quiz_router.callback_query(F.data == 'quiz_prog', QuizStates.list)
async def quiz_prog(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(QuizStates.theme)
    await state.update_data(theme='quiz_prog')
    await state.update_data(counter=0)
    await state.update_data(counter_true=0)
    await callback.answer(show_alert=False)
    gpt_service.add_user_message('quiz_prog')
    response = (gpt_service.get_response())
    await callback.message.answer(response, reply_markup=quiz_inline_theme)


@quiz_router.callback_query(F.data == 'quiz_math', QuizStates.list)
async def quiz_math(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(QuizStates.theme)
    await state.update_data(theme='quiz_math')
    await state.update_data(counter=0)
    await state.update_data(counter_true=0)
    await callback.answer(show_alert=False)
    gpt_service.add_user_message('quiz_math')
    response = (gpt_service.get_response())
    await callback.message.answer(response, reply_markup=quiz_inline_theme)


@quiz_router.callback_query(F.data == 'next_quiz', QuizStates.theme)
async def quiz_next_quiz(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(show_alert=False)
    user_dict[callback.message.from_user.id] = await state.get_data()
    user_message = user_dict[callback.message.from_user.id]['theme']
    gpt_service.add_user_message(user_message)
    response = (gpt_service.get_response())
    await callback.message.answer(response, reply_markup=quiz_inline_theme)


@quiz_router.message(QuizStates.theme)
async def quiz_message(message: types.Message, state: FSMContext):
    gpt_service.add_user_message(message.text)
    response = (gpt_service.get_response())
    user_dict[message.from_user.id] = await state.get_data()
    await state.update_data(counter=user_dict[message.from_user.id]['counter'] + 1)
    if response == 'Правильно!':
        await state.update_data(counter_true=user_dict[message.from_user.id]['counter_true'] + 1)
    await message.answer(response, reply_markup=quiz_inline_theme)


@quiz_router.callback_query(QuizStates.theme)
async def quiz_theme_exit(callback: types.CallbackQuery, state: FSMContext):
    user_dict[callback.message.from_user.id] = await state.get_data()
    await callback.message.answer(f'{callback.message.chat.first_name}, вы ответили правильно на '
                                f'{user_dict[callback.message.from_user.id]['counter_true']} вопросов '
                                f'из {user_dict[callback.message.from_user.id]['counter']}')
    await callback.message.answer_photo(photo=types.FSInputFile(os.path.join('resources', 'images', 'quiz.jpg')))
    await state.set_state(QuizStates.list)
    prompt = await get_prompt('quiz')
    gpt_service.set_system_message(prompt)
    await callback.message.answer('Выберите тему для викторины:', reply_markup=quiz_inline)