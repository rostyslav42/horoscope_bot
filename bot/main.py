import asyncio
from os import getenv

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TELEGRAM_BOT_TOKEN")
AUTHORIZATION_TOKEN = getenv("AUTHORIZATION_TOKEN")

ZODIAC_MAP = {
    "Овен": 1,
    "Aries": 1,
    "Телець": 2,
    "Taurus": 2,
    "Близнюки": 3,
    "Gemini": 3,
    "Рак": 4,
    "Cancer": 4,
    "Лев": 5,
    "Leo": 5,
    "Діва": 6,
    "Virgo": 6,
    "Терези": 7,
    "Libra": 7,
    "Скорпіон": 8,
    "Scorpio": 8,
    "Стрілець": 9,
    "Sagittarius": 9,
    "Козоріг": 10,
    "Capricorn": 10,
    "Водолій": 11,
    "Aquarius": 11,
    "Риби": 12,
    "Pisces": 12,
}


class Form(StatesGroup):
    choosing_language = State()
    choosing_zodiac = State()


language_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Українська")], [KeyboardButton(text="English")]],
    resize_keyboard=True,
)

zodiac_kb_ua = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Овен"), KeyboardButton(text="Телець")],
        [KeyboardButton(text="Близнюки"), KeyboardButton(text="Рак")],
        [KeyboardButton(text="Лев"), KeyboardButton(text="Діва")],
        [KeyboardButton(text="Терези"), KeyboardButton(text="Скорпіон")],
        [KeyboardButton(text="Стрілець"), KeyboardButton(text="Козоріг")],
        [KeyboardButton(text="Водолій"), KeyboardButton(text="Риби")],
    ],
    resize_keyboard=True,
)

zodiac_kb_en = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Aries"), KeyboardButton(text="Taurus")],
        [KeyboardButton(text="Gemini"), KeyboardButton(text="Cancer")],
        [KeyboardButton(text="Leo"), KeyboardButton(text="Virgo")],
        [KeyboardButton(text="Libra"), KeyboardButton(text="Scorpio")],
        [KeyboardButton(text="Sagittarius"), KeyboardButton(text="Capricorn")],
        [KeyboardButton(text="Aquarius"), KeyboardButton(text="Pisces")],
    ],
    resize_keyboard=True,
)


async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message, state: FSMContext):
        await message.answer("Привіт! Обери, будь ласка, мову / Hi! Please choose your language:", reply_markup=language_kb)
        await state.set_state(Form.choosing_language)

    @dp.message(Form.choosing_language)
    async def process_language(message: Message, state: FSMContext):
        language = message.text
        await state.update_data(language=language)

        if language == "English":
            await message.answer("Great! Now choose your zodiac sign:", reply_markup=zodiac_kb_en)
        else:
            await message.answer("Дякую! Тепер обери свій знак зодіаку:", reply_markup=zodiac_kb_ua)

        await state.set_state(Form.choosing_zodiac)

    @dp.message(Form.choosing_zodiac)
    async def process_zodiac(message: Message, state: FSMContext):
        zodiac = message.text
        zodiac_id = ZODIAC_MAP.get(zodiac)

        await state.update_data(
            zodiac=zodiac,
            zodiac_sign=zodiac_id,
            telegram_id=message.from_user.id,
            telegram_username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        print(message.from_user.model_dump)
        data = await state.get_data()
        language = data.get("language", "Українська")

        async with aiohttp.ClientSession() as session:
            # payload = {
            #     "user_id": message.from_user.id,
            #     "language": language,
            #     "zodiac_id": zodiac_id,
            # }
            headers = {
                "Authorization": f"Bearer {AUTHORIZATION_TOKEN}",
            }
            try:
                async with session.post("http://127.0.0.1:8000/api/user/", headers=headers, json=data) as resp:
                    if resp.status in [200, 201]:
                        print("Success")
                    else:
                        print(resp)
                        print(dir(resp))
                        print(resp.json())
                        print(f"Failed: {resp.status}")
            except Exception as e:
                print(f"Error: {e}")

        if language == "English":
            text = (
                f"You chose language: {language}\n"
                f"And your zodiac sign: {zodiac}\n"
                "Now you will receive fresh forecasts every day!"
            )
        else:
            text = (
                f"Ти обрав мову: {language}\n"
                f"Та знак зодіаку: {zodiac}\n"
                "Тепер ти будеш отримувати свіжі прогнози кожного дня!"
            )
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        print(data)
        await state.clear()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
