from django.db import models

BOX_CHOICES = (
    ('in_storage', 'на хранении'),
    ('removed', 'снят с хранения'),
)

ORDER_CHOICES = (
    ('adopted', 'принят'),
    ('fulfilled', 'исполнен'),
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Box(models.Model):
    start_storage = models.DateField('начало хранения')
    end_storage = models.DateField('конец хранения')
    client = models.ForeignKey(Client,
                               verbose_name='клиент',
                               on_delete=models.CASCADE,
                               related_name='boxes')
    status = models.CharField('статус', choices=BOX_CHOICES, max_length=10, default='in_storage')

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
    address = models.TextField('адрес', null=True, blank=True)
    phone = models.IntegerField('телефон', unique=True)
    box = models.OneToOneField(Box, on_delete=models.CASCADE, null=True, blank=True)
    size = models.PositiveIntegerField('кв.м', null=True, blank=True)
    price = models.PositiveIntegerField('цена', null=True, blank=True)
    state = models.CharField('состояние', choices=ORDER_CHOICES, max_length=9, default='adopted')


    def __str__(self):
        return f'заказ {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
