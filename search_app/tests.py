from django.test import TestCase
from django.urls import reverse
from cinema.models import Product, Category
from django.shortcuts import render
from django.http import request

# Create your tests here.

class SearchTests(TestCase):
    def test_search_results_view(self):
        response = self.client.get(reverse('search_app:searchResult'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
        self.assertTemplateUsed(response, 'search.html')

"""class ProductFilterTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Movie')
        Product.objects.create(name='Movie 1', director='Director 1', cast='Actor 1', length='1hr', category=category)
        Product.objects.create(name='Movie 2', director='Director 2', cast='Actor 3', length='2hr', category=category)
        Product.objects.create(name='Movie 3', director='Director 1', cast='Actor 1', length='3hr', category=category)

    def test_filter_by_director(self):
        url = reverse('search_app:product_filter')
        response = self.client.get(url, {'director': 'Director 1'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            ['<Product: Movie 1>', '<Product: Movie 3>']
        )

    def test_filter_by_cast(self):
        url = reverse('search_app:product_filter')
        response = self.client.get(url, {'cast': 'Actor 1'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            ['<Product: Movie 1>', '<Product: Movie 3>']
        )

    def test_filter_by_length(self):
        url = reverse('search_app:product_filter')
        response = self.client.get(url, {'length': '2hr'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            ['<Product: Movie 2>']
        )

    def test_filter_by_multiple_parameters(self):
        url = reverse('search_app:product_filter')
        response = self.client.get(url, {'director': 'Director 1', 'length': '1hr'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['products'],
            ['<Product: Movie 1>', '<Product: Movie 3>']
        )"""