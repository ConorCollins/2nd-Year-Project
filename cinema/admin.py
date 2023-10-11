from django.contrib import admin
from .models import Category, Product, Screening, Seat

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_editable = ['name']
    list_display_links = None

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_categories', 'available', 'created', 'updated', 'image', 'trailer', 'director', 'cast', 'length']
    list_editable = ['name', 'description', 'available', 'image', 'trailer']
    list_per_page = 20
    list_display_links = None

    """def get_categories(self, obj):
        # Custom method to get comma-separated list of categories for a movie
        return ", ".join([category.name for category in obj.category.all()])
    get_categories.short_description = 'Categories' # Set column name in the admin list view"""


admin.site.register(Product, ProductAdmin)

class ScreeningAdmin(admin.ModelAdmin):
    list_display = ['movie', 'time', 'date']
    list_editable = ['time', 'date']
    list_per_page = 20

admin.site.register(Screening, ScreeningAdmin)

class SeatAdmin(admin.ModelAdmin):
    list_display = ['screening', 'number', 'is_available']
    list_editable = ['is_available']
    list_per_page = 40

admin.site.register(Seat, SeatAdmin)

