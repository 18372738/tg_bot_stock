from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from stock_models.models import Client, Box


def reminder():
    boxes_in_storage = Box.objects.filter(status='in_storage')
    for box in boxes_in_storage:

        msg = EmailMultiAlternatives(
            # title:
            'напоминание',
            # message:
            f'конец срока хранения {box.end_storage}',
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [box.client.email]
        )
        msg.send()
        print(f'сообщение отправлено на {box.client.email}')
