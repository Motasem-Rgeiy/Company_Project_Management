from django import forms
from . import models
from accounts.models import User, UserRoles
from django.utils.translation import gettext_lazy as _

class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['title', 'description', 'due_date', 'uploaded_file', 'category', 'users']
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'due_date': _("Due date"),
            'uploaded_file': _('Uploaded File'),
            'category': _('Category'),
            'users': _('Users')
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'bg-slate-200 w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-slate-200  border border-slate-300 w-full h-12 p-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'bg-slate-100 border border-slate-300 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'uploaded_file': forms.FileInput(attrs={
                'class': 'block  text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-slate-800 file:text-slate-100 hover:file:bg-slate-700 cursor-pointer'
            }),
            'category': forms.Select(attrs={
                'class': 'bg-slate-100 border border-slate-300 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'users': forms.SelectMultiple(attrs={
                'class': 'bg-slate-100 border border-slate-300 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['users'].queryset = User.objects.filter(role=UserRoles.EMPLOYEE)

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['title', 'due_date', 'uploaded_file', 'category', 'users']

        labels = {
                    'title': _('Title'),
                    'due_date': _("Due date"),
                    'uploaded_file': _('Uploaded File'),
                    'category': _('Category'),
                    'users': _('Users')
                }


    #Extra validation to ensure only employees are chosen
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
    
            self.fields['users'].queryset = User.objects.filter(role=UserRoles.EMPLOYEE)


class TaskCreateForm(forms.ModelForm):
    order = forms.IntegerField(required=False, initial=1)
    class Meta:
        model = models.Task
        fields = ['title', 'order','description', 'project']
        labels = {
            'title': _('Title'),
            'order': _('Order'),
            'description':_('Description'),
            'project':_('Project')
        }

    def clean_order(self):
        order = self.cleaned_data['order']

        if order is None:
     
            return 1

        return order


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name']
        labels = {'name': _('Name')}

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-slate-200 w-full px-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
        }


class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ['content']
        labels = {
            'content':_('Note')
        }

        widgets = {
            'content': forms.TextInput(attrs={
                'class':'bg-slate-100 p-2 shadow-md shadow-slate-200'
            })
        }
    







#can i benefit from in project management implementation
'''
  def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                project = models.Project.objects.filter(pk=self.instance.pk).last()
                users = project.users.all()
                self.fields['users'].queryset = users

'''