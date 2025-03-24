from aiogram import Router, types, F
from aiogram.dispatcher import router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.filters.command import Command

from keyboards.keyboard_utils import create_keyboard, create_inline_keyboard
from lexicons.lexicon_ru import LEXICON_MAIN_MENU, LEXICON_INLINE_MENU
from utils.fsm_bot import FSMFillForm, FSMContext, user_dict
from utils.utils_bot import get_photo

@router.message(F.text=='Заполнить анкету')
async def blank_start(message: Message, state: FSMContext):
    await message.answer('Давайте заполним анкету')
    await message.answer('Введите Ваше имя')
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def blank_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Спасибо, введите возраст')
    await state.set_state(FSMFillForm.fill_age)


@router.message(StateFilter(FSMFillForm.fill_name))
async def blank_name(message: Message, state: FSMContext):
    await message.answer('Некорректное имя, введите имя буквами')
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_age))
async def blank_name(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Спасибо, введите Email')
    await state.set_state(FSMFillForm.fill_email)


@router.message(StateFilter(FSMFillForm.fill_email))
async def blank_name(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer('Спасибо, анкета заполнена')
    if message.from_user.id in user_dict:
        await message.answer(f'Имя: {user_dict[message.from_user.id]['name']}\n'
                             f'Возраст: {user_dict[message.from_user.id]['age']}\n'
                             f'Email: {user_dict[message.from_user.id]['email']}\n'
                             )
