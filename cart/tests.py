from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from unittest.mock import MagicMock
from django.urls import reverse
from cinema.models import Product, Category, Screening, Seat
from extras.models import Extra
from .models import Cart, MovieCartItem, ExtraCartItem
from .views import MovieCartItem, ExtraCartItem, movie_add_cart, extra_add_cart

# Create your tests here.
class AddCartViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.get('/')
        get_response = MagicMock()
        self.session_middleware = SessionMiddleware(get_response)
        response = self.session_middleware(request)

        #Create test data
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', category=self.category)
        self.screening = Screening.objects.create(movie=self.product, date='2023-04-21', time='21:00:00')
        self.seat = Seat.objects.create(screening=self.screening, number=20, is_available=True)
        self.extra = Extra.objects.create(description='Mega Deal', price=10, stock=20)
        self.cart = Cart.objects.create()
        self.cart_item1 = MovieCartItem.objects.create(product=self.product, screening=self.screening, cart=self.cart)
        self.cart_item1.seats.set([self.seat])
        self.cart_item2 = ExtraCartItem.objects.create(extra=self.extra, cart=self.cart, quantity=2)
    
    def test_add_cart_view(self):
        # set up test request 
        request = self.factory.post(reverse('cart:movie_add_cart', args= [self.screening.id] ))
        request_two = self.factory.post(reverse('cart:extra_add_cart', args=[self.extra.id] ))
        self.session_middleware.process_request(request)
        self.session_middleware.process_request(request_two)
        request.session.save()
        request_two.session.save()
        #call view function
        response = movie_add_cart(request, self.screening.id)
        response_two = extra_add_cart(request, self.extra.id)
        #check that cart items were added
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(MovieCartItem.objects.filter(cart=self.cart)), 1)
        self.assertEqual(MovieCartItem.objects.filter(cart=self.cart, product=self.product, screening=self.screening, seats=self.seat).count(), 1)
        self.assertEqual(len(ExtraCartItem.objects.filter(cart=self.cart)), 1)
        self.assertEqual(ExtraCartItem.objects.filter(cart=self.cart, extra=self.extra).count(), 1)

    def tearDown(self):
        self.category.delete()
        self.product.delete()
        self.screening.delete()
        self.seat.delete()
        self.extra.delete()
        self.cart.delete()
        self.cart_item1.delete()
        self.cart_item2.delete()

