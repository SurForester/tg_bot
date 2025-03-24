from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_keyboard(width: int, *args, **kwargs: str):
    menu: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []
    if args:
        for button in args:
            buttons.append(KeyboardButton(text=button))
    if kwargs:
        for key, value in kwargs.items():
            buttons.append(KeyboardButton(text=value, callback_data=key))
    menu.row(*buttons, width=width)
    return menu.as_markup(resize_keyboard=True)


def create_inline_keyboard(width: int, button_under: str | None = None, *args, **kwargs: str):
    inline_menu: InlineKeyboardBuilder = InlineKeyboardBuilder()
    inline_buttons: list[InlineKeyboardButton] = []
    if args:
        for button in args:
            if button:
                inline_buttons.append(InlineKeyboardButton(text=button, callback_data=button))
    if kwargs:
        for key, value in kwargs.items():
            if value:
                inline_buttons.append(InlineKeyboardButton(text=value, callback_data=key))
    # menu.add(*buttons, width=width)
    if len(inline_buttons) > 0:
        inline_menu.row(*inline_buttons, width=width)
    if button_under:
        add_button = InlineKeyboardButton(text=button_under, callback_data=button_under)
        inline_menu.row(add_button)
    return inline_menu.as_markup(resize_keyboard=True)
