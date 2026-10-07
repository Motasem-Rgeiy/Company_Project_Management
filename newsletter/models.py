from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email



class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
  #  image = models.ImageField(null=True, blank=True)
  #  uploaded_file = models.FileField(null=True, blank=True)
    #Must be only a site manager
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title




class NewsletterStatus(models.IntegerChoices):
        PENDING = 1, _('pedning')
        DELIVERED = 2, _('delivered')
        FAILED = 3, _('failed')


#Record the emails with their status for monitoring
#Used for future purposes like displaying newsletters in a chart  or show the successed and failed emails 
class NewsletterHistory(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.PROTECT)
    status = models.IntegerField(choices=NewsletterStatus.choices, default=NewsletterStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)