from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_1 = KeyboardButton(text='Contact', request_contact=True)
kb_2 = KeyboardButton(text='Geo', request_location=True)
kb_3 = KeyboardButton(text='Hometown')
kb_4 = KeyboardButton(text='answer')
kb_5 = KeyboardButton(text='description')
kb_6 = KeyboardButton(text='laptop')

rkm_1 = ReplyKeyboardMarkup(keyboard=[[kb_1, kb_2]], resize_keyboard=True, one_time_keyboard=False)
rkm_2 = ReplyKeyboardMarkup(keyboard=[[kb_3, kb_4, kb_5, kb_6]], resize_keyboard=True, one_time_keyboard=False)

