from re import I
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



inline_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
inline_kb.add(InlineKeyboardButton(text='BackUp SQL', callback_data='backup_sql'))
