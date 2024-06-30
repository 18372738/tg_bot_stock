from django.db import models

BOX_CHOICES = (
    ('reserved', 'зарезервирован'),
    ('in_storage', 'на хранении'),
    ('removed', 'снят с хранения'),
    ('expired', 'просрочен'),
)

ORDER_CHOICES = (
    ('todo', 'принять в работу'),
    ('true', 'подтвержден'),
    ('topay', 'выставить счет'),
    ('false', 'отменен'),
)


class Bitlink(models.Model):
    original_url = models.URLField(verbose_name="Url-Адрес")
    bitlink = models.URLField(verbose_name="Сокращенная ссылка", blank=True, null=True)
    clicks = models.IntegerField(verbose_name="Количество переходов", default=0)

    def __str__(self):
        return self.bitlink or self.original_url


class Client(models.Model):
    name = models.CharField('ФИО', max_length=200)
    email = models.EmailField('email', unique=True)
    phone = models.CharField('Телефон', max_length=200)
    telegram_id = models.CharField('телеграмм ID', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Box(models.Model):
    start_storage = models.DateTimeField('начало хранения')
    end_storage = models.DateTimeField('конец хранения')
    client = models.ForeignKey(Client,
                               verbose_name='клиент',
                               on_delete=models.CASCADE,
                               related_name='boxes')
    size = models.PositiveIntegerField('кв.м', null=True, blank=True)
    status = models.CharField('статус', choices=BOX_CHOICES, max_length=10, default='reserved')

    def __str__(self):
        return f'бокс {self.id}'

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'


class Order(models.Model):
    client = models.ForeignKey(Client,
                               verbose_name='клиент',
                               on_delete=models.CASCADE,
                               related_name='orders')
    date = models.DateField(auto_now_add=True)
    address = models.TextField('адрес')
    box = models.OneToOneField(Box, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField('цена', null=True, blank=True)
    state = models.CharField('состояние', choices=ORDER_CHOICES, max_length=9, default='todo')

    def __str__(self):
        return f'заказ {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
