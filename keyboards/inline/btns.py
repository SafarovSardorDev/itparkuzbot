from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Foydalanuvchilarning tillarini saqlash uchun dictionary
user_languages = {}

# Til tanlash uchun inline buttonlar
def get_languages_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_uz = InlineKeyboardButton("Uz 🇺🇿", callback_data="lang_uz")
    button_en = InlineKeyboardButton("En 🇬🇧", callback_data="lang_en")
    keyboard.add(button_uz, button_en)
    return keyboard

# Kurslar va Ro'yxatdan o'tish uchun inline buttonlar
def get_course_register_keyboard(lang):
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    if lang == 'uz':
        button_courses = InlineKeyboardButton("📚 Kurslar", callback_data="courses_uz")
        button_register = InlineKeyboardButton("📝 Ro'yxatdan o'tish", callback_data="register_uz")
        button_contact = InlineKeyboardButton("📞 Bog'lanish", callback_data="contact_uz")
    else:  # Ingliz tili
        button_courses = InlineKeyboardButton("📚 Courses", callback_data="courses_en")
        button_register = InlineKeyboardButton("📝 Register", callback_data="register_en")
        button_contact = InlineKeyboardButton("📞 Contact us", callback_data="contact_en")
    
    keyboard.add(button_courses, button_register, button_contact)
    return keyboard

# Kurslarning o'zbek va inglizcha nomlarini ko'rsatish
def get_courses_keyboard(lang):
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    if lang == 'uz':
        button_1 = InlineKeyboardButton("Kompyuter savadxonligi", callback_data="course_uz_1")
        button_2 = InlineKeyboardButton("WEB dasturlash", callback_data="course_uz_2")
        button_3 = InlineKeyboardButton("Grafik dizayn", callback_data="course_uz_3")
        button_4 = InlineKeyboardButton("Android ilovalari", callback_data="course_uz_4")
        # back_button = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main_uz")
    else:  # Ingliz tili
        button_1 = InlineKeyboardButton("Computer literacy", callback_data="course_en_1")
        button_2 = InlineKeyboardButton("WEB development", callback_data="course_en_2")
        button_3 = InlineKeyboardButton("Graphic design", callback_data="course_en_3")
        button_4 = InlineKeyboardButton("Android applications", callback_data="course_en_4")
        # back_button = InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main_uz")

    keyboard.add(button_1, button_2, button_3, button_4)
    return keyboard
