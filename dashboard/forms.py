from django.forms import ModelForm

from dashboard.models import Picture


class PictureForm(ModelForm):

    class Meta:
        model = Picture
        fields = ['name', 'description', 'image']
