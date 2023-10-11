from django.contrib import admin
from .models import Extra

# Register your models here.
class ExtraAdmin(admin.ModelAdmin):
    list_display = ['description', 'price', 'stock', 'image']
    list_editable = ['price', 'stock']
    list_per_page = 20

admin.site.register(Extra, ExtraAdmin)