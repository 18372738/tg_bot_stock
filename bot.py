import os
import sys
import telegram
import django
from dotenv import load_dotenv
from django.utils import timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock.settings')
django.setup()

from stock_models.models import Client, Order


def start(update: Update, context: CallbackContext) -> None:
    show_main_menu(update.message)


def show_main_menu(message) -> None:
    keyboard = [
        [InlineKeyboardButton('Условия хранения', callback_data='conditions')],
        [InlineKeyboardButton('Запрещено хранить', callback_data='prohibited')],
        [InlineKeyboardButton('Сдать вещи', callback_data='handing_things')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text('Привет! Я бот SelfStorage. Я помогу тебе оставить заявку на хранение вещей. Рекомендую ознакомиться с условиями хранения и что хранить запрещено.', reply_markup=reply_markup)


def main_menu_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'conditions':
        show_storage_conditions(query)
    elif query.data == 'prohibited':
        show_storage_prohibited(query)
    elif query.data == 'handing_things':
        show_handing_thing(query)


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
        show_main_menu(query)


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
    query.message.reply_text('Стоимость хранения зависит от размера, если вы не знаете размер, наш курьер измерит на месте. Выбирите пункт:', reply_markup=reply_markup)


def select_bring_myself(query) -> None:
    keyboard = [
        [InlineKeyboardButton("Забронировать место", callback_data='reserve')],
        [InlineKeyboardButton("Прайс", callback_data='price')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Вы можете ознакомиться с нашим прайсом и забронировать свободное место на складе', reply_markup=reply_markup)


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
        [InlineKeyboardButton("Согласие", callback_data='consent')],
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
    dispatcher.add_handler(CallbackQueryHandler(main_menu_handler, pattern='^(conditions|prohibited|handing_things)$'))
    dispatcher.add_handler(CallbackQueryHandler(show_handler, pattern='^(update_conditions|update_prohibited|free_export|bring_myself)$'))
    dispatcher.add_handler(CallbackQueryHandler(consent_processing, pattern='^(know_size|need_measure|reserve|price)$'))
    dispatcher.add_handler(CallbackQueryHandler(data_collection, pattern='^(update_reserve)$'))
    dispatcher.add_handler(CallbackQueryHandler(update_data_collection, pattern='^(consent)$'))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    print('Бот в сети')
    updater.idle()
