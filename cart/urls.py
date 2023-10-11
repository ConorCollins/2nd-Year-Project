from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('add_movie/<uuid:screening_id>/', views.movie_add_cart, name='movie_add_cart'),
    path('add_extra/<uuid:extra_id>/', views.extra_add_cart, name='extra_add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove_extra/<uuid:extra_id>/', views.extra_cart_remove, name='extra_cart_remove'),
    path('full_remove_extra/<uuid:extra_id>/', views.extra_full_remove, name='extra_full_remove'),
    path('full_remove_movie/<uuid:screening_id>/', views.movie_full_remove, name='movie_full_remove'),

]
