from django.db import models
from cinema.models import Product, Screening, Seat
from extras.models import Extra

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id

class MovieCartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    numSeats = models.PositiveIntegerField(null=True, default=0)
    #seats = models.TextField()
    #extras = models.ManyToManyField(Extra)
    #extras_quantity = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'MovieCartItem'

    def sub_total(self):
        return self.numSeats * 10.0

    def __str__(self):
        return self.product

class ExtraCartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    extra = models.ForeignKey(Extra, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ExtraCartItem'

    def sub_total(self):
        return self.extra.price * self.quantity

    def __str__(self):
        return self.extra