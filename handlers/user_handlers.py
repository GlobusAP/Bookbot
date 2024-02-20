from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from database.database import users_db, user_dict_template
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.bookmarks_kb import create_bookmarks_kb, create_edit_kb
from lexicon.lexicon import LEXICON
from services.file_handling import book
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData

router = Router()


@router.message(CommandStart())
async def process_start_cmd(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command(commands='help'))
async def process_help_cmd(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands=['beginning', 'continue']))
async def process_beginning_cmd(message: Message):
    if message.text == '/beginning':
        users_db[message.from_user.id]['page'] = 1
    page = users_db[message.from_user.id]['page']
    text = book[page]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            page=page
        )
    )


@router.message(Command(commands='bookmarks'))
async def process_bookmarks_cmd(message: Message):
    bookmarks = users_db[message.from_user.id]['bookmarks']
    if bookmarks:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_kb(*bookmarks)
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data.in_({'forward', 'backward'}))
async def process_forward_press(callback: CallbackQuery):
    page = users_db[callback.from_user.id]['page']
    if callback.data == 'forward' and page < len(book):
        page += 1
    elif callback.data == 'backward' and page > 1:
        page -= 1
    text = book[page]
    users_db[callback.from_user.id]['page'] = page
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(page=page))


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    id_users_db = users_db[callback.from_user.id]
    id_users_db['bookmarks'].add(id_users_db['page'])
    await callback.answer('Страница добавлена в закладки!')


@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(page=int(callback.data))
    )


@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_kb(*users_db[callback.from_user.id]['bookmarks'])
    )


@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])


@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_kb(*users_db[callback.from_user.id]['bookmarks'])
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
