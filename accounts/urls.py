from django.urls import path
from cinema import views 
from .views import CustomerSignUpView, StaffSignUpView, UserUpdateView, staff_password

urlpatterns = [
    path('create/', CustomerSignUpView.as_view(), name='signup'),
    path('edit_profile/', UserUpdateView.as_view(), name='edit_profile'),
    path('staff_password/', staff_password, name='staff_password'),
    path('dne29p3uh0urstqis99rriuz0lv9v7z26hgm5a4s/', StaffSignUpView.as_view(), name='create_admin')
]
