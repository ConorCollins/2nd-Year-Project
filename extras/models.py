from django.db import models
import uuid
from django.urls import reverse

# Create your models here.

class Extra(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to = 'extra', blank=True)

    class Meta:
        ordering = ('-price','description',)
        verbose_name = 'extra'
        verbose_name_plural = 'extras'
    
    def __str__(self):
        return self.description
    
    def get_absolute_url(self):
        return reverse('extras:all_extras')