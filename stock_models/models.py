from django.db import models

class Bitlink(models.Model):
    original_url = models.URLField()
    bitlink = models.URLField(blank=True, null=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.bitlink or self.original_url
