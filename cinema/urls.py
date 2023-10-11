from django.urls import path
from .views import CategoryCreateView, CategoryDeleteView, MovieCreateView, MovieDeleteView, MovieUpdateView, TimeCreateView, TimeDeleteView
from . import views

app_name = 'cinema'

urlpatterns = [
    path('', views.prod_list, name = 'all_products'),
    path('genre/<uuid:category_id>/', views.prod_list, name = 'products_by_category'),
    path('movie/<uuid:product_id>/', views.product_detail, name='product_detail'),
    path('cinema/category_new/', CategoryCreateView.as_view(), name='category_new'), 
    path('cinema/<uuid:pk>/category_delete/', CategoryDeleteView.as_view(), name='category_delete'), 
    path('cinema/movie_new/', MovieCreateView.as_view(), name='movie_new'), 
    path('cinema/<uuid:pk>/movie_delete', MovieDeleteView.as_view(), name='movie_delete'), 
    path('cinema/<uuid:pk>/movie_edit', MovieUpdateView.as_view(), name='movie_edit'),
    path('cinema/<uuid:product_id>/movie_time_select/', views.select_time, name='select_time'),
    path('cinema/<uuid:screening_id>/seat_selection/', views.seat_selection, name='seat_selection'),
    path('cinema/<uuid:screening_id>/create_seats/', views.create_seats, name='create_seats'),
    path('cinema/create_time/', views.TimeCreateView.as_view(), name='time_new'), 
    path('cinema/<uuid:pk>/time_delete/', TimeDeleteView.as_view(), name='time_delete'),
    path("json", views.jsondata), # for generating json file
]
