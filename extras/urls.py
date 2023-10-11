from django.urls import path
from .views import extras_list, ExtraCreateView, ExtraDeleteView, ExtraUpdateView

app_name='extras'

urlpatterns = [
    path('', extras_list, name = 'all_extras'),
    path('new/', ExtraCreateView.as_view(), name = 'extra_create'),
    path('<uuid:pk>/delete', ExtraDeleteView.as_view(), name='extra_delete'), 
    path('<uuid:pk>/edit', ExtraUpdateView.as_view(), name='extra_edit'),
]