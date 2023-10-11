from django import forms
from .models import Product, Screening

class CreateNewMovie(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image', 'available', 'trailer', 'director', 'cast', 'length',] 
        labels = {
            'name': 'Movie Title',
            'description': 'Movie Description',
            'category': 'Movie Genre(s)',
            'image': 'Movie Image',
            'available': 'Availability',
            'trailer' : 'Trailer',
            'director' : 'Director',
            'cast' : 'Cast',
            'length' : 'Duration', 
        }
        widgets = {
            'description' : forms.TextInput(attrs={'class': 'rows=3'}),
        }

class EditMovie(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image', 'available', 'trailer', 'director', 'cast', 'length',]
        labels = {
            'name': 'Movie Title',
            'description': 'Movie Description',
            'category': 'Movie Genre(s)',
            'image': 'Movie Image',
            'available': 'Availability',
            'trailer' : 'Trailer',
            'director' : 'Director',
            'cast' : 'Cast',
            'length' : 'Duration',
        }
        widgets = {
            'description' : forms.TextInput(attrs={'class': 'rows=3'}),
        }

class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = ['date', 'time']

class CreateNewTime(forms.ModelForm):
    time_choices = (
        ('10:00:00', '10:00 AM'),
        ('13:00:00', '1:00 PM'),
        ('16:00:00', '4:00 PM'),
        ('19:00:00', '7:00 PM'),
        ('20:00:00', '8:00 PM'),
        ('21:00:00', '9:00 PM'),
        ('22:00:00', '10:00 PM'),
    )
    time = forms.ChoiceField(choices=time_choices)
    class Meta:
        model = Screening
        fields = ['movie', 'date', 'time']
        labels = {
            'movie' : 'Movie Title',
            'date' : 'Date',
            'time' : 'Time'
        }