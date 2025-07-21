import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
import asyncio

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "7355892035:AAGkwOEh1m5y3jmZlQ3ysYg6ZZ75Rbjpofo"
ADMIN_CHAT_ID = 992132564

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Данные с переводами

languages = {
    "en": "English",
    "ru": "Русский",
    "uk": "Українська",
    "es": "Español"
}

lang_buttons = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "uk": "🇺🇦 Українська",
    "es": "🇪🇸 Español"
}

cities = {
    "en": ["Barcelona", "Madrid", "Valencia", "Alicante"],
    "ru": ["Барселона", "Мадрид", "Валенсия", "Аликанте"],
    "uk": ["Барселона", "Мадрид", "Валенсія", "Аліканте"],
    "es": ["Barcelona", "Madrid", "Valencia", "Alicante"]
}

cars = {
    "en": {
        "Toyota Camry": 45,
        "Honda Accord": 45,
        "Mazda6": 50,
        "Volkswagen Passat": 50,
        "Hyundai Sonata": 35,
        "Kia K5": 50,
        "Ford Fusion": 40,
        "Subaru Legacy": 35,
        "Nissan Altima": 30,
        "Skoda Superb": 50,
    },
    "ru": {
        "Тойота Камри": 45,
        "Хонда Аккорд": 45,
        "Мазда6": 50,
        "Фольксваген Пассат": 50,
        "Хёндай Соната": 35,
        "Киа К5": 50,
        "Форд Фьюжн": 40,
        "Субару Легаси": 35,
        "Ниссан Альтима": 30,
        "Шкода Суперб": 50,
    },
    "uk": {
        "Тойота Камрі": 45,
        "Хонда Аккорд": 45,
        "Мазда6": 50,
        "Фольксваген Пассат": 50,
        "Хюндай Соната": 35,
        "Кіа К5": 50,
        "Форд Ф'южн": 40,
        "Субару Легасі": 35,
        "Ніссан Альтіма": 30,
        "Шкода Суперб": 50,
    },
    "es": {
        "Toyota Camry": 45,
        "Honda Accord": 45,
        "Mazda6": 50,
        "Volkswagen Passat": 50,
        "Hyundai Sonata": 35,
        "Kia K5": 50,
        "Ford Fusion": 40,
        "Subaru Legacy": 35,
        "Nissan Altima": 30,
        "Skoda Superb": 50,
    }
}

texts = {
    "en": {
        "choose_language": "Choose language / Выберите язык / Оберіть мову / Seleccione un idioma",
        "welcome": 'Welcome to "SpainHire"!',
        "choose_city": "Please choose a city:",
        "choose_car": "Select a car:",
        "enter_dates": "Enter rental dates (from - to):",
        "enter_name": "Enter your full name:",
        "enter_phone": "Enter your phone number:",
        "enter_email": "Enter your email:",
        "enter_telegram": "Enter your Telegram (e.g., @username):",
        "confirm": "✅ Your request has been sent! We will contact you soon.",
        "per_day": "per day"
    },
    "ru": {
        "choose_language": "Choose language / Выберите язык / Оберіть мову / Seleccione un idioma",
        "welcome": 'Добро пожаловать в "SpainHire"!',
        "choose_city": "Выберите город:",
        "choose_car": "Выберите машину:",
        "enter_dates": "Введите даты аренды (с - по):",
        "enter_name": "Введите ваше ФИО:",
        "enter_phone": "Введите ваш номер телефона:",
        "enter_email": "Введите ваш Email:",
        "enter_telegram": "Введите ваш Telegram (например, @username):",
        "confirm": "✅ Ваша заявка отправлена! Мы скоро свяжемся с вами.",
        "per_day": "в день"
    },
    "uk": {
        "choose_language": "Choose language / Выберите язык / Оберіть мову / Seleccione un idioma",
        "welcome": 'Ласкаво просимо до "SpainHire"!',
        "choose_city": "Оберіть місто:",
        "choose_car": "Оберіть машину:",
        "enter_dates": "Введіть дати оренди (з - по):",
        "enter_name": "Введіть ваше ПІБ:",
        "enter_phone": "Введіть ваш номер телефону:",
        "enter_email": "Введіть вашу електронну пошту:",
        "enter_telegram": "Введіть ваш Telegram (наприклад, @username):",
        "confirm": "✅ Ваша заявка надіслана! Ми скоро зв'яжемося з вами.",
        "per_day": "в день"
    },
    "es": {
        "choose_language": "Choose language / Выберите язык / Оберіть мову / Seleccione un idioma",
        "welcome": '¡Bienvenido a "SpainHire"!',
        "choose_city": "Seleccione una ciudad:",
        "choose_car": "Seleccione un coche:",
        "enter_dates": "Ingrese las fechas de alquiler (desde - hasta):",
        "enter_name": "Ingrese su nombre completo:",
        "enter_phone": "Ingrese su número de teléfono:",
        "enter_email": "Ingrese su correo electrónico:",
        "enter_telegram": "Ingrese su Telegram (por ejemplo, @username):",
        "confirm": "✅ ¡Su solicitud ha sido enviada! Nos pondremos en contacto pronto.",
        "per_day": "por día"
    }
}

