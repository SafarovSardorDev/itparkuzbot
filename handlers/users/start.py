from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot
from keyboards.inline.btns import get_languages_keyboard, get_course_register_keyboard, get_courses_keyboard,  user_languages
from states.registrstate import RegistrationState
from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import ContentType
# from keyboards.default.contactbtn import create_phone_request_keyboard, is_valid_phone 



# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     await message.answer(f"Salom, {message.from_user.full_name}! \nTilni tanlang. \nChoose language.", reply_markup=languages_keyboard)

from aiogram.types import Message

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    # Agar foydalanuvchi ilgari tilni tanlagan bo'lsa, tilni qaytarib yuborish
    if user_id in user_languages:
        lang = user_languages[user_id]
        if lang == 'uz':
            await message.answer(f"Salom {message.from_user.full_name}! Quyidagi bo'limlardan birini tanlang!", reply_markup=get_course_register_keyboard('uz'))
        else:
            await message.answer(f"Hello {message.username}! Choose one of the sections below!", reply_markup=get_course_register_keyboard('en'))
    else:
        # Foydalanuvchidan til tanlashni so'rash
        keyboard = get_languages_keyboard()
        await message.answer(f"Salom {message.from_user.full_name}! \nTilni tanlang.  \nChoose your language.", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('lang_'))
async def process_language_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = callback_query.data.split('_')[1]  # 'uz' yoki 'en' tilni olish

    # Foydalanuvchi tilini saqlash
    user_languages[user_id] = lang

    # Tilga mos xabar va keyingi tugmalar
    if lang == 'uz':
        response = "O'zbek tilini tanladingiz. Kurslar va Ro'yxatdan o'tish imkoniyatlarini tanlang."
    else:  # Ingliz tili
        response = "You have selected English. Choose between Courses and Register options."

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, response, reply_markup=get_course_register_keyboard(lang))

