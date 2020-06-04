from django.contrib import admin

# Register your models here.

from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = MenuItem

admin.site.register(MenuItem, MenuItemAdmin)