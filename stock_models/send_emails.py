import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import datetime
import smtplib
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from stock_models.models import Box


def reminder():
    time_now = datetime.date.today()
    three_days_before_end = time_now + timedelta(days=3)
    two_weeks_before_end = time_now + timedelta(weeks=2)
    three_weeks_before_end = time_now + timedelta(weeks=3)
    one_month_before_end = time_now + timedelta(days=30)
    dates = [three_days_before_end,
             two_weeks_before_end,
             three_weeks_before_end,
             one_month_before_end
             ]
    boxes_in_storage = Box.objects.filter(end_storage__in=dates)
    for box in boxes_in_storage:
        try:
            send_mail(
                # title:
                'напоминание',
                # message:
                f'конец срока хранения {box.end_storage}. \n'
                f'Вы можете забрать вещи сами или заказать доставку.',
                # from:
                settings.EMAIL_HOST_USER,
                # to:
                [box.client.email],
                fail_silently=False,
            )
        except smtplib.SMTPRecipientsRefused as e:
            print(f'Error sending email:  {e}')

    pick_up_today = Box.objects.filter(end_storage=time_now)
    for box in pick_up_today:
        try:
            send_mail(
                # title:
                'напоминание',
                # message:
                f'Заберите вещи сегодня. Вы можете забрать вещи сами или заказать доставку.\n'
                f'Если вы не заберете вещи, они будут храниться 6 месяцев, но тариф будет чуть выше.\n'
                f' После чего вы их потеряете',
                # from:
                settings.EMAIL_HOST_USER,
                # to:
                [box.client.email],
                fail_silently=False,
            )
        except smtplib.SMTPRecipientsRefused as e:
            print(f'Error sending email:  {e}')

    one_month_before_today = time_now - timedelta(days=30)
    two_month_before_today = time_now - timedelta(days=60)
    three_month_before_today = time_now - timedelta(days=90)
    four_month_before_today = time_now - timedelta(days=120)
    five_month_before_today = time_now - timedelta(days=150)
    six_month_before_today = time_now - timedelta(days=180)
    dates = [one_month_before_today,
             two_month_before_today,
             three_month_before_today,
             four_month_before_today,
             five_month_before_today,
             six_month_before_today
             ]
    expired_boxes = Box.objects.filter(end_storage__in=dates)
    for box in expired_boxes:
        pick_up_time = box.end_storage + timedelta(days=180)
        try:
            send_mail(
                # title:
                'напоминание',
                # message:
                f'Хранение просрочено. Заберите вещи до {pick_up_time}.\n'
                f'Вы можете забрать вещи сами или заказать доставку',
                # from:
                settings.EMAIL_HOST_USER,
                # to:
                [box.client.email],
                fail_silently=False,
            )
        except smtplib.SMTPRecipientsRefused as e:
            print(f'Error sending email:  {e}')


if __name__ == '__main__':
    reminder()
