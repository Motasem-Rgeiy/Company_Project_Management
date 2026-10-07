from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('create', views.PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>', views.PostUpdateView.as_view(), name="post_update"),
    path('post/<int:postId>', views.post_details, name='post_details'),
    path('delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('category/create', views.CategoryCreateView.as_view(), name='blog_category_create'),
    path('tag', views.TagListView.as_view(), name='tag_list'),
    path('tag/create', views.TagCreateView.as_view(), name='tag_create'),
    path('tag/delete/<int:tagId>', views.tag_delete_view, name='tag_delete'),
    path('comment/save<int:pk>', views.comment_save, name='comment_save')
]
