from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Category, Product, Screening, Reviews, Seat
from extras.models import Extra
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .forms import CreateNewMovie, EditMovie, CreateNewTime
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

# Create your views here.
def prod_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_id != None:
        category = get_object_or_404(Category, id = category_id)
        products = Product.objects.filter(category = category)
        
    paginator = Paginator(products, 12)
    try:
        page = int(request.GET.get('page', '1'))
    except:
         page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'category':category, 'prods':products})

def product_detail(request,  product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        rating = request.POST.get("rating", 3)
        comment = request.POST.get('comment', "")

        if comment:
            reviews = Reviews.objects.filter(created_by=request.user, product = product)
            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.comment = comment
                review.save()
            else:
                review = Reviews.objects.create(
                    rating = rating,
                    product = product,
                    comment = comment,
                    created_by = request.user
            )
            return redirect('.')
    return render(request, 'product.html', {'product':product})

class MovieCreateView(CreateView):
    model = Product
    template_name = 'movie_new.html'
    form_class = CreateNewMovie

    def form_valid(self, form):
        return super().form_valid(form)

class MovieDeleteView(DeleteView):
    model = Product
    template_name = 'movie_delete.html'
    success_url = reverse_lazy('cinema:all_products')

class MovieUpdateView(UpdateView):
    model = Product
    template_name = 'movie_edit.html'
    form_class = EditMovie

class CategoryCreateView(CreateView):
    model = Category
    fields = ('name',)
    template_name = 'category_new.html'

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('cinema:all_products')

class TimeCreateView(CreateView):
    model = Screening
    template_name = 'time_new.html'
    #success_url = reverse_lazy('cinema:all_products')
    form_class = CreateNewTime

    def form_valid(self, form):
        return super().form_valid(form)
    

class TimeDeleteView(DeleteView):
    model = Screening
    template_name = 'time_delete.html'
    success_url = reverse_lazy('cinema:all_products')

    """def get_success_url(self):
        # Get the parent model instance related to the child model
        parent_model = Product.objects.get(id=self.object.movie.id)
        # Redirect to the detail view of the parent model instance
        return reverse('cinema:product_detail', args=[self.object.movie.id])"""

def select_time(request, product_id):
    movie = get_object_or_404(Product, id=product_id)
    screenings = Screening.objects.filter(movie=movie).order_by('date', 'time')
    context = {'movie':movie, 'screenings':screenings}
    return render(request, 'time_select.html', context)

def create_seats(request, screening_id):
    screening = get_object_or_404(Screening, id=screening_id)
    for i in range(40):
        seats = [Seat(screening=screening, number=i+1)]
        Seat.objects.bulk_create(seats)
    
    return render(request, 'seats_created.html', {'screening': screening})


def seat_selection(request, screening_id):
    screening = get_object_or_404(Screening, pk=screening_id)
    seats = Seat.objects.filter(screening=screening)
    context = {
        "gap" : [4,12,20,28,36],
        "rowEnd" : [8,16,24,32,40],
        'screening': screening, 
        'seats': seats,
    }
    return render(request, 'seat_selection.html', context)



# For creating json file

from django.core import serializers
from django.http import HttpResponse

def jsondata(request):
    cats = Category.objects.all()
    cat_list = serializers.serialize('json', cats)

    prods = Product.objects.all()
    prod_list = serializers.serialize('json', prods)

    screens = Screening.objects.all()
    screen_list = serializers.serialize('json', screens)

    seats = Seat.objects.all()
    seats_list = serializers.serialize('json', seats)

    extras = Extra.objects.all()
    extras_list = serializers.serialize('json', extras)

    return HttpResponse(extras_list, content_type="text/json-comment-filtered")

