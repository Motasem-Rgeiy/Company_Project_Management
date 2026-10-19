from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from . import models, forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
# Create your views here.


def hello(request):
    return render(request, 'base.html')

class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    form_class = forms.UserCreateForm
    template_name = 'registration/register.html'
    permission_required = 'accounts.add_user'
    raise_exception = True

    def form_valid(self, form):
        user = form.save(commit=False)
        if user.is_superuser:
            user.role = None

        user.save()
        form.save_m2m()
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse_lazy('project_list')