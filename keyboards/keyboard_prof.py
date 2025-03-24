from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_rows_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    rows = [KeyboardButton(text=button) for button in buttons]
    return ReplyKeyboardMarkup(keyboard=[rows], resize_keyboard=True)