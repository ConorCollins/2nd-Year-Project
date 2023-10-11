from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Category, Screening, Seat, Reviews
from django.contrib.auth import get_user_model


class CategoryTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
        name = 'Test Category'
    )
        
    def test_category_listing(self):
        self.assertEqual(f'{self.category.name}', 'Test Category')
        self.assertEqual(str(self.category), self.category.name)

    def test_category_detail_view(self):
        response = self.client.get(self.category.get_absolute_url())
        no_response = self.client.get('/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Category')
        self.assertTemplateUsed(response, 'category.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'top-navbar.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'slideshow.html')
        self.assertTemplateUsed(response, 'footer.html')
        


class ProductTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name = 'Test Product',
            description = 'product test description',
            category = Category.objects.create(name = 'Test Category'),
            image = 'test.png',
            trailer = 'https://www.youtube.com/watch?v=HWEW_qTLSEE',
            director = 'test director',
            cast = 'cast1, cast2, cast3',
            length = '1h 1m'
        )

    def test_product_listing(self):
        self.assertEqual(f'{self.product.name}', 'Test Product')
        self.assertEqual(f'{self.product.description}', 'product test description')
        #self.assertEqual(f'{self.product.category}', Category.objects.get(name='Test Category'))
        self.assertEqual(f'{self.product.category}', 'Test Category')
        self.assertEqual(f'{self.product.image}', 'test.png')
        self.assertEqual(f'{self.product.trailer}', 'https://www.youtube.com/watch?v=HWEW_qTLSEE')
        self.assertEqual(f'{self.product.director}', 'test director')
        self.assertEqual(f'{self.product.cast}', 'cast1, cast2, cast3')
        self.assertEqual(f'{self.product.length}', '1h 1m')
        self.assertEqual(str(self.product), self.product.name)
        #self.assertEqual(self.product.overall_rating, 0)

    """
    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        no_response = self.client.get('/12345/9876/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'cinema/product.html')
        #response2 = self.client.post(self.product.get_absolute_url(), {'user': self.user, 'product': self.product})
        #self.assertEqual(response2.status_code, 200)
    """
    

    def test_product_list_view(self):
        response = self.client.get(reverse('cinema:all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'category.html')
        self.assertTemplateUsed(response, 'category.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'top-navbar.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'slideshow.html')
        self.assertTemplateUsed(response, 'footer.html')



class ScreeningTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create( name = 'Test Product', description = 'product test description', category = Category.objects.create(name = 'Test Category'), image = 'test.png', trailer = 'https://www.youtube.com/watch?v=HWEW_qTLSEE', director = 'test director', cast = 'cast1, cast2, cast3', length = '1h 1m' )
        self.screening = Screening.objects.create(
            movie = self.product,
            date = '2023-04-12',
            time = '18:00:00',
        )

    def test_screening_listing(self):
        self.assertEqual(f'{self.screening.movie}', 'Test Product')
        self.assertEqual(f'{self.screening.date}', '2023-04-12')
        self.assertEqual(f'{self.screening.time}', '18:00:00')
    

class SeatTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create( name = 'Test Product', description = 'product test description', category = Category.objects.create(name = 'Test Category'), image = 'test.png', trailer = 'https://www.youtube.com/watch?v=HWEW_qTLSEE', director = 'test director', cast = 'cast1, cast2, cast3', length = '1h 1m' )
        self.screening = Screening.objects.create( movie = self.product, date = '2023-04-12', time = '18:00:00', )
        self.seat = Seat.objects.create(
            screening = self.screening,
            number = '20'
        )

    def test_seat_listing(self):
        self.assertEqual(f'{self.seat.number}', '20')
        self.assertEqual(str(self.seat), self.seat.number)


class ReviewTests(TestCase):
    def setUp(self): 
        self.product = Product.objects.create( name = 'Test Product', description = 'product test description', category = Category.objects.create(name = 'Test Category'), image = 'test.png', trailer = 'https://www.youtube.com/watch?v=HWEW_qTLSEE', director = 'test director', cast = 'cast1, cast2, cast3', length = '1h 1m' )
        self.user = get_user_model().objects.create_user( username='testuser', email='testuser@test.com', age='44', password='testing123' )
        self.review = Reviews.objects.create(
            product = self.product,
            rating = '5',
            comment = 'test comment',
            created_by = self.user
        )

    def test_review_listing(self):
        self.assertEqual(f'{self.review.rating}', '5')
        self.assertEqual(f'{self.review.comment}', 'test comment')

