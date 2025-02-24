from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import re

def create_phone_request_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("📞 Telefon raqamni ulashish", request_contact=True))
    return keyboard


def is_valid_phone(phone):
    pattern = r"^\+998\d{9}$"  # +998 bilan boshlanib, 9 ta raqam bo'lishi kerak
    return bool(re.match(pattern, phone))
