from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('project/create', views.ProjectCreateView.as_view(), name='project_create'),
    path('project/update/<int:pk>', views.ProjectUpdateView.as_view(), name='project_update'),
    path('project/delete/<int:pk>',views.ProjectDeleteView.as_view(), name="project_delete"),
    path('project/task/create', views.taskCreateView, name='task_create'),
    path('project/task/delete/<int:taskId>', views.taskDeleteView, name='task_delete')    ,
    path('project/category/create',views.CategoryCreateView.as_view(), name='category_create'),
    path('project/task/check/<int:taskId>', views.task_check, name='task_check'),
    path('project/user/delete/<int:projectId>/<int:userId>', views.remove_users_from_project, name='project_user_remove'),
    path('project/manage/<int:projectId>', views.project_management, name='project_manage'),
    path('project/status/update/<int:projectId>', views.project_status_update, name='project_status_update'),
    path('project/note/save/<int:projectId>', views.note_save, name='note_save'),
]
