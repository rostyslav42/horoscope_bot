import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TELEGRAM_BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

# In-memory user language storage (for demo; use DB in production)
user_languages = {}

LANGUAGE_TEXTS = {
    "en": {
        "greeting": "Hello, {name}!",
        "choose_language": "Please choose your language:",
        "english": "English",
        "ukrainian": "Українська",
        "language_set": "Language set to English.",
        "signs": [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ],
    },
    "uk": {
        "greeting": "Вітаю, {name}!",
        "choose_language": "Будь ласка, оберіть мову:",
        "english": "Англійська",
        "ukrainian": "Українська",
        "language_set": "Мову змінено на українську.",
        "signs": [
            "Овен",
            "Телець",
            "Близнюки",
            "Рак",
            "Лев",
            "Діва",
            "Терези",
            "Скорпіон",
            "Стрілець",
            "Козоріг",
            "Водолій",
            "Риби",
        ],
    },
}

# In-memory user zodiac storage (for demo; use DB in production)
user_zodiacs = {}


class Form(StatesGroup):
    choosing_language = State()
    choosing_zodiac = State()


# Keyboards:
def get_language_keyboard(texts):
    # texts = LANGUAGE_TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts["english"])],
            [KeyboardButton(text=texts["ukrainian"])],
        ],
        resize_keyboard=True,
    )


def get_zodiac_keyboard(texts):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=sign)] for sign in texts],
        resize_keyboard=True,
    )


def get_user_language(user_data):
    print(user_data)
    return user_data.get("language_code", "en")


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    # user_id = message.from_user.id
    lang = get_user_language(message.from_user.model_dump())
    texts = LANGUAGE_TEXTS[lang]
    await message.answer(texts["greeting"].format(name=html.bold(message.from_user.full_name)))
    await state.set_state(Form.choosing_language)
    # await language_handler(message)


# @dp.message(Command("language"))
@dp.message(Form.choosing_language)
async def language_handler(message: Message):
    lang = get_user_language(message.from_user.model_dump())
    texts = LANGUAGE_TEXTS[lang]
    keyboard = get_language_keyboard(texts)
    await message.answer(texts["choose_language"], reply_markup=keyboard)


@dp.message()
async def set_language_handler(message: Message):
    print("language")
    user_id = message.from_user.id
    text = message.text
    # Check if user is choosing a language
    if text in (LANGUAGE_TEXTS["en"]["english"], LANGUAGE_TEXTS["uk"]["english"]):
        user_languages[user_id] = "en"
        await message.answer(LANGUAGE_TEXTS["en"]["language_set"])
        await zodiac_handler(message)
        return
    elif text in (LANGUAGE_TEXTS["en"]["ukrainian"], LANGUAGE_TEXTS["uk"]["ukrainian"]):
        user_languages[user_id] = "uk"
        await message.answer(LANGUAGE_TEXTS["uk"]["language_set"])
        await zodiac_handler(message)
        return
    # Fallback to echo
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


@dp.message(Command("zodiac"))
async def zodiac_handler(message: Message):
    # Show zodiac options as keyboard
    lang = get_user_language(message.from_user.model_dump())
    texts = LANGUAGE_TEXTS[lang]["signs"]
    keyboard = get_zodiac_keyboard(texts)
    await message.answer("Please choose your zodiac sign:", reply_markup=keyboard)


# @dp.message()
# async def set_zodiac_handler(message: Message):
#     print("zodiac")
#     user_id = message.from_user.id
#     text = message.text
#     if text in ZODIAC_SIGNS:
#         user_zodiacs[user_id] = text
#         await message.answer(f"Your zodiac sign is set to {text}.")
#         return
#     # Fallback to echo
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
