from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup

from keyboards.keyboard_prof import make_rows_keyboard
from handlers.common import keyboard_main

router = Router()

available_jobs = [
    'Повар',
    'Строитель',
    'Водитель',
    'Сварщик'
]

available_grades = [
    'Junior',
    'Middle',
    'Senior'
]


class CareerChoice(StatesGroup):
    job = State()
    grade = State()


@router.message(Command('prof'))
async def command_prof(message: types.Message, state: FSMContext):
    await message.answer('Выберите профессию: ', reply_markup=make_rows_keyboard(available_jobs))
    await state.set_state(CareerChoice.job)


@router.message(CareerChoice.job, F.text.in_(available_jobs))
async def command_job(message: types.Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await message.answer('Выберите уровень: ', reply_markup=make_rows_keyboard(available_grades))
    await state.set_state(CareerChoice.grade)


@router.message(CareerChoice.job)
async def command_job_correct(message: types.Message):
    await message.answer('Выберите профессию: ', reply_markup=make_rows_keyboard(available_jobs))


@router.message(CareerChoice.grade, F.text.in_(available_grades))
async def command_grade(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()
    await message.answer(f'Вы выбрали: профессия {user_data['profession']}, уровень {user_data['grade']}',
                         reply_markup=keyboard_main)


@router.message(CareerChoice.grade, F.text.in_(available_grades))
async def command_job_correct(message: types.Message):
    await message.answer('Выберите уровень: ', reply_markup=make_rows_keyboard(available_grades))