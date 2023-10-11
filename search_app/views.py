from cinema.models import Product, Category
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render

# Create your views here.

class SearchResultsListView(ListView):
    models = Product
    context_object_name = 'product_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

def product_filter(request):
    category = request.GET.get('category')
    director = request.GET.get('director')
    cast = request.GET.get('cast')
    length = request.GET.get('length')

    filter_kwargs = {}
    if category:
        filter_kwargs['category__name__icontains'] = category
    if director:
        filter_kwargs['director__icontains'] = director
    if cast:
        filter_kwargs['cast__icontains'] = cast
    if length:
        filter_kwargs['length__icontains'] = length

    products = Product.objects.filter(**filter_kwargs)

    return render(request, 'product_filter.html', {'products': products})