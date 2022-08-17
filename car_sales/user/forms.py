from django.forms import ModelForm
from user.models import ContactUs

class ContactUsForm(ModelForm):

    class Meta:
        model = ContactUs
        exclude = ('user',)

class ContactUsAuthenticatedForm(ModelForm):

    class Meta:
        model = ContactUs
        fields = ('car_image','query',)