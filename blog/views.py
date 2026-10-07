from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from . import forms, models
from django.views import generic
from accounts.models import UserRoles
from project.models import Category
from project.forms import CategoryCreateForm
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required, login_required
from approval.models import Approval, ApprovalStatus
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _


#list posts page  < ALl users
#create post, category, tags at the same page < company manager, employees with permessions
#update post page < can edited by the publisher
#detail post, comments at the same page



class PostListView(generic.ListView):
     model = models.Post
     template_name = 'post/post_list.html'
     paginate_by = 12

     def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(status=models.PostStatus.PUBLISHED)
            .order_by('-created_at')  # Applied ordering directly
        )




#require building the comunication system between employee and maanger for aproving posting
class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Post
    form_class = forms.PostCreateForm
    template_name = 'post/post_create.html'
    raise_exception = True

    def form_valid(self, form):
        
        form.instance.publisher = self.request.user
        
     
        if self.request.user.role == UserRoles.EMPLOYEE:
            
            self.object = form.save()
           
            Approval.objects.create(
                    content_type=ContentType.objects.get_for_model(self.object),
                    object_id=self.object.pk,
                    order=_('Post'),
                    procedure=models.PostStatus.PUBLISHED,
                    requester=self.request.user,
                    )


            print('Your request has been sent to the manager.')

        else:
            print('You are the manager')
            form.instance.status = models.PostStatus.PUBLISHED
                    

        return super().form_valid(form)



    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # Pass category_form to the context for inclusion
            context['category_form'] = CategoryCreateForm()
            context['tag_form'] = forms.TagCreateForm()  # Ensure this is present!
            context['tag_list'] = models.Tag.objects.all()
            return context


    def get_success_url(self):            
            return reverse('post_list')









#Hide update button from anynoumos users and unrelated employees
#require building the comunication system between employee and maanger for aproving posting
class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
     model = models.Post
     form_class = forms.PostCreateForm
     template_name = 'post/post_update.html'
     raise_exception = True


     def get_object(self, queryset = None):
          post = super().get_object(queryset)

          if self.request.user.role == UserRoles.EMPLOYEE and post.publisher != self.request.user:
                raise PermissionDenied('You are not the publisher of this post!')

          return post


     def get_success_url(self):
          return reverse('post_details', args=[self.object.id])




    
#The deletion link button should be in update page.
#Employee can not delete any post at all.
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
     model = models.Post
     template_name = 'post/post_delete.html'
     permission_required = 'blog.delete_post'
     raise_exception = True

     def get_success_url(self):
          return reverse('post_list')




def post_details(request, postId):
     post = models.Post.objects.filter(pk=postId).last()

     
    
     if not post:
          return HttpResponse('Not found!')

     if post.status == models.PostStatus.DRAFTED and not request.user.is_authenticated:
          return HttpResponse('Not Available yet')

     
     if post.status == models.PostStatus.DRAFTED and request.user.role != UserRoles.SITE_MANAGER:
          return HttpResponse('Not Available yet')

     comment_counts = post.comment_set.all().count()

     return render(request, 'post/post_details.html', {'post':post, 'comment_count':comment_counts})




#Only site manager and company manager can create cat
class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
     model = Category
     form_class = CategoryCreateForm
     template_name = 'category/blog_category_create.html'
     permission_required = 'project.can_create_blog'
     raise_exception = True

     def get_success_url(self):
          return reverse('post_create')







class TagCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
     model = models.Tag
     form_class = forms.TagCreateForm
     template_name = 'tag/tag_create.html'
     permission_required = 'blog.add_tag'
     raise_exception = True


     def get_success_url(self):
            return reverse('post_create')



class TagListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
     model = models.Tag
     template_name = 'tag/tag_list.html'
     permission_required = 'blog.view_tag'
     raise_exception = True



@permission_required('blog.delete_tag', raise_exception=True)
@login_required
def tag_delete_view(request, tagId):
    tag = models.Tag.objects.filter(pk=tagId).last()
    if not tag:
         return HttpResponse('Not found!')

    tag.delete()

    return redirect('post_create')





@csrf_exempt
def comment_save(request, pk):
     post = models.Post.objects.filter(pk=pk).last()
     if not post:
          return  HttpResponse('Not found!')

     if request.method == "POST":
          form = forms.CommentCreateForm(request.POST)
          if form.is_valid():
               body = form.cleaned_data['body']
               models.Comment.objects.create(
                    body=body,
                    post = post,
                    publisher=request.user if request.user.is_authenticated else None
                    )
        

     return redirect('post_details', pk)

     