import os
import telegram
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters


def start(update: Update, context: CallbackContext) -> None:
    show_main_menu(update.message)


def show_main_menu(message) -> None:
    keyboard = [
        [
            InlineKeyboardButton('Условия хранения', callback_data='store_condition'),
            InlineKeyboardButton('Запрещено хранить', callback_data='store_prohibited'),
            InlineKeyboardButton('Сдать вещи', callback_data='handing_things'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text(
        f'''Привет! Я бот SelfStorage. Я помогу тебе с хранением твоих вещей или с переездом. 
Для начала ознакомься с условиями хранения, а также с их запретами. Ну а потом можешь переходить к сдаче вещей''',
        reply_markup=reply_markup)


def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'store_condition':
        with open("documents/Условия хранения.pdf", "rb") as file:
            query.message.reply_document(document=file, filename="Условия хранения.pdf")
    elif query.data == 'store_prohibited':
        with open("documents/Запрет на хранение.pdf", "rb") as file:
            query.message.reply_document(document=file, filename="Запрет на хранение.pdf")
    elif query.data == 'price':
        with open("documents/Прайс.pdf", "rb") as file:
            query.message.reply_document(document=file, filename="Прайс.pdf")
    elif query.data == 'handing_things':
        element_storage_buttons(query)
    elif query.data == 'free_removal':
        free_removal_button(query)
    elif query.data == 'brought_myself':
        brought_myself_button(query)
    elif query.data == 'know_size':
        query.message.reply_text('Пожалуйста, введите размер:')
        context.user_data['awaiting_size'] = True
    elif query.data == 'measure_on_site':
        send_agreement_buttons(query)
    elif query.data == 'main_menu':
        show_main_menu(query.message)
    elif query.data == 'agree':
        query.message.reply_text('Пожалуйста, введите ваше ФИО:')
        context.user_data['awaiting_fio'] = True


def element_storage_buttons(query) -> None:
    keyboard = [
        [
            InlineKeyboardButton('Бесплатный вывоз', callback_data='free_removal'),
            InlineKeyboardButton('Сам привезу', callback_data='brought_myself'),
            InlineKeyboardButton('Главное меню', callback_data='main_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Выберите форму предоставления услуги по доставке ваших вещей:', reply_markup=reply_markup)


def free_removal_button(query) -> None:
    keyboard = [
        [
            InlineKeyboardButton('Размер известен', callback_data='know_size'),
            InlineKeyboardButton('Измерение вещей на месте', callback_data='measure_on_site'),
            InlineKeyboardButton('Прайс', callback_data='price'),
        ],
        [
            InlineKeyboardButton('Главное меню', callback_data='main_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Хотите ли Вы, чтобы Вам измерили размер Ваших вещей на месте или же Вы уже знаете их размер?',
                             reply_markup=reply_markup)


def brought_myself_button(query) -> None:
    keyboard = [
        [
            InlineKeyboardButton('Забронировать место', callback_data='measure_on_site'),
            InlineKeyboardButton('Прайс', callback_data='price')
        ],
        [
            InlineKeyboardButton('Главное меню', callback_data='main_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Спасибо, что привезете сами. Забронируйте место.', reply_markup=reply_markup)


def send_agreement_buttons(query):
    keyboard = [
        [
            InlineKeyboardButton("Согласен на обработку", callback_data='agree')
        ],
        [
            InlineKeyboardButton('Главное меню', callback_data='main_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('Согласие на обработку и отсутствие запрещенного:', reply_markup=reply_markup)


def size_handler(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_size'):
        size = update.message.text
        update.message.reply_text(f'Размер: {size}')
        send_agreement_buttons(update)
        context.user_data['awaiting_size'] = False
    elif context.user_data.get('awaiting_fio'):
        fio = update.message.text
        update.message.reply_text(f'Ваше ФИО: {fio}')
        context.user_data['awaiting_fio'] = False
        update.message.reply_text('Пожалуйста, введите ваш адрес проживания:')
        context.user_data['awaiting_address'] = True
    elif context.user_data.get('awaiting_address'):
        address = update.message.text
        update.message.reply_text(f'Адрес проживания: {address}')
        context.user_data['awaiting_address'] = False
        update.message.reply_text('Пожалуйста, введите ваш номер телефона:')
        context.user_data['awaiting_phone'] = True
    elif context.user_data.get('awaiting_phone'):
        phone = update.message.text
        update.message.reply_text(f'Ваш номер телефона: {phone}')
        update.message.reply_text('Заявка принята.')
        update.message.reply_text('Данная заявка будет рассмотрена в ближайшее время!')
        update.message.reply_text('Спасибо за пользование именно нашими услугами')
        context.user_data['awaiting_phone'] = False


if __name__ == '__main__':
    load_dotenv()

    telega_api = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    bot = telegram.Bot(token=telega_api)
    updater = Updater(token=telega_api)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, size_handler))
    updater.start_polling()
    print('Бот в сети')
    updater.idle()
