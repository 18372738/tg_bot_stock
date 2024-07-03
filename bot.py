import os
import sys
import telegram
import django
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from django.db.models import Q

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock.settings')
django.setup()

from stock_models.models import Client, Order, Box


def start(update: Update, context: CallbackContext) -> None:
    telegram_id = update.effective_user.id
    if Client.objects.filter(telegram_id=telegram_id).first():
        update_main_menu(update.message)
    else:
        show_main_menu(update.message)


def show_main_menu(message) -> None:
    keyboard = [
        [InlineKeyboardButton('Условия хранения', callback_data='conditions')],
        [InlineKeyboardButton('Запрещено хранить', callback_data='prohibited')],
        [InlineKeyboardButton('Сдать вещи', callback_data='handing_things')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text('Привет! Я бот SelfStorage. Я помогу тебе оставить заявку на хранение вещей. Рекомендую ознакомиться с условиями хранения и что хранить запрещено.', reply_markup=reply_markup)


def update_main_menu(message) -> None:
    keyboard = [
        [InlineKeyboardButton('Оставшийся срок хранения', callback_data='remaining_term')],
        [InlineKeyboardButton('Забрать вещи', callback_data='get_things')],
        [InlineKeyboardButton('Сдать вещи', callback_data='handing_things')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text('Добро пожаловать в SelfStorage', reply_markup=reply_markup)


def main_menu_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'conditions':
        show_storage_conditions(query)
    elif query.data == 'prohibited':
        show_storage_prohibited(query)
    elif query.data == 'handing_things':
        show_handing_thing(query)
    elif query.data == 'remaining_term':
        show_remaining_term(query)
    elif query.data == 'get_things':
        show_get_things(query)


def show_storage_conditions(query) -> None:
    with open("documents/Условия хранения.pdf", "rb") as file:
        query.message.reply_document(document=file, filename="Условия хранения.pdf")
    keyboard = [
        [InlineKeyboardButton("Запрещено хранить", callback_data='update_prohibited')],
        [InlineKeyboardButton("Сдать вещи", callback_data='handing_things')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выбирете пункт:',reply_markup=reply_markup)


def show_storage_prohibited(query) -> None:
    with open("documents/Запрет на хранение.pdf", "rb") as file:
        query.message.reply_document(document=file, filename="Запрет на хранение.pdf")
    keyboard = [
        [InlineKeyboardButton('Условия хранения', callback_data='update_conditions')],
        [InlineKeyboardButton("Сдать вещи", callback_data='handing_things')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выбирете пункт:',reply_markup=reply_markup)


def show_handing_thing(query) -> None:
    keyboard = [
        [InlineKeyboardButton("Бесплатный вывоз", callback_data='free_export')],
        [InlineKeyboardButton("Сам привезу", callback_data='bring_myself')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Мы можем забрать и отвезти ваши вещи на склад бесплатно или можете привезти их сами по адресу - Ленинский просрект 100.', reply_markup=reply_markup)


def show_remaining_term(query) -> None:
    keyboard = [
        [InlineKeyboardButton("Главное меню", callback_data='update_main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    client_id = query.from_user.id
    client = Client.objects.filter(telegram_id=client_id).first()
    boxes_storage = Box.objects.filter(Q(client=client) | Q(status=("expired","in_storage")))
    if not boxes_storage:
        message = "У вас нет вещей на складе в хранении."
    else:
        message = "Ваши вещи хранятся до следующих дат:\n"
        for box in boxes_storage:
            message += f"- Бокс №{box.id}. Дата окончания хранения - {box.end_storage}. Статус хранения - {box.status}\n"
    query.message.reply_text(message, reply_markup=reply_markup)


def show_get_things(query) -> None:
    keyboard = [
        [InlineKeyboardButton("Заказать доставку", callback_data='delivery')],
        [InlineKeyboardButton("Главное меню", callback_data='update_main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    client_id = query.from_user.id
    client = Client.objects.filter(telegram_id=client_id).first()
    boxes_storage = Box.objects.filter(Q(client=client) | Q(status=("expired","in_storage")))
    if not boxes_storage:
        message = "У вас нет вещей на складе в хранении."
    else:
        message = "Вещи в хранение:\n"
        for box in boxes_storage:
            message += f"-Бокс №{box.id}. Дата хранения - с {box.start_storage} по {box.end_storage}. Статус хранения - {box.status}.\n"
    query.message.reply_text(message)
    query.message.reply_text("Забрать можно по адресу Ленинский проспект 100 с 9:00 по 18:00", reply_markup=reply_markup)


def show_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'update_conditions':
        update_storage_conditions(query)
    elif query.data == 'update_prohibited':
        update_storage_prohibited(query)
    elif query.data == "free_export":
        order_free_export(query)
    elif query.data == "bring_myself":
        select_bring_myself(query)
    elif query.data == "main_menu":
        show_main_menu(query.message)
    elif query.data == "update_main_menu":
        update_main_menu(query.message)
    elif query.data == "delivery":
        get_delivery(query)


def update_storage_conditions(query) -> None:
    with open("documents/Условия хранения.pdf", "rb") as file:
        query.message.reply_document(document=file, filename="Условия хранения.pdf")
    keyboard = [
        [InlineKeyboardButton("Сдать вещи", callback_data='handing_things')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выбирете пункт:',reply_markup=reply_markup)


def update_storage_prohibited(query) -> None:
    with open("documents/Запрет на хранение.pdf", "rb") as file:
        query.message.reply_document(document=file, filename="Запрет на хранение.pdf")
    keyboard = [
        [InlineKeyboardButton("Сдать вещи", callback_data='handing_things')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выбирете пункт:',reply_markup=reply_markup)


def order_free_export(query) -> None:
    keyboard = [
        [InlineKeyboardButton("Знаю размер", callback_data='know_size')],
        [InlineKeyboardButton("Нужен замер", callback_data='need_measure')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("Стоимость хранения зависит от размера, если вы не знаете размер, наш курьер измерит на месте. Выбирите пункт:", reply_markup=reply_markup)


def select_bring_myself(query) -> None:
    keyboard = [
        [InlineKeyboardButton("Забронировать место", callback_data='reserve')],
        [InlineKeyboardButton("Прайс", callback_data='price')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Вы можете ознакомиться с нашим прайсом и забронировать свободное место на складе', reply_markup=reply_markup)


def get_delivery(query) -> None:
    keyboard = [
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Для оформления доставки вещей свяжитесь с нашим менеджером по телефону +79999999999', reply_markup=reply_markup)


def consent_processing(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'know_size':
        consent_processing_handler(query)
    elif query.data == 'need_measure':
        consent_processing_handler(query)
    elif query.data == "reserve":
        consent_processing_handler(query)
    elif query.data == "price":
        price_update(query)


def price_update(query) -> None:
    with open("documents/Прайс.pdf", "rb") as file:
        query.message.reply_document(document=file, filename="Прайс.pdf")
    keyboard = [
        [InlineKeyboardButton("Забронировать место", callback_data='update_reserve')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выбирете пункт:', reply_markup=reply_markup)


def consent_processing_handler(query) -> None:
    keyboard = [
        [InlineKeyboardButton("Согласен на обработку данных", callback_data='consent')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выбирая этот пункт вы даете согласие на обработку персональных данных и что не будете хранить запрещенные предметы.', reply_markup=reply_markup)


def data_collection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'update_reserve':
        consent_processing_handler(query)


def new_order(update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        query.message.reply_text('Пожалуйста, введите ваше ФИО:')
        context.user_data['awaiting_full_name'] = True


def handle_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_full_name'):
        process_full_name(update, context)
    elif context.user_data.get('awaiting_address'):
        process_address(update, context)
    elif context.user_data.get('awaiting_phone'):
        process_phone_number(update, context)
    elif context.user_data.get('awaiting_email'):
        process_email(update, context)


def process_full_name(update: Update, context: CallbackContext) -> None:
    context.user_data['full_name'] = update.message.text
    update.message.reply_text('Введите ваш адрес:')
    context.user_data['awaiting_address'] = True
    context.user_data['awaiting_full_name'] = False


def process_address(update: Update, context: CallbackContext) -> None:
    context.user_data['address'] = update.message.text
    update.message.reply_text('Введите номер телефона:')
    context.user_data['awaiting_phone'] = True
    context.user_data['awaiting_address'] = False


def process_phone_number(update: Update, context: CallbackContext) -> None:
    context.user_data['phone'] = update.message.text
    update.message.reply_text('Введите ваш электронный адрес:')
    context.user_data['awaiting_email'] = True
    context.user_data['awaiting_phone'] = False


def process_email(update: Update, context: CallbackContext) -> None:
    context.user_data['email'] = update.message.text
    full_name = context.user_data['full_name']
    address = context.user_data['address']
    phone = context.user_data['phone']
    email = context.user_data['email']
    telegram_id = update.effective_user.id
    if not Client.objects.filter(telegram_id=telegram_id).exists():
        client = Client.objects.create(name=full_name, email=email, phone=phone, telegram_id=telegram_id)
    else:
        client = Client.objects.get(telegram_id=telegram_id)

    Order.objects.create(client=client, address=address)
    update.message.reply_text('Спасибо за вашу заявку. Наш менеджер свяжется с вами.')
    update.message.reply_text('Для запуска бота введите команду "/start"')
    context.user_data['awaiting_email'] = False


def update_data_collection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'consent':
        new_order(update, context)


if __name__ == '__main__':
    load_dotenv()

    telegram_api = os.environ["TELEGRAM_BOT_TOKEN"]
    bot = telegram.Bot(token=telegram_api)
    updater = Updater(token=telegram_api)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(main_menu_handler, pattern='^(conditions|prohibited|handing_things|remaining_term|get_things|handing)$'))
    dispatcher.add_handler(CallbackQueryHandler(show_handler, pattern='^(update_conditions|update_prohibited|free_export|bring_myself|main_menu|update_main_menu|delivery)$'))
    dispatcher.add_handler(CallbackQueryHandler(consent_processing, pattern='^(know_size|need_measure|reserve|price)$'))
    dispatcher.add_handler(CallbackQueryHandler(data_collection, pattern='^(update_reserve)$'))
    dispatcher.add_handler(CallbackQueryHandler(update_data_collection, pattern='^(consent)$'))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    print('Бот в сети')
    updater.idle()
