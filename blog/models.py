from django.db import models
from accounts.models import User
from project.models import Category
from django.utils.translation import gettext as _

# Create your models here.

class Tag(models.Model):
    name = models.CharField(200)

    def __str__(self):
            
            return self.name



class PostStatus(models.IntegerChoices):
    DRAFTED = 1, _('drafted')
    PENDING_UPDATE = 2, _('pending_update')
    REJECTED = 3, _('rejected')
    PUBLISHED = 4, _('published')





class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    status = models.IntegerField(choices=PostStatus.choices, default=PostStatus.DRAFTED)
  #  is_published = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='assigned_tags')



    def __str__(self):
        return self.title



#May status field is messing
class Comment(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    publisher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) #Need test + review




