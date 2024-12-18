import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

API_TOKEN = 'API'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

# Основное меню
@bot.message_handler(commands=['start'])
def start_menu(message):
    print("Команда /start получена")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    calculate_button = telebot.types.KeyboardButton('Рассчитать')
    info_button = telebot.types.KeyboardButton('Информация')
    markup.add(calculate_button, info_button)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

# Функция для отображения Inline-клавиатуры
@bot.message_handler(func=lambda message: message.text == 'Рассчитать')
def main_menu(message):
    print("Пользователь выбрал 'Рассчитать'")
    markup = InlineKeyboardMarkup()
    calories_button = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
    formulas_button = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
    markup.add(calories_button, formulas_button)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

# Функция для обработки нажатия на кнопку 'Формулы расчёта'
@bot.callback_query_handler(func=lambda call: call.data == 'formulas')
def get_formulas(call: CallbackQuery):
    print("Пользователь выбрал 'Формулы расчёта'")
    formula_message = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) + 5\n"
        "Для женщин: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) - 161"
    )
    bot.send_message(call.message.chat.id, formula_message)
    bot.answer_callback_query(call.id)  # Обязательно отвечаем на callback

# Функция для обработки нажатия на кнопку 'Рассчитать норму калорий'
@bot.callback_query_handler(func=lambda call: call.data == 'calories')
def set_age(call: CallbackQuery):
    print("Пользователь выбрал 'Рассчитать норму калорий'")
    bot.send_message(call.message.chat.id, "Пожалуйста, введите ваш возраст:")
    bot.answer_callback_query(call.id)  # Обязательно отвечаем на callback

# Обработка текстового сообщения с возрастом
@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_age(message):
    age = int(message.text)
    print(f"Пользователь ввел возраст: {age}")
    bot.send_message(message.chat.id, f"Ваш возраст: {age}. Теперь введите ваш вес:")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен")
    bot.polling(none_stop=True)
