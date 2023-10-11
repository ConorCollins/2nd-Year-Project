from accounts.models import CustomUser
from django.db import models
import uuid
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from django import forms
import datetime
from imagekit.models import ImageSpecField

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('cinema:products_by_category', args=[self.id])
    
    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to = 'product_images', blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    trailer = EmbedVideoField(blank=True)
    director = models.CharField(max_length=100, blank=True)
    cast = models.CharField(max_length=200, blank=True)
    length = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_categories(self):
        return ",".join([str(cat) for cat in self.category.all()])

    def get_absolute_url(self):
        return reverse('cinema:product_detail', args=[str(self.id)])
   
    def __str__(self):
        return self.name

    def overall_rating(self):
        total_reviews = 0 
        for review in self.reviews.all():
            total_reviews += review.rating
        if total_reviews > 0:
                return round(total_reviews / self.reviews.count(),1)
        return 0
    

class Screening(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    movie = models.ForeignKey(Product, on_delete=models.CASCADE)
    def check_date(value):
        if value < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return value
    date = models.DateField(validators=[check_date])
    time = models.TimeField()

    class Meta:
        ordering = ('movie',)
        verbose_name = 'screening'
        verbose_name_plural = 'screenings'
    
    # made so that seats are automatically created
    def get_absolute_url(self):
        return reverse('cinema:create_seats', args=[self.id])
    

class Seat(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ('screening',)
        verbose_name = 'seat'
        verbose_name_plural = 'seats'
    
    def __str__(self):
        return str(self.number)    

    
class Reviews(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    comment = models.TextField()
    created_by = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
