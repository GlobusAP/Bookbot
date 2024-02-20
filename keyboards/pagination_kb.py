from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON
from services.file_handling import book


def create_pagination_keyboard(page: int) -> InlineKeyboardMarkup:
    buttons = ['backward', f'{page}/{len(book)}', 'forward']
    buttons = buttons[1:] if page == 1 else buttons[:-1] if len(book) == page else buttons
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[InlineKeyboardButton(
            text=LEXICON.get(button, button), callback_data=button) for button in buttons]
    )
    return kb_builder.as_markup()
