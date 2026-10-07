from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy, reverse
from django.views import generic
from . import  models, forms
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.models import UserRoles, User
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST, require_GET
from approval.models import Approval, ApprovalStatus
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _











class ProjectListView(generic.ListView):
    model = models.Project
    template_name = 'project/project_list.html'
    paginate_by = 6
  

    def get_queryset(self):
       

        if not self.request.user.is_authenticated:
            #Must be updated later to return only Completed
            return super().get_queryset().filter(status=models.ProjectStatus.COMPLETED)
        # 1. Base queryset filtered by owner (matching the context processor)

        if self.request.user.role == UserRoles.SITE_MANAGER:
               return super().get_queryset().filter(status=models.ProjectStatus.COMPLETED)
        
        queryset = super().get_queryset()

        
        employee_id = self.request.GET.get('employee')
        if employee_id:
            user = User.objects.filter(pk=employee_id).last()
            return user.assigned_projects.all()

        status = self.request.GET.get('status')
        
        if status:
              print(status)
              queryset = queryset.filter(status=int(status))


        return queryset.order_by('-created_at')


    









class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin  ,PermissionRequiredMixin, generic.CreateView):
    model = models.Project
    form_class = forms.ProjectCreateForm
    template_name = 'project/project_create.html'
    permission_required = 'project.add_project'
    raise_exception = True

    def test_func(self):
           if self.request.user.is_superuser:
                  return False
           
           return True


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse_lazy('project_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass category_form to the context for inclusion
        context['category_form'] = forms.CategoryCreateForm()
        return context










class ProjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = models.Project
    form_class = forms.ProjectUpdateForm
    template_name = 'project/project_update.html'
    permission_required = 'project.change_project'
    raise_exception = True

    def get_success_url(self):
            return reverse('project_update', args=[self.object.id])
    









#The deletion link button should be in update page.
class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
            model = models.Project
            template_name = 'project/project_delete.html'
            permission_required = 'project.delete_project'
            raise_exception = True

            def get_success_url(self):
                    return reverse('project_list')


            



   




#Must be accessed only by the owner
@permission_required('project.add_task', raise_exception=True)
@require_POST
@login_required
def taskCreateView(request):

        project_id = request.POST.get('project', None)
        if not project_id:
             return HttpResponse('Related project is not given')

        project = models.Project.objects.filter(pk=project_id).last()

        if not project:
             return HttpResponse('The project is not exist!')

       # if request.user != project.owner:
        #    raise PermissionDenied('You are not allowed to create a task to this project!')

       
        form = forms.TaskCreateForm(request.POST)
 
     
        if form.is_valid():
            print(form.cleaned_data)
            task = models.Task.objects.create(
                title = form.cleaned_data['title'],
                description= form.cleaned_data['description'],
                order = form.cleaned_data['order'],
                project = form.cleaned_data['project'],
            )
      

            task.save()
        else:
            print('Unvalid')
        

           
    
        return redirect('project_update', request.POST.get('project'))



@permission_required('project.delete_task', raise_exception=True)
@login_required
def taskDeleteView(request, taskId):
      task = models.Task.objects.filter(pk=taskId).last()

      if not task:
                  return HttpResponse('No found')
      
   #   if task.project.owner != request.user:
   #         raise PermissionDenied('You are not allowed!')
      

      task.delete()
      

      return redirect('project_update', task.project.pk)
      

    



#Must be accessed only by the company manager
class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
     model = models.Category
     form_class = forms.CategoryCreateForm
     permission_required = 'project.add_category'
     raise_exception = True
     template_name = 'category/category_create.html' 

     def get_success_url(self):
          return reverse('project_create')
  









#delete users from a project: many to many only by the company manager


@permission_required('project.change_project', raise_exception=True)
@login_required
def remove_users_from_project(request, userId, projectId):
        project = models.Project.objects.filter(pk=projectId).last()
        if not project:
            return HttpResponse('Not found')

    #    if project.owner != request.user:
     #           raise PermissionDenied('You are not allowed!')
        
        project.users.remove(userId)

        

        return redirect('project_update', projectId)












#Project management by related employees
#must be accessed only the owner and related users
@require_GET
@permission_required('project.can_manage_project', raise_exception=True)
@login_required
def project_management(request, projectId):
    
    project = models.Project.objects.filter(pk=projectId).last()

    if not project:
                return HttpResponse('Not Found!')

    if project.status in [models.ProjectStatus.CANCELLED, models.ProjectStatus.COMPLETED]:
           return HttpResponse('The project is not available.')

    if request.user not in project.users.all() and request.user.role != UserRoles.COMPANY_MANAGER:
        raise PermissionDenied('You Are not allowed to access this page')



    due_date_duration =project.due_date - project.created_at.date()


    available_status = [
         ('pending', models.ProjectStatus.PENDING),
           ('in_progress', models.ProjectStatus.IN_PROGRESS),
             ('under_review', models.ProjectStatus.UNDER_REVIEW),
         ]

    last_note = project.note_set.order_by('-created_at').first()

    all_status = models.ProjectStatus.choices
  

    context = {'project':project,
              'due_date_duration':due_date_duration,
                'status':available_status,
                'last_note':last_note,
                'all_status':all_status,
          #      'tasks_page': tasks_page,
          #       'users_page': users_page,
           #      'notes_page': notes_page,
                   }
    
   

    return render(request, 'project/project_manage.html', context)










#must be accessed only the owner and related users
#check button must be disabled for company manager!
#all status must be shown in the tamplate
#But complated status and cancalled logic should be done alone
@require_POST
@permission_required('project.change_task', raise_exception=True)
@login_required
def task_check(request, taskId):
    task = models.Task.objects.filter(pk=taskId).last()
    if not task:
         return HttpResponse('Not Found!')

    if request.user not in task.project.users.all():
          raise PermissionDenied('You are not in the team!')

    project_id = task.project.id


    is_checked = request.POST.get('is_checked')
    
    if is_checked:
               task.is_checked = True
               
    else:
                
                task.is_checked = False
    
    task.save()
           
    return redirect('project_manage', project_id)







#must be accessed only the owner and related users
#here the logic of status request to the manager is done
#Review the ability of company manager to change the status

@permission_required('project.can_edit_project_status', raise_exception=True)
@login_required
@require_POST
def project_status_update(request, projectId):
     print('hello')
     print(projectId)

     project = models.Project.objects.filter(pk=projectId).last()
     #if not project:
         # return HttpResponse('Not Found!')

     if request.user not in project.users.all() and request.user.role == UserRoles.EMPLOYEE:
               raise PermissionDenied('You are not in the team!')
     

                 #check from the user role, employees shouldnot edit to complete or cancelled
        
     status = json.loads(request.body).get('status')
     if project.status in [models.ProjectStatus.COMPLETED, models.ProjectStatus.CANCELLED]:
                return JsonResponse({'message':_('The project is not valid!')})
     
     status = int(status)
     approval = Approval.objects.filter(content_type=ContentType.objects.get_for_model(project), object_id=project.id,).last()
     if status in [models.ProjectStatus.PENDING, models.ProjectStatus.IN_PROGRESS, models.ProjectStatus.UNDER_REVIEW]:
                if approval:
                      approval.status = ApprovalStatus.CANCELLED
                      approval.save()
                project.status = status
                project.save()
                return JsonResponse({'message':_('The status has been changed.'), 'update':True})

     elif status in [models.ProjectStatus.COMPLETED, models.ProjectStatus.CANCELLED]:

            if status == models.ProjectStatus.COMPLETED:
                    target_status = models.ProjectStatus.COMPLETED
            

            else:
                  target_status = models.ProjectStatus.CANCELLED

            if not approval:
                    Approval.objects.create(
                                              content_type=ContentType.objects.get_for_model(project),
                                              object_id=project.id,
                                              order=_('Project Status'),
                                              procedure=target_status,
                                              requester=request.user,
                                              )
                  
            else:
                  approval.procedure = target_status
                  approval.status = ApprovalStatus.PENDING
                  approval.requester = request.user
                  approval.save()


            return JsonResponse({'message':_('Your request is sent to the manager.'), 'update':False}, status=200) 
            

     else:
            return JsonResponse({"message":_('The status is not available in our Database!')})
     
 
     

#must be accessed only the owner and related users
#This view requires extra validation for the note per day logic
@csrf_exempt
@require_POST
@permission_required('project.can_write_note', raise_exception=True)
@login_required
def note_save(request, projectId):
            print(projectId, 'jjj')
            form = forms.NoteCreateForm(request.POST)
            
            if form.is_valid():
                   print(form.cleaned_data)
                   models.Note.objects.create(
                        content=form.cleaned_data['content'],
                        project_id=projectId,
                        user=request.user    
                   )

                   return redirect('project_manage', projectId)
            else:
                   return HttpResponse('The form is not valid!')

            



       