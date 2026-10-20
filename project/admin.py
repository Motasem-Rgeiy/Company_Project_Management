from django.contrib import admin
from .models import Project, Category, Task, Note
# Register your models here.



admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Note)
admin.site.register(Project)


