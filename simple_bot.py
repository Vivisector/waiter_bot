from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from telegram.ext import ContextTypes

# Определяем стадии диалога
SELECTING_DRINK, SELECTING_QUANTITY, ENTERING_ADDRESS, ENTERING_PHONE, CONFIRMATION = range(5)

# Список напитков
DRINKS_MENU = [
    ["Кофе", "Чай"],
    ["Сок", "Вода"],
    ["Cola", "Квас", "Vodka"],
]


# Функция для приветствия пользователя и показа меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(f'Привет, {user.first_name}! Добро пожаловать в наш магазин напитков!')

    reply_keyboard = ReplyKeyboardMarkup(DRINKS_MENU, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Выберите напиток из меню:', reply_markup=reply_keyboard)

    return SELECTING_DRINK


# Функция для обработки выбора напитка
async def select_drink(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['selected_drink'] = update.message.text  # Сохраняем выбранный напиток
    await update.message.reply_text(f'Вы выбрали: {update.message.text}. Теперь укажите количество:')
    return SELECTING_QUANTITY


# Функция для обработки выбора количества
async def select_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    quantity = update.message.text
    if not quantity.isdigit():
        await update.message.reply_text('Пожалуйста, введите корректное количество.')
        return SELECTING_QUANTITY

    context.user_data['quantity'] = int(quantity)  # Сохраняем количество
    selected_drink = context.user_data['selected_drink']

    # Запрашиваем адрес доставки
    await update.message.reply_text('Введите адрес доставки:')
    return ENTERING_ADDRESS


# Функция для ввода адреса
async def enter_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['address'] = update.message.text  # Сохраняем адрес
    await update.message.reply_text('Введите ваш номер телефона:')
    return ENTERING_PHONE


# Функция для ввода номера телефона
async def enter_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['phone'] = update.message.text  # Сохраняем телефон
    selected_drink = context.user_data['selected_drink']
    quantity = context.user_data['quantity']
    address = context.user_data['address']

    # Подтверждаем заказ
    await update.message.reply_text(
        f'Вы заказали {quantity} порций {selected_drink}.\n'
        f'Адрес доставки: {address}\n'
        f'Номер телефона: {context.user_data["phone"]}\n'
        'Подтверждаете заказ? Напишите "да" для подтверждения или "нет" для отмены.'
    )
    return CONFIRMATION


# Функция для подтверждения заказа
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == 'да':
        await update.message.reply_text('Ваш заказ принят! Спасибо за покупку!')
    else:
        await update.message.reply_text('Ваш заказ отменён.')

    # Очищаем данные пользователя
    context.user_data.clear()
    return ConversationHandler.END


# Функция для отмены
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Ваш заказ отменён.')
    context.user_data.clear()  # Очищаем данные пользователя
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
            ENTERING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_address)],
            ENTERING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_phone)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    print("Бот запущен. Нажмите Ctrl+C для завершения.")
    application.run_polling()
