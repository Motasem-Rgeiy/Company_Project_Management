from django import forms
from . import models
from django.utils.translation import gettext as _

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'body', 'image', 'category', 'tags']

        labels = {
            'title': _('Title'),
            'body':_('Body'),
            'image':_('Image'),
            'category':_('Category'),
            'tags':_('Tags')
        }

        widgets = {
                    'title': forms.TextInput(attrs={
                        'class': 'bg-slate-200 w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'
                    }),
                    'body': forms.Textarea(attrs={
                        'class': 'bg-slate-200  border border-slate-300 w-full h-36 p-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'
                    }),
                 
                    'image': forms.FileInput(attrs={
                        'class': 'block  text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-slate-800 file:text-slate-100 hover:file:bg-slate-700 cursor-pointer'
                    }),
                    'category': forms.Select(attrs={
                        'class': 'bg-slate-100 border border-slate-300 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-indigo-500'
                    }),
                    'tags': forms.SelectMultiple(attrs={
                        'class': 'bg-slate-100 border border-slate-300 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-indigo-500'
                    }),
                }


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ['name']
        labels = {"name": _("Tag name")}
        widgets = {
             'name': forms.TextInput(attrs={
                                'class': 'bg-slate-200 w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mt-1',
                                'placeholder':'New Tag'
                            }),
                            }



class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body']
        labels = {'body': _('Body')}