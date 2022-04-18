from django.contrib import admin

from users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'first_name', 'last_name')

admin.site.register(CustomUser, CustomUserAdmin)