from django.contrib import admin

from account.models import BlockUser, Profile

@admin.register(BlockUser)
class BlockUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'till_date',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'university', 'phone')
    search_fields = ('user__username', 'name', 'university')
