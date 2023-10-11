from django.urls import path
from .views import SearchResultsListView, product_filter

app_name='search_app'

urlpatterns = [
    path('', SearchResultsListView.as_view(), name='searchResult'),
    path('product_filter/', product_filter, name='product_filter'),
]
