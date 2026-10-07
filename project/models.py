from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _
#project model

# Create your models here.

class ProjectStatus(models.IntegerChoices):
    PENDING = 1, _('pending')
    IN_PROGRESS = 2, _('in progress')
    UNDER_REVIEW = 3, _('under review')
    CANCELLED = 4, _('cancelled')
    COMPLETED = 5, _('completed')



class Category(models.Model):
   name = models.CharField(max_length=200)
   is_featured = models.BooleanField(default=False)


   class Meta:
       permissions = [
            ('can_create_blog', 'can_create a category in a blog'),

       
               ]
       


   def __str__(self):
       return self.name



#uploaded_file must be only .txt or .pdf
#description has no conditions.
#status must be handled upon on the user permissions in the view logic
#Review if null and black in users field is necessary to set

#fixed error: there is not beenfit from set null=True in users field
#fixed error: you can not use "projects" as a related_name(it's default)
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    uploaded_file = models.FileField( null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['txt' , 'pdf'])])
    status = models.IntegerField(choices=ProjectStatus, default=ProjectStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_projects', on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='assigned_projects')

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    class Meta:
        permissions = [
            ('can_manage_project', 'can manage a project'),
            ('can_edit_project_status', 'can edit a status of a project'),
            ('can_write_note', 'can write a note to a project')

        ]

    def __str__(self):
        return self.title




class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    is_checked = models.BooleanField(default=False)
    order = models.IntegerField(default=1,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)



#Review if null and black is necessary to set
class Note(models.Model):
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


