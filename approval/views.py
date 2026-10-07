from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Approval, ApprovalStatus
from project.models import ProjectStatus, Project
from blog.models import PostStatus, Post
from accounts.models import UserRoles
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required

# Create your views here.



class RequestListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Approval
    template_name = 'approve_list.html'
    permission_required = 'approval.view_approval'
    raise_exception = True
    context_object_name = 'approvals'


    def get_queryset(self):
        queryset = super().get_queryset().filter(status=ApprovalStatus.PENDING)
   

        if self.request.user.role == UserRoles.SITE_MANAGER:
            content_type = ContentType.objects.get_for_model(Post)
          
        elif self.request.user.role == UserRoles.COMPANY_MANAGER:
             content_type = ContentType.objects.get_for_model(Project)

        else:
             raise PermissionDenied('You are not allowed to open this page!')
             
        return queryset.filter(content_type=content_type)

        



   
@login_required
@permission_required('approval.change_approval', raise_exception=True)
def request_accept(request, pk):
    approve = Approval.objects.filter(pk=pk).last()

    if not approve:
             return HttpResponse('Not found!')


    if request.user.role == UserRoles.SITE_MANAGER and approve.is_project:
            raise PermissionDenied('You cannot accept this request.')


    if request.user.role == UserRoles.COMPANY_MANAGER and approve.is_post:
         raise PermissionDenied('You cannot accept this request.')


    instance = approve.target_object
    instance.status = approve.procedure
    instance.save()

    approve.status = ApprovalStatus.APPROVED
    approve.save()
        
   

    return redirect('approval_list')
      



@login_required
@permission_required('approval.change_approval', raise_exception=True)
def request_reject(request, pk):
    approve = Approval.objects.filter(pk=pk).last()

    if not approve:
         return HttpResponse('Not found!')
    
    
    if request.user.role == UserRoles.SITE_MANAGER and approve.is_project:
            raise PermissionDenied('Site managers cannot reject project requests.')
    
    
    if request.user.role == UserRoles.COMPANY_MANAGER and approve.is_post:
             raise PermissionDenied('Company managers cannot reject post requests.')

    
    if approve.is_post and approve.target_object:
        
        post = approve.target_object

        if post.status == PostStatus.DRAFTED:
             post.status = PostStatus.REJECTED

        post.save()


    approve.status = ApprovalStatus.REJECTED
   
    approve.save()


    return redirect('approval_list')
    