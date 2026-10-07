from django.contrib import admin
from .models import Project, Category, Task, Note
# Register your models here.



admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Note)



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

