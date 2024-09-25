from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler

# Список напитков
DRINKS_MENU = [
    ["Кофе", "Чай"],
    ["Сок", "Вода"],
    ["Cola", "Квас"],
]


# Функция для приветствия пользователя и показа меню
async def start(update: Update, context) -> None:
    user = update.message.from_user  # Получаем информацию о пользователе
    # Приветствие
    await update.message.reply_text(f'Привет, {user.first_name}! Добро пожаловать в наш магазин напитков!')

    # Создаем клавиатуру с напитками
    reply_keyboard = ReplyKeyboardMarkup(DRINKS_MENU, one_time_keyboard=True, resize_keyboard=True)

    # Отправляем меню с напитками
    await update.message.reply_text(
        'Выберите напиток из меню:',
        reply_markup=reply_keyboard
    )


# Основной блок программы
if __name__ == '__main__':
    # Вставляем сюда ваш токен от BotFather
    TOKEN = "7799454159:AAGgpP-umwyBdun7QBudA2iGPKFSKNCzEd4"

    # Создаем объект Application для управления ботом
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    print("Бот запущен. Нажмите Ctrl+C для завершения.")
    application.run_polling()
