from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserRoles
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

class UserLoginForm(AuthenticationForm):
     def  __init__(self, request = ..., *args, **kwargs):
        super(UserLoginForm , self).__init__(*args, **kwargs)

     username = forms.CharField(
             label=_("Username"),
             widget=forms.TextInput(
                 attrs={
                     "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                     "placeholder": _("Username"),
                 }
             ),
         )

     password = forms.CharField(
             label=_("Password"),
             strip=False,
             widget=forms.PasswordInput(
                 attrs={
                     "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-800 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                 }
             ),
         )
    

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First Name"),
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                "placeholder": _("First name"),
            }
        ),
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                "placeholder": _("Last name"),
            }
        ),
    )

    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                "placeholder": _("Username"),
            }
        ),
    )

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                "placeholder": "email@example.com",
            }
        ),
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-800 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
            }
        ),
    )

    password2 = forms.CharField(
        label=_("Password Confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-800 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            'image'
        ]  # Include the fields you want rendered in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply the style to 'role' or any other field dynamically
        if "role" in self.fields:
            self.fields["role"].widget.attrs.update(
                {
                    "class": "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-800 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                }
            )

     
  


