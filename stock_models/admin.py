from django.contrib import admin
from .models import Bitlink
from vk_utils import shorten_link_vkontakte, get_clicks_vkontakte



@admin.register(Bitlink)
class BitlinkAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'bitlink', 'clicks')
    actions = ['shorten_links', 'update_clicks']

    def shorten_links(self, request, queryset):
        for bitlink in queryset:
            if not bitlink.bitlink:
                try:
                    shortened = shorten_link_vkontakte(bitlink.original_url)
                    bitlink.bitlink = shortened
                    bitlink.save()
                    self.message_user(request, f"Ссылка '{bitlink.original_url}' сокращена до '{shortened}'", level='info')
                except Exception as e:
                    self.message_user(request, f"Ошибка: {e}", level='error')
        self.message_user(request, "Ссылки успешно сокращены", level='success')

    shorten_links.short_description = "Сократить выбранные ссылки"

    def update_clicks(self, request, queryset):
        for bitlink in queryset:
            if bitlink.bitlink:
                try:
                    stats = get_clicks_vkontakte(bitlink.bitlink)
                    total_clicks = sum(stat['views'] for stat in stats)
                    bitlink.clicks = total_clicks
                    bitlink.save()
                    self.message_user(request, f"Ссылка '{bitlink.bitlink}' имеет {total_clicks} переходов", level='info')
                except Exception as e:
                    self.message_user(request, f"Ошибка: {e}", level='error')
        self.message_user(request, "Переходы обновлены", level='success')

    update_clicks.short_description = "Обновить переходы по выбранным битлинкам"