@dp.callback_query_handler(lambda c: c.data.startswith('courses_'))
async def process_course_or_register(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_languages.get(user_id, 'uz')  # Foydalanuvchining tilini olish

    # Kurslarni yoki ro'yxatdan o'tishni tanlash
    if callback_query.data.startswith('courses'):
        await bot.answer_callback_query(callback_query.id)

        # Kurslar tugmasi bosilganda, kurslar ro'yxatini chiqarish
        if lang == 'uz':
            await bot.send_message(callback_query.from_user.id, "Kurslarni tanlang:", reply_markup=get_courses_keyboard(lang))
        else:
            await bot.send_message(callback_query.from_user.id, "Choose course:", reply_markup=get_courses_keyboard(lang))
        # await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    elif callback_query.data.startswith('register'):
        await bot.answer_callback_query(callback_query.id)
    
    

# Ro'yxatdan o'tish tugmasi bosilganda, ro'yxatni olish
@dp.callback_query_handler(lambda c: c.data.startswith('register_'))
async def start_registration(callback_query: types.CallbackQuery):
    lang = callback_query.data.split('_')[1]  # 'uz' yoki 'en'

    # Tugmalarni o'chirish
    # await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

    # Tilga mos xabarni yuborish
    if lang == 'uz':
        msg = "Iltimos, ismingiz va familiyangizni kiriting:"
    else:
        msg = "Please enter your full name:"

    await bot.send_message(callback_query.from_user.id, msg)

    # Keyingi holatga o'tkazamiz
    await RegistrationState.name.set()

@dp.message_handler(state=RegistrationState.name)
async def process_name(message: types.Message, state: FSMContext):
    # Foydalanuvchi yuborgan ma’lumotlarni saqlaymiz
    await state.update_data(name=message.text)
    lang = user_languages.get(message.from_user.id, 'uz')  # Default 'uz'
    if lang == 'uz':
        await message.answer("Telefon raqamingizni kiriting:")
    # Telefon raqamini so‘raymiz
    else:
        await message.answer("Please enter your phone number:")
    await RegistrationState.phone.set()

# @dp.message_handler(state=RegistrationState.phone, content_types=ContentType.CONTACT)
# async def process_contact(message: types.Message, state: FSMContext):
#     # Foydalanuvchi raqamini ulashgan bo'lsa
#     await state.update_data(phone=message.contact.phone_number)
#     await message.answer("Telefon raqamingiz muvaffaqiyatli qabul qilindi!")
#     await complete_registration(message, state)

# @dp.message_handler(state=RegistrationState.phone)
# async def process_phone(message: types.Message, state: FSMContext):
#     # Foydalanuvchi qo'lda raqam kiritgan bo'lsa
#     if is_valid_phone(message.text):
#         await state.update_data(phone=message.text)
#         await message.answer("Telefon raqamingiz muvaffaqiyatli qabul qilindi!")
#         await complete_registration(message, state)
#     else:
#         await message.answer("Noto'g'ri telefon raqam. Iltimos, telefon raqamingizni +998901234567 formatida kiriting yoki 'Telefon raqamni ulashish' tugmasidan foydalaning.")



@dp.message_handler(state=RegistrationState.phone)
async def process_phone(message: types.Message, state: FSMContext):
    # Foydalanuvchi yuborgan telefon raqamini saqlaymiz
    await state.update_data(phone=message.text)

    # Saqlangan ma’lumotlarni o‘qiymiz
    user_data = await state.get_data()
    name = user_data['name']
    phone = user_data['phone']

    # Foydalanuvchini ro'yxatdan o'tkazish haqida xabar
    # Foydalanuvchi tanlagan tilni olish
    lang = user_languages.get(message.from_user.id, 'uz')  # Default 'uz'

    # Tilga qarab xabarni shakllantirish
    if lang == 'uz':
        msg = (
            f"Ro'yxatdan o'tganingiz uchun rahmat, {name}!\n"
            f"Sizning ma'lumotlaringiz:\n"
            f"F.I.O: {name}\n"
            f"Telefon raqamingiz: {phone}\n"
            f"Kurs haqida batafsil ma'lumot uchun operatorlarimiz bilan bog'laning."
        )
    else:
        msg = (
            f"Thank you for registering, {name}!\n"
            f"Your details:\n"
            f"F.I.O: {name}\n"
            f"Phone number: {phone}\n"
            f"For more information about the course, contact our operators."
        )
    # Xabarni chiqarish
    await message.answer(msg)

    # Holatni tozalash
    await state.finish()
    
#Contact us
@dp.callback_query_handler(lambda c: c.data.startswith('contact_'))
async def contact_info(callback_query: types.CallbackQuery):
    lang = callback_query.data.split('_')[1]  # 'uz' yoki 'en'

    # Tilga mos xabarni chiqarish
    if lang == 'uz':
        msg = (
            "📞 Biz bilan bog'lanish:\n\n"
            "📱 Telefon: +998 99 026-11-99\n"
            "Savollaringiz bo‘lsa, biz bilan bog‘laning!"
        )
    else:
        msg = (
            "📞 Contact Us:\n\n"
            "📱 Phone: +998 99 026-11-99\n"
            "Feel free to reach out for any inquiries!"
        )

    # Tugmani bosilgandan keyin xabarni chiqarish
    await bot.send_message(callback_query.from_user.id, msg)
    # await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)



@dp.callback_query_handler(lambda c: c.data.startswith('course_'))
async def process_course_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = user_languages.get(user_id, 'uz')  # Foydalanuvchining tilini olish

    # Kursni tanlash
    if callback_query.data == 'course_uz_1' or callback_query.data == 'course_en_1':
        if lang == 'uz':
            course_name = "KOMPYUTER SAVODXONLIGI"
            description = """
    - KOMPYUTER HAQIDA UMUMIY TUSHUNCHA;
    - OPERATSION SISTEMA HAQIDA TUSHUNCHA;
    - FAYLLAR BILAN ISHLASH;
    - MS OFFICE DASTURLARI BILAN ISHLASH;
    - INTERNETDA ISHLASH;

    ⏳ KURS DAVOMIYLIGI: 1 OY HAFTADA 3 KUN 2 SOATDAN
    💵 KURS NARXI: 300 000 SO'M
"""
        else:
            course_name = "COMPUTER LITERACY"
            description = """
    - GENERAL UNDERSTANDING OF COMPUTER;
    - UNDERSTANDING OF THE OPERATING SYSTEM;
    - WORKING WITH FILES;
    - WORKING WITH MS OFFICE PROGRAMS;
    - WORK ON THE INTERNET;

    ⏳ COURSE DURATION: 1 MONTH, 3 DAYS PER WEEK FOR 2 HOURS
    💵 COURSE PRICE: 300 000 UZS 
"""

        # course_name = "Kompyuter savadxonligi" if lang == 'uz' else "Computer literacy"
        # description = "Python dasturlashni o'rganing!" if lang == 'uz' else "Learning python"
    elif callback_query.data == 'course_uz_2' or callback_query.data == 'course_en_2':
        if lang == 'uz':
            course_name = "WEB DASTURLASH"
            description = """
    FULL STACK
    - FRONTEND (HTML, CSS, BOOTSTRAP, SASS, JAVASCRIPT)

    ⏳ KURS DAVOMIYLIGI: 6 OY HAFTADA 3 KUN 2 SOATDAN
    💵 KURS NARXI: 400 000 SO'M

    - BACKEND (PYTHON);
    - PYTHON ASOSLARI (PYTHON CORE, FUNKSIONAL DASTURLASH);
    - PARSING, DJANGO, DRF;
    - TELEGRAM BOT YARATISH;

    ⏳ KURS DAVOMIYLIGI: 8 OY HAFTADA 3 KUN 2 SOATDAN
    💵 KURS NARXI: 500 000 SO'M
"""
        else:
            course_name = "WEB DEVELOPMENT"
            description = """
    FULL STACK
    - FRONTEND (HTML, CSS, BOOTSTRAP, SASS, JAVASCRIPT)

    ⏳ COURSE DURATION: 6 MONTHS, 3 DAYS PER WEEK FOR 2 HOURS
    💵 COURSE PRICE: 400,000 SOM

    - BACKEND (PYTHON);
    - PYTHON BASICS (PYTHON CORE, FUNCTIONAL PROGRAMMING);
    - PARSING, DJANGO, DRF;
    - TELEGRAM BOT CREATION;

    ⏳ COURSE DURATION: 8 MONTHS, 3 DAYS A WEEK FOR 2 HOURS
    💵 COURSE PRICE: 500,000 UZS
"""
    elif callback_query.data == 'course_uz_3' or callback_query.data == 'course_en_3':
        if lang == 'uz':
            course_name = "GRAFIK DIZAYN"
            description = """
    2D GRAFIKA
    - ADOBE PHOTOSHOP;
    - ADOBE ILLUSTRATOR;
    - FIGMA;
    - LIGHTROOM;

    ⏳ KURS DAVOMIYLIGI: 7 OY HAFTADA 3 KUN 2 SOATDAN
    💵 KURS NARXI: 400 000 SO'M

    3D GRAFIKA
    - 3D MODEL YASASH;
    - 3D ANIMATSIAY QILISH;
    - PRODUCT ANIMATION;
    - INTERIOR, EKSTERIOR DIZAYN;

    ⏳ KURS DAVOMIYLIGI: 10 OY HAFTADA 3 KUN 2 SOATDAN
    💵 KURS NARXI: 450 000 SO'M
"""
        else:
            course_name = "GRAPHIC DESIGN"
            description = """
    2D GRAPHICS
    - ADOBE PHOTOSHOP;
    - ADOBE ILLUSTRATOR;
    - FIGMA;
    - LIGHTROOM;

    ⏳ COURSE DURATION: 7 MONTHS, 3 DAYS PER WEEK FOR 2 HOURS
    💵 COURSE PRICE: 400,000 UZS

    3D GRAPHICS
    - MAKE A 3D MODEL;
    - 3D ANIMATION;
    - PRODUCT ANIMATION;
    - INTERIOR, EXTERIOR DESIGN;

    ⏳ COURSE DURATION: 10 MONTHS, 3 DAYS PER WEEK FOR 2 HOURS
    💵 COURSE PRICE: 450,000 UZS
"""
    elif callback_query.data == 'course_uz_4' or callback_query.data == 'course_en_4':
        if lang == 'uz':
            course_name = "ANDROID ILOVALARNI DASTURLASH"
            description = """
    - ANDROID STUDIO;
    - JAVA;
    - KOTLIN;

    ⏳ KURS DAVOMIYLIGI: 9 OY HAFTADA 3 KUN 2 SOATDAN
    💵 KURS NARXI: 400 000 SO'M
"""
        else:
            course_name = "ANDROID APPLICATION PROGRAMMING"
            description = """
    - ANDROID STUDIO;
    - JAVA;
    - COTLIN;

    ⏳ COURSE DURATION: 9 MONTHS, 3 DAYS PER WEEK FOR 2 HOURS
    💵 COURSE PRICE: 400,000 UZS
"""

    # Kurs haqida ma'lumot yuborish
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, f"<b>{course_name}</b>\n{description}")



