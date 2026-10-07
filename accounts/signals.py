from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import User, UserRoles




#if you plan to make users edit page, you can remove ""if created" condition to let the signal work for it
@receiver(post_save, sender=User)
def assign_user_role_group(sender, instance, created, **kwargs):
         print(instance.role)
         print('Hello signals')
         if instance.role == UserRoles.COMPANY_MANAGER:
                print('f')
                codenames = ['add_project', 'can_update_project', 'change_project', 'delete_project', 'add_category', 'add_task', 'can_manage_project', 'can_edit_project_status', 'delete_task', 'delete_post', 'can_create_blog', 'add_tag', 'view_tag', 'delete_tag', 'view_approval', 'change_approval']
                group, _ = Group.objects.get_or_create(name="company_managers")
                permission = Permission.objects.filter(codename__in=codenames)
        
                group.permissions.add(*permission)
                instance.groups.add(group)
        
         elif instance.role == UserRoles.SITE_MANAGER:
                        print('Site')
                        codenames = ['add_user', 'add_newsletter', 'view_newsletter', 'change_newsletter', 'delete_newsletter', 'delete_post', 'can_create_blog', 'add_tag', 'view_tag', 'delete_tag', 'view_approval', 'change_approval']
                        group, _ = Group.objects.get_or_create(name='site_managers')

                        permission = Permission.objects.filter(codename__in=codenames)
        
                        group.permissions.add(*permission)
                        instance.groups.add(group)

         elif instance.role == UserRoles.EMPLOYEE:
            
              codenames = ['can_manage_project', 'can_edit_project_status', 'can_write_note', 'change_task']
              group, _ = Group.objects.get_or_create(name='employees')
              permission = Permission.objects.filter(codename__in=codenames)
              group.permissions.add(*permission)  

              instance.groups.add(group)


