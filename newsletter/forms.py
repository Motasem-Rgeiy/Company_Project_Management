from django import forms
from . import models
from django.utils.translation import gettext_lazy as _


class NewsletterCreateForm(forms.ModelForm):
    class Meta:
        model = models.Newsletter
        fields = ['title', 'body']
        labels = {
            'title': _('Title'),
            'body': _('Body'),
        }
