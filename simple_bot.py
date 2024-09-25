from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

# Определяем стадии диалога
SELECTING_DRINK, SELECTING_QUANTITY = range(2)

# Список напитков
DRINKS_MENU = [
    ["Кофе", "Чай"],
    ["Сок", "Вода"],
    ["Cola", "Квас"],
]


# Функция для приветствия пользователя и показа меню
async def start(update: Update, context) -> int:
    user = update.message.from_user
    await update.message.reply_text(f'Привет, {user.first_name}! Добро пожаловать в наш магазин напитков!')

    reply_keyboard = ReplyKeyboardMarkup(DRINKS_MENU, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Выберите напиток из меню:', reply_markup=reply_keyboard)

    return SELECTING_DRINK


# Функция для обработки выбора напитка
async def select_drink(update: Update, context) -> int:
    context.user_data['selected_drink'] = update.message.text  # Сохраняем выбранный напиток
    await update.message.reply_text(f'Вы выбрали: {update.message.text}. Теперь укажите количество:')
    return SELECTING_QUANTITY


# Функция для обработки выбора количества
async def select_quantity(update: Update, context) -> int:
    quantity = update.message.text
    # Проверка на число
    if not quantity.isdigit():
        await update.message.reply_text('Пожалуйста, введите корректное количество.')
        return SELECTING_QUANTITY

    context.user_data['quantity'] = int(quantity)  # Сохраняем количество
    selected_drink = context.user_data['selected_drink']
    await update.message.reply_text(
        f'Вы заказали {quantity} порций {selected_drink}. Переходим к оформлению заказа!'
    )

    # Здесь можно добавить логику для оформления доставки или оплаты.
    return ConversationHandler.END


# Функция для отмены
async def cancel(update: Update, context) -> int:
    await update.message.reply_text('Ваш заказ отменён.')
    return ConversationHandler.END


# Основной блок программы
if __name__ == '__main__':
    TOKEN = "7799454159:AAGgpP-umwyBdun7QBudA2iGPKFSKNCzEd4"

    application = Application.builder().token(TOKEN).build()

    # Создаем обработчик диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_DRINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_drink)],
            SELECTING_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_quantity)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    print("Бот запущен. Нажмите Ctrl+C для завершения.")
    application.run_polling()
