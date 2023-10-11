from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomerCreationForm, StaffCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username','age','is_staff',]
    
admin.site.register(CustomUser, CustomUserAdmin)
