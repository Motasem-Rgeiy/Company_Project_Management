from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserRoles(models.IntegerChoices):
    COMPANY_MANAGER = 1, _('Company Manager')
    SITE_MANAGER = 2, _('Site Manager')
    EMPLOYEE = 3, _('Employee')

class User(AbstractUser):
    role = models.IntegerField(choices=UserRoles.choices, default=UserRoles.SITE_MANAGER)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


