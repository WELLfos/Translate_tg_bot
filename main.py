import os
from aiogram import Bot, Dispatcher, types, executor
from translate import Translator
from gtts import gTTS

bot = Bot(token='6557991781:AAEeuxBYUH4Lo8YWjJqIJ3FlafLxCDStIOk')

dp = Dispatcher(bot)

# Словарь, сопоставляющий пары языковых, кодов с их соответствующим текстовым представлением
languages = {
    'ru-en': {'from_lang': 'ru', 'to_lang': 'en', 'text': '🇷🇺 на 🇬🇧'},
    'en-ru': {'from_lang': 'en', 'to_lang': 'ru', 'text': '🇬🇧 на 🇷🇺'},
    'ru-it': {'from_lang': 'ru', 'to_lang': 'it', 'text': '🇷🇺 на 🇨🇮'},
    'it-ru': {'from_lang': 'it', 'to_lang': 'ru', 'text': '🇨🇮 на 🇷🇺'},
    'ru-fr': {'from_lang': 'ru', 'to_lang': 'fr', 'text': '🇷🇺 на 🇫🇷'},
    'fr-ru': {'from_lang': 'fr', 'to_lang': 'ru', 'text': '🇫🇷 на 🇷🇺'},
}

translator = Translator(from_lang=languages['ru-en']['from_lang'], to_lang=languages['ru-en']['to_lang'])

# Обработчики команд и сообщений
@dp.message_handler(commands=['start', 'menu'])
async def start(message: types.Message):
    # Клава с выбором языков
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for key in languages:
        buttons.append(types.InlineKeyboardButton(text=languages[key]['text'], callback_data=key))
    keyboard.add(*buttons)
    await message.answer("Выберите на какой язык переводить:", reply_markup=keyboard)

@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    global translator
    # Настройте переводчик на выбранный язык.
    translator = Translator(from_lang=languages[callback_query.data]['from_lang'],
                             to_lang=languages[callback_query.data]['to_lang'])
    # Отправить пользователю сообщение с выбранным языком
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           f"Выберите на какой язык переводить: {languages[callback_query.data]['text']}")

@dp.message_handler()
async def translate_message(message: types.Message):
    global translator
    # Перевод входящего сообщения
    translated_text = translator.translate(message.text)
    await message.answer(translated_text)
    # Преобразование текста в гс
    tts = gTTS(text=translated_text, lang=translator.to_lang)
    tts.save("translated_message.mp3")
    # Отправка гс пользователю
    with open("translated_message.mp3", "rb") as voice:
        await bot.send_voice(chat_id=message.chat.id, voice=voice)

if __name__ == '__main__':
    executor.start_polling(dp)