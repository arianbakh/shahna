from django.contrib import admin

from account.models import BlockUser

@admin.register(BlockUser)
class BlockUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'till_date',)