from django.shortcuts import render
from .models import Extra
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse

# Create your views here.

def extras_list(request):
    products = Extra.objects.all()
        
    paginator = Paginator(products, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
         page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'extras.html', {'prods':products})

class ExtraCreateView(CreateView):
    model = Extra
    fields = ('description', 'price', 'stock', 'image')
    template_name = 'extra_new.html'

class ExtraDeleteView(DeleteView):
    model = Extra
    template_name = 'extra_delete.html'
    success_url = reverse_lazy('extras:all_extras')

class ExtraUpdateView(UpdateView):
    model = Extra
    fields = ('description', 'price', 'stock', 'image')
    template_name = 'extra_edit.html'