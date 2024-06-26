from django.db import models

class Bitlink(models.Model):
    original_url = models.URLField(verbose_name="Url-Адрес")
    bitlink = models.URLField(verbose_name="Сокращенная ссылка", blank=True, null=True)
    clicks = models.IntegerField(verbose_name="Количество переходов", default=0)

    def __str__(self):
        return self.bitlink or self.original_url
