from django.db import models
from project.models import Project
from blog.models import Post
from accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
# Create your models here.

class ApprovalStatus(models.IntegerChoices):
    PENDING = 1, _('pending')
    APPROVED = 2, _('approved')
    REJECTED = 3, _('rejected')
    CANCELLED = 4, _('cancelled')


class Approval(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    target_object = GenericForeignKey('content_type', 'object_id') #used
    order = models.CharField(null=True, max_length=100)
    procedure = models.IntegerField(null=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    updated_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('content_type', 'object_id')


    @property
    def is_post(self):
        return self.content_type and self.content_type.model == 'post'

    @property
    def is_project(self):
        return self.content_type and self.content_type.model == 'project'

    
   