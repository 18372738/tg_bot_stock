# Python Stock Бот: Руководство по использыванию и документация
## Оглавление
- [Описание проекта](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#описание-проекта)
- [Что понадобиться?](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#что-понадобится)
  - [Предварительные требования](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#предварительные-требования)
  - [Установка зависимостей](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#установка-зависимостей)
  - [Переменные окружения](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#переменные-окружения)
  - [Дополнительные требования](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#дополнительные-требования)
  - [Запустить миграцию](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#запустить-миграцию)
  - [Создать суперпользователя](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#создать-суперпользователя) 
- [Как запустить?](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#как-запустить)
  - [Запуск админ-панели](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#запуск-админ-панели)
  - [Запуск бота](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#запуск-бота)
  - [Запуск планировщика задач](https://github.com/18372738/tg_bot_stock/blob/main/README.md#запуск-планировщика-задач)
- [Админ-панель](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#админ-панель)
  - [Таблицы с данными](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#таблицы-с-данными)
  - [Таблица статистики рекламы](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#таблица-статистики-рекламы)
- [Основные скрипты](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#основные-скрипты)
- [Цели проекта](https://github.com/18372738/tg_bot_stock?tab=readme-ov-file#цели-проекта)
### Описание проекта
Бот для хранения личных вещей на складе. Бот предоставляет пользователям возможность оставить заявку на хранение вещей на складе. После оставления вещей можно отслеживать срок хранения и получить данные по тому как забрать свои вещи. 
### Что понадобится?
#### Предварительные требования
Скачайте или склонируйте репозиторий на свой компьютер.
Python3 должен быть уже установлен. 
#### Установка зависимостей
Используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```commandline
pip install -r requirements.txt
```
#### Переменные окружения
Создайте файл ```.env``` в вашей директории проекта, откройте его в любом текстовом редакторе. Вам понадобятся следующие переменные окружения:
```python
VK_ACCESS_TOKEN='Сервисный токен приложения Вконтакте'
TELEGRAM_TOKEN='Токен вашего бота'
EMAIL_HOST='email host вашей электронной почты'
EMAIL_HOST_USER='ваш email для отправки писем'
EMAIL_HOST_PASSWORD='пароль для приложения (разрешает приложению отправлять письма)'
```
#### Дополнительные требования
Создать телеграм бота и получить токен. Для регистрации и получения токена, нужно написать в [@BotFather](https://t.me/BotFather)
```
/newbot - регистрация нового бота
/token - получить токен бота 
```
Для отслеживания статистики рекламы зарегестрируйтесь в социальной сети [Вконтакте](https://vk.com). Создайте [приложение](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/create-application). Получите сервисный [токен](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/tokens/service-token) приложения.
#### Запустить миграцию
Для настройки базы данных SQLite
```bush
python manage.py migrate
```
#### Создать суперпользователя 
Для получения логина и пароля от админ-панели
```bush
python manage.py createsuperuser
```
При запуске команды вам понадобиться ввести данные (логин, E-mail, пароль)
### Как запустить 
#### Запуск админ-панели 
```bush
python manage.py runserver
```


При запуске команды выводится url-адрес в конце которого нужно добавить ```/admin```, получится ссылка типа ```http://127.0.0.1:8000/admin```, которая откроет страницу с админ-панелью, где нужно будет ввести логин и пароль, который указывали при создании суперпользователя.
#### Запуск бота
```bush
python bot.py
```
При запуске команды, если все шаги сделали правильно, бот готов к работе.
#### Запуск планировщика задач 
Для отправки напоминаний в автоматическом режиме
```bush
python manage.py qcluster
```
При желании можно запускать отправку напоминаний один раз в день из оболочки ```shell```
Для этого в командной строке введите
```bush
python manage.py shell
```
В открывшейся интерактивной оболочке ```shell``` сделайте необходимые импорты

```commandline
import smtplib
import datetime
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from stock_models.models import Bitlink, Client, Box, Order
from stock_models.send_emails import reminder
```
Запустите функцию для отправки напоминаний
```commandline
reminder()
```

### Админ-панель
#### Таблицы с данными
Админка Django позволяет управлять данными бота. Просматривать данные таблицы, вносить изменения, удалять. В данном боте представлены 5 таблиц: bitlinks, клиенты, боксы, закзаы
#### Таблица статистики рекламы
Для отслеживания статистики рекламы вам понадобиться сокращённая ссылка. 
Чтобы получить сокращённую ссылку добавьте ваш Url-адрес в поле ```Url-адрес``` и нажмите кнопку ```сохранить```
![2024-06-27_00-48-46](https://github.com/18372738/tg_bot_stock/assets/133884450/5ed0358d-3c70-46e4-bb3f-f742b4333da3)

В таблице выберете нужную вам ссылку и из  выпадающего списка выберите ```Сократить выбранные ссылки``` 
![2024-06-27_00-50-12](https://github.com/18372738/tg_bot_stock/assets/133884450/bf2ca746-d51a-4d94-8100-3d90e1acc742)

Сокращенную ссылку используйте в рекламе, чтобы в данной таблице вы смогли увидеть количество переходов по ссылке. Выбрав нужную нам ссылку и из выпадающего списка выбрав ```Обновить переходы по выбранным битлинкам```.
Данные в поле ```Сокращённая ссылка``` и в поле ```Количество переходов``` заполняются автоматически.
### Основные скрипты
- [vk_bitlink.py](https://github.com/18372738/tg_bot_stock/blob/main/vk_utils.py)
- [admin.py](https://github.com/18372738/tg_bot_stock/blob/main/stock_models/admin.py)
- [models.py](https://github.com/18372738/tg_bot_stock/blob/main/stock_models/models.py)
- [bot.py](https://github.com/18372738/tg_bot_stock/blob/main/bot.py)
-[send_emails.py](https://github.com/18372738/tg_bot_stock/blob/main/stock_models/send_emails.py)
### Цели проекта
Проект написан в образовательных целях.