class Booking(StatesGroup):
    language = State()
    city = State()
    car = State()
    dates = State()
    name = State()
    phone = State()
    email = State()
    telegram = State()


@dp.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    keyboard = InlineKeyboardBuilder()
    for code, text_btn in lang_buttons.items():
        keyboard.row(InlineKeyboardButton(text=text_btn, callback_data=f"lang_{code}"))
    await state.clear()

    photo_url = "https://s.zagranitsa.com/images/articles/1993/870x486/087603febfa3da7d27458d9039f66989.jpg"

    await message.answer_photo(photo=photo_url, caption=texts["en"]["choose_language"], reply_markup=keyboard.as_markup())
    await state.set_state(Booking.language)


@dp.callback_query(lambda c: c.data and c.data.startswith("lang_"))
async def choose_language(call: CallbackQuery, state: FSMContext):
    lang_code = call.data[5:]
    if lang_code not in languages:
        await call.answer("Unsupported language")
        return

    await state.update_data(language=lang_code)
    await call.message.delete()

    await call.message.answer(texts[lang_code]["welcome"])

    keyboard = InlineKeyboardBuilder()
    for city in cities[lang_code]:
        keyboard.row(InlineKeyboardButton(text=city, callback_data=f"city_{city}"))

    await call.message.answer(texts[lang_code]["choose_city"], reply_markup=keyboard.as_markup())
    await state.set_state(Booking.city)
    await call.answer()


@dp.callback_query(lambda c: c.data and c.data.startswith("city_"))
async def choose_city(call: CallbackQuery, state: FSMContext):
    city = call.data[5:]
    data = await state.get_data()
    lang = data.get("language", "en")

    if city not in cities[lang]:
        await call.answer("Invalid city")
        return

    await state.update_data(city=city)

    keyboard = InlineKeyboardBuilder()
    for car_name, price in cars[lang].items():
        keyboard.row(InlineKeyboardButton(text=f"{car_name} - {price} € {texts[lang]['per_day']}", callback_data=f"car_{car_name}"))

    await call.message.delete()
    await call.message.answer(texts[lang]["choose_car"], reply_markup=keyboard.as_markup())
    await state.set_state(Booking.car)
    await call.answer()


@dp.callback_query(lambda c: c.data and c.data.startswith("car_"))
async def choose_car(call: CallbackQuery, state: FSMContext):
    car = call.data[4:]
    data = await state.get_data()
    lang = data.get("language", "en")
    city = data.get("city")

    if city is None or car not in cars[lang]:
        await call.answer("Invalid car")
        return

    await state.update_data(car=car)

    await call.message.delete()
    await call.message.answer(texts[lang]["enter_dates"])
    await state.set_state(Booking.dates)
    await call.answer()


@dp.message(StateFilter(Booking.dates))
async def enter_dates(message: Message, state: FSMContext):
    dates = message.text.strip()
    if "-" not in dates:
        await message.answer("Please enter dates in format: from - to")
        return

    await state.update_data(dates=dates)
    data = await state.get_data()
    lang = data.get("language", "en")

    await message.answer(texts[lang]["enter_name"])
    await state.set_state(Booking.name)


@dp.message(StateFilter(Booking.name))
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    data = await state.get_data()
    lang = data.get("language", "en")

    await message.answer(texts[lang]["enter_phone"])
    await state.set_state(Booking.phone)


@dp.message(StateFilter(Booking.phone))
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    data = await state.get_data()
    lang = data.get("language", "en")

    await message.answer(texts[lang]["enter_email"])
    await state.set_state(Booking.email)


@dp.message(StateFilter(Booking.email))
async def enter_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    data = await state.get_data()
    lang = data.get("language", "en")

    await message.answer(texts[lang]["enter_telegram"])
    await state.set_state(Booking.telegram)


@dp.message(StateFilter(Booking.telegram))
async def enter_telegram(message: Message, state: FSMContext):
    await state.update_data(telegram=message.text.strip())
    data = await state.get_data()
    lang = data.get("language", "en")

    # Формируем сообщение для админа
    text = (
        f"<b>New booking request:</b>\n\n"
        f"<b>Language:</b> {languages.get(lang, 'Unknown')}\n"
        f"<b>City:</b> {data.get('city')}\n"
        f"<b>Car:</b> {data.get('car')}\n"
        f"<b>Dates:</b> {data.get('dates')}\n"
        f"<b>Name:</b> {data.get('name')}\n"
        f"<b>Phone:</b> {data.get('phone')}\n"
        f"<b>Email:</b> {data.get('email')}\n"
        f"<b>Telegram:</b> {data.get('telegram')}\n"
    )

    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, parse_mode="HTML")

    await message.answer(texts[lang]["confirm"])
    await state.clear()


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
