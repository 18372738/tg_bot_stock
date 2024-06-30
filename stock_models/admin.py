from django.contrib import admin
from .models import Bitlink, Client, Box, Order
from vk_bitlink import shorten_link_vkontakte, get_clicks_vkontakte



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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone')
    list_filter = ('name',)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'start_storage', 'end_storage')
    list_filter = ('client', 'start_storage', 'end_storage', 'status')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'box', 'address')
    list_filter = ('client', 'date', 'box', 'state',)
